from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import re
import json # Make sure this is at the top

def extract_name_email_from_pdf(pdf_path):
    output_string = StringIO()
    laparams = LAParams() # Use default LAParams
    text = "" # Initialize text to ensure it's available in case of error

    try:
        with open(pdf_path, 'rb') as fh:
            extract_text_to_fp(fh, output_string, laparams=laparams, output_type='text', codec='utf-8')
        text = output_string.getvalue()
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        return {"name": None, "email": None}
    finally:
        output_string.close()

    found_name = None
    found_email = None

    # Regex for email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        found_email = email_match.group(0)

    # Regex for name (simple example)
    # This regex is very basic and might need significant improvement.
    # It looks for sequences of capitalized words.
    name_match = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", text) # Looking for at least two capitalized words
    if name_match:
        found_name = name_match.group(0).strip()
        # Avoid matching lines that are likely headers or titles in all caps by checking character ratio
        if found_name.isupper(): # if the whole string is uppercase
            found_name = None
        elif len(re.findall(r"[A-Z]", found_name)) > len(re.findall(r"[a-z]", found_name)) * 1.5 : # if too many caps
             found_name = None


    return {"name": found_name, "email": found_email}

# ... (existing extract_name_email_from_pdf function) ...

def save_to_json(data, json_file_path):
    try:
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON {json_file_path}: {e}")

if __name__ == "__main__":
    pdf_file = "sample_resume.pdf"  # Assumed sample PDF
    json_file = "output.json"

    print(f"Extracting data from {pdf_file}...")
    # Note: This will raise FileNotFoundError if sample_resume.pdf does not exist
    # For the purpose of this step, we assume the file might not be present yet.
    # Actual execution with a PDF would be a separate testing/running step.
    try:
        extracted_data = extract_name_email_from_pdf(pdf_file)

        if extracted_data.get("name") or extracted_data.get("email"): # Check if any data was actually found
            print(f"Saving data to {json_file}...")
            save_to_json(extracted_data, json_file)
            print("Extraction and saving complete.")
            print(f"Extracted data: {extracted_data}")
        else:
            print("No name or email found in the PDF.")
            # Optionally save even if empty, or handle as an error
            # For now, just printing a message. If output.json should still be created:
            # save_to_json(extracted_data, json_file)
            # print(f"Empty data saved to {json_file}")


    except FileNotFoundError:
        print(f"Error: The file {pdf_file} was not found. Please make sure it exists in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
