from PyPDF2 import PdfReader
import os

def pdf_to_text(pdf_path, page_number):
    """
    Extracts text from a specific page of a PDF file.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        if 0 < page_number <= len(reader.pages):
            page_index = page_number - 1
            text = reader.pages[page_index].extract_text() or ""
    return text

# Your other functions and the rest of your script follow here...


def text_to_markdown(text, output_path):
    """
    Converts the extracted text to Markdown format and saves it to a file. 
    """
    markdown_text = f"```\n{text}\n```"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_text)


# Example usage
input_pdf_path = r"C:\Users\steph\Downloads\Player-Survival-Guide-v1.2.pdf"
base_output_dir = r"C:\Users\steph\OneDrive\Default\Documents\Projects\WhiskeyReclusiam\WhiskeyReclusiam\Macallan\Mothership_Data\Rulesoutput"
pages_to_extract = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]

for page_number in pages_to_extract:
    pdf_text = pdf_to_text(input_pdf_path, page_number)
    output_md_path = os.path.join(base_output_dir, f"Page_{page_number}.md")
    text_to_markdown(pdf_text, output_md_path)
    print(f"Page {page_number} from the PDF has been successfully saved to: {output_md_path}")
