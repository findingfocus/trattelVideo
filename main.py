from docxtpl import DocxTemplate
import os
import zipfile
from datetime import datetime
import shutil

OUTPUT_FOLDER = "Output"

def clear_output_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def perform_task(year, videographer, month_str, day, start_time, deponent, case_name, plaintiff_attorney, defense_attorney):
    # Convert month to integer and validate
    try:
        month = int(month_str)
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12.")
    except ValueError as e:
        return str(e), None

    month_text = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][month - 1]

    def get_day_suffix(day):
        if 10 <= day <= 20:
            return 'th'
        last_digit = day % 10
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(last_digit, 'th')

    try:
        day = int(day)
        if day < 1 or day > 31:
            raise ValueError("Day must be between 1 and 31.")
    except ValueError as e:
        return str(e), None

    day_suffix = get_day_suffix(day)

    # Clear the output folder before generating new files
    clear_output_folder(OUTPUT_FOLDER)

    # Define file paths
    date_str = f"{year}-{month:02}-{day:02}"
    readon_path = f"{OUTPUT_FOLDER}/READON {deponent} {month}-{day}-{year}.docx"
    videolog_path = f"{OUTPUT_FOLDER}/{deponent} {month}-{day}-{year}.docx"
    zip_filename = f"{OUTPUT_FOLDER}/{date_str} {deponent} Video Worksheets.zip"

    # Create Output directory if it doesn't exist
    os.makedirs(os.path.dirname(readon_path), exist_ok=True)

    # Create and save .docx files
    try:
        subject_line = f"{month}-{day}-{year} {deponent} Deposition"
        # Example for creating a .docx file using docxtpl
        doc = DocxTemplate("readonTemplate.docx")  # Make sure to have a template file
        context = {
            'year': year,
            'videographer': videographer,
            'month': month_text,
            'day': day,
            'suffix': day_suffix,
            'start_time': start_time,
            'deponent': deponent,
            'case_name': case_name,
            'plaintiff_attorney': plaintiff_attorney,
            'defense_attorney': defense_attorney,
            'subject_line': subject_line
        }
        doc.render(context)
        doc.save(readon_path)

        # Use videologTemplate
        videolog_template_path = "videologTemplate.docx"
        doc = DocxTemplate(videolog_template_path)  # Adjust path if needed
        doc.render(context)  # Use the same context or adjust as needed
        doc.save(videolog_path)

        # Create the ZIP file
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(readon_path, os.path.basename(readon_path))
            zipf.write(videolog_path, os.path.basename(videolog_path))

    except Exception as e:
        return f"Error generating files: {e}", None

    return zip_filename, None