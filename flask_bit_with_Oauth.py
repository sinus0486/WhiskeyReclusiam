from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import sqlite3

app = Flask(__name__)

# Configure the app with your Google OAuth credentials
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['GOOGLE_OAUTH_CLIENT_ID'] = 'your_google_client_id'
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = 'your_google_client_secret'

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Simulated user database
users = {}

# Flask-Login User class
class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<User: {self.name}>"

# Setup Google OAuth
google_bp = make_google_blueprint(
    client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    redirect_to='google_login'
)
app.register_blueprint(google_bp, url_prefix='/login')

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Google login callback
@app.route("/login/google/authorized")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()

    user_id = user_info["id"]
    email = user_info["email"]
    name = user_info["name"]

    # If user doesn't exist, add them
    if user_id not in users:
        users[user_id] = User(id_=user_id, name=name, email=email)

    user = users[user_id]
    login_user(user)

    return redirect(url_for("dashboard"))

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Protected dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
