import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Check if target_dir falls within the absolute working_directory path
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        # List all items in the target directory
        dir_items = os.listdir(target_dir)
        
        # Build the result string line by line
        lines = []
        for item in dir_items:
            item_path = os.path.join(target_dir, item)

            # Get size and is_dir info
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            line = f"- {item}: file_size={size} bytes, is_dir={is_dir}"
            lines.append(line)

        # Join lines with newlines and return
        return "\n".join(lines)
    
    except Exception as e:
        # Return generic error string prefixed with "Error:"
        return f'Error: {e}'
    
# This tells the LLM how the function should be called
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
    