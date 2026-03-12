import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Construct the full path to the target file
        target_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if target_file falls within the absolute working_directory path
        valid_target_file = os.path.commonpath([working_dir_abs, target_abs]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file' 
        if not target_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_abs]

        # If args is not None, extend the command list with args
        if args is not None:
            command.extend(args)

        # Run the command using subprocess.run()
        result = subprocess.run(
            command, 
            cwd=working_dir_abs, 
            capture_output=True, 
            text=True, 
            timeout=30
            )
        
        # Handle the return code
        if result.returncode != 0:
            return f'Process exited with code {result.returncode}'

        # If both stdout and stderr are empty
        if result.stdout.strip() == '' and result.stderr.strip() == '':
            return 'No output produced'
        
        # Otherwise prefix stdout and stderr
        parts = []
        if result.stdout.strip() != '':
            parts.append(f'STDOUT: {result.stdout.rstrip()}')
        if result.stderr.strip() != '':
            parts.append(f'STDERR: {result.stderr.rstrip()}')

        return '\n'.join(parts)
    
    except subprocess.TimeoutExpired:
        return 'Process timed out'
    except Exception as e:
        return f"Error: executing Python file: {e}"