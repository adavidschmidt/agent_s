import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_path, file_path))
    if os.path.commonpath([abs_working_path, abs_file_path]) != abs_working_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory' 
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found'
    if os.path.splitext(abs_file_path)[1] != ".py":
        return f'Error: "{file_path}" is not a Python file'
    try:
        output = subprocess.run(['python3', file_path],
                                capture_output=True,
                                text=True, 
                                timeout=30,
                                cwd=abs_working_path)
        
        response = []
        if output.stdout:
            response.append(f"STDOUT: {output.stdout}")
        if output.stderr:
            response.append(f"STDERR: {output.stderr}")
        if output.returncode != 0:
            response.append(f"Process exited with code {output.returncode}")
        if len(response) == 0:
            response.append("No output produced")
        return "\n".join(response)
    except Exception as e:
        return f'Error: executing Python file: {e}'