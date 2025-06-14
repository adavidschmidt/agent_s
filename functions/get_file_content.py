import os

def get_file_content(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    path_to_file = os.path.abspath(os.path.join(working_path, file_path))
    if os.path.commonpath([working_path, path_to_file]) != working_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path_to_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    MAX_CHARS = 10000
    try:
        with open(path_to_file,"r") as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) == MAX_CHARS:
                file_content += f'\n...File "{file_path}" turncated at 10000 characters'
        return file_content
    except Exception as e:
        return f'Error reading "{file_path}": {e}'