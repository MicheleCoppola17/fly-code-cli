import os

def write_file(working_directory, file_path, content):
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target file
        target_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if target_file falls within the absolute working_directory path
        valid_target_file = os.path.commonpath([working_dir_abs, target_abs]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
            
        if os.path.isdir(target_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Ensure all parent directories of the file exist
        parent_dir = os.path.dirname(target_abs)
        os.makedirs(parent_dir, exist_ok=True)

        # Open the file and write content
        with open(target_abs, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'