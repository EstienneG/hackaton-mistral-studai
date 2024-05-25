import fitz  # PyMuPDF
import re

def clean_extracted_text(text):
    import re  # Import regular expressions library
    lines = text.split('\n')
    cleaned_lines = []
    last_line_was_heading = False  # To track consecutive heading lines

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Handle consecutive heading lines
        current_line_is_heading = line.startswith("#")
        if current_line_is_heading and last_line_was_heading:
           line = line.replace('#', '')  # Remove all '#' symbols from the line
        last_line_was_heading = current_line_is_heading

        # Use a regular expression to match lines starting with '#' followed by one or several spaces and 'CHAPITRE'
        if re.match(r'^#\s+CHAPITRE', line):
            line = "\n\n" + line  # Prepend two line breaks

        # Decide on line breaks based on punctuation and specific cases
        if line.endswith('.'):
            # End of sentence or apostrophe, allow for normal line break
            cleaned_lines.append(line + "\n")
        else:
            # No line break for continuing sentences or lines ending with "l'"
            cleaned_lines.append(line + " ")

    return ''.join(cleaned_lines).strip()


def extract_and_clean_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        text = ""
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        # Check for bold and italic
                        is_bold = span['flags'] & 16  # Bold flag
                        is_italic = span['flags'] & 2  # Italic flag
                        # if span['size'] == 11.0 and is_bold and is_italic:
                        #     text += "## " + span['text'] + "\n"  # Consider as subtitle
                        if span['size'] >= 14.0:  # Title
                            text += "# " + span['text'] + "\n"
                        # elif span['size'] >= 11.0:  # Subtitle
                        #     text += "## " + span['text'] + "\n"
                        else:
                            text += span['text'] + "\n"
        # Clean the extracted text before adding it to the full_text
        cleaned_text = clean_extracted_text(text)
        full_text += cleaned_text

    return full_text


# Specify the path to your PDF here
pdf_path = "hackaton-mistral-studai/data/RAGAS_09_2023.pdf"
text = extract_and_clean_text(pdf_path)
print(text)
