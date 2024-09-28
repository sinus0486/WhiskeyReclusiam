from PyPDF2 import PdfReader
import json

def pdf_to_text(pdf_path, pages=None):
    """
    Extracts text from specific pages of a PDF file.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        
        # Determine which pages to extract text from
        if pages is None:
            pages_to_extract = range(num_pages)
        else:
            # Adjust for PyPDF2's 0-based index
            pages_to_extract = [p - 1 for p in pages if 0 < p <= num_pages]
        
        # Extract text from specified pages
        for i in pages_to_extract:
            page_text = reader.pages[i].extract_text() or ""
            text += page_text + "\n"
    return text

def text_to_markdown(text):
    """
    Converts the extracted text to Markdown format. 
    """
    # Using a basic Markdown format with code blocks to preserve text format
    markdown_text = f"```\n{text}\n```"
    return markdown_text

# Example usage
input_pdf_path = r"C:\Users\steph\Downloads\Player-Survival-Guide-v1.2.pdf"
output_md_path = r"C:\Users\steph\OneDrive\Default\Documents\Projects\WhiskeyReclusiam\WhiskeyReclusiam\Macallan\Mothership_Data\Rulesoutput.md"
pages_to_extract = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, ]  # Specify the pages you want to extract

# Extract text from specific pages of the PDF
pdf_text = pdf_to_text(input_pdf_path, pages=pages_to_extract)

# Convert extracted text to Markdown
pdf_markdown = text_to_markdown(pdf_text)

# Save the Markdown output
with open(output_md_path, "w", encoding="utf-8") as md_file:
    md_file.write(pdf_markdown)

print("Specific pages from the PDF have been successfully parsed into a Markdown file.")
