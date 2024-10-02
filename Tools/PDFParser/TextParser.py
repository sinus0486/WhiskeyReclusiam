import re
import json

def parse_sections_from_text_file(file_path, output_file):
    # Adjusted regular expression: handles more flexible spacing and titles (assuming all caps regardless of spacing)
    section_pattern = re.compile(r'^\d{2}\.\d{1,2}\s+[A-Z][A-Z\s]*$')
    sections = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_section = None

    # Process each line and match against the section pattern
    for line in lines:
        line = line.strip()

        # Check if this is a new section
        if section_pattern.match(line):
            # Debug output to see if sections are correctly identified
            print(f"New section found: {line}")

            # If there's already a current section, save it before starting a new one
            if current_section:
                sections.append(current_section)
            
            # Start a new section block
            current_section = {'section': line, 'text': ''}
        elif current_section:
            # Accumulate text under the current section
            current_section['text'] += line + ' '
    
    # Add the very last section if it exists, after the loop
    if current_section:
        sections.append(current_section)
    
    # Output the collected sections to the JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(sections, json_file, indent=2)

# File paths - adjust as necessary
input_file = r'C:\Users\steph\OneDrive\Default\Documents\Projects\WhiskeyReclusiam\WhiskeyReclusiam\Macallan\Mothership_Data\Rules\Rulesoutput.md'
output_file = r'C:\Users\steph\OneDrive\Default\Documents\Projects\WhiskeyReclusiam\WhiskeyReclusiam\Macallan\Mothership_Data\Rules\Clean_Rules.json'

# Execute the function
parse_sections_from_text_file(input_file, output_file)
