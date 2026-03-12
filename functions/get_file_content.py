import os
from config import MAX_READ_CHARS

def get_file_content(working_directory, file_path):
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target file
        target_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if target_file falls within the absolute working_directory path
        valid_target_file = os.path.commonpath([working_dir_abs, target_abs]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Open and read up to MAX_READ_CHARS
        with open(target_abs, "r") as f:
            content = f.read(MAX_READ_CHARS)
            # Check if there is more data after MAX_READ_CHARS
            if f.read(1):  # read one more char; if not EOF, it was truncated
                content += f'[...File "{file_path}" truncated at {MAX_READ_CHARS} characters]'

        return content
    except Exception as e:
        return f'Error: {e}'
