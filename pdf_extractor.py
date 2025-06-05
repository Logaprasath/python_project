"""
Extracts name and email from a PDF file and saves the information to a JSON file.
"""
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import re
import json # Make sure this is at the top

def extract_name_email_from_pdf(pdf_path):
    """
    Extracts text from the given PDF and searches for a name and email.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        dict: A dictionary {"name": found_name, "email": found_email}.
              Values are None if not found or if an error occurs during PDF processing.
              Prints an error message to stderr if PDF processing fails.
    """
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

    # Regex to find email addresses.
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        found_email = email_match.group(0)

    # Regex for name: Looks for sequences of capitalized words (e.g., "Firstname Lastname").
    # This is a simplistic approach and might incorrectly identify capitalized words in headers
    # or other parts of the document. Further refinement might be needed for better accuracy.
    name_match = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", text) # Looking for at least two capitalized words
    if name_match:
        found_name = name_match.group(0).strip()
        # Attempt to filter out names that are likely all-caps headers or have an unusual ratio of caps to lowercase.
        # This check helps to avoid matching overly capitalized strings as names.
        if found_name.isupper(): # if the whole string is uppercase
            found_name = None
        elif len(re.findall(r"[A-Z]", found_name)) > len(re.findall(r"[a-z]", found_name)) * 1.5 : # if significantly more caps than lowercase
             found_name = None


    return {"name": found_name, "email": found_email}

def save_to_json(data, json_file_path):
    """
    Saves the given data dictionary to a JSON file.

    Args:
        data (dict): The dictionary to save.
        json_file_path (str): Path to the output JSON file.

    Prints an error message to stderr if saving fails.
    """
    try:
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON {json_file_path}: {e}")

if __name__ == "__main__":
    # Define file paths
    pdf_file = "sample_resume.pdf"  # Path to the input PDF file
    json_file = "output.json"       # Path to the output JSON file

    print(f"Extracting data from {pdf_file}...")

    # Attempt to extract data from the PDF
    # Note: This will raise FileNotFoundError if sample_resume.pdf does not exist.
    # The script's internal error handling for extract_name_email_from_pdf
    # will also catch issues during PDF processing itself.
    try:
        extracted_data = extract_name_email_from_pdf(pdf_file)

        # Check if any data (name or email) was successfully extracted
        if extracted_data.get("name") or extracted_data.get("email"):
            print(f"Saving data to {json_file}...")
            # Save the extracted data to a JSON file
            save_to_json(extracted_data, json_file)
            print("Extraction and saving complete.")
            print(f"Extracted data: {extracted_data}")
        elif extracted_data.get("name") is None and extracted_data.get("email") is None and not pdf_file_exists_in_try_block_scope_hack_for_FileNotFound_check : # if processing happened but found nothing
            print("No name or email found in the PDF.")
            # Optionally, one might still want to save an empty JSON or log this.
            # For now, just printing a message. If output.json should still be created:
            # save_to_json(extracted_data, json_file)
            # print(f"Empty data structure saved to {json_file}")
        # If extracted_data itself is None (e.g. from a processing error handled inside extract_name_email_from_pdf),
        # an error message would have already been printed by that function.
        # The main block's FileNotFoundError will catch if the PDF isn't there to begin with.


    except FileNotFoundError:
        # This handles the case where the PDF file itself is not found.
        print(f"Error: The input PDF file '{pdf_file}' was not found. Please ensure it exists in the specified path.")
    except Exception as e:
        # Catch-all for any other unexpected errors during the main execution.
        print(f"An unexpected error occurred in the main execution block: {e}")

# A bit of a hack to make the conditional logic cleaner above,
# as the `extracted_data` variable will exist due to the try block structure,
# but we need to distinguish "file not found" from "file processed but no data found".
# This variable is not robust and is just for this specific control flow.
pdf_file_exists_in_try_block_scope_hack_for_FileNotFound_check = True
try:
    open(pdf_file, 'rb').close() # Check if file exists before main try block to set the flag
except FileNotFoundError:
    pdf_file_exists_in_try_block_scope_hack_for_FileNotFound_check = False
