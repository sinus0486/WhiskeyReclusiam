from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'warhammer_scores.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# Home route: displays the leaderboard and form
@app.route('/')
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, total_score, games_played FROM players ORDER BY total_score DESC")
    players = cur.fetchall()
    conn.close()
    return render_template('index.html', players=players)

# Route to handle adding scores
@app.route('/add_score', methods=['POST'])
def add_score():
    player_name = request.form['player_name']
    score = float(request.form['score'])
    is_winner = request.form.get('is_winner') == 'on'

    # Calculate proportional penalty for winning
    if is_winner:
        penalty = 0.10 * score
        score -= penalty

    conn = get_db()
    cur = conn.cursor()
    # Update player score and games played
    cur.execute("UPDATE players SET total_score = total_score + ?, games_played = games_played + 1 WHERE name = ?", (score, player_name))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# Route to add a new player
@app.route('/add_player', methods=['POST'])
def add_player():
    player_name = request.form['player_name']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (name, total_score, games_played) VALUES (?, 0, 0)", (player_name,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
