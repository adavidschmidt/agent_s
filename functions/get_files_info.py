import os

def get_files_info(working_directory, directory=None):
    working_path = os.path.abspath(working_directory)
    if directory is not None:
        directory_path = os.path.abspath(os.path.join(working_directory, directory))
    else:
        directory_path =working_path
    if os.path.commonpath([working_path, directory_path]) != working_path:
        return f'Error: Cannot list "{directory}" as it is outsied the permitted working directory'
    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'
    dir_list = os.listdir(directory_path)
    try:
        file_list = []
        for i in dir_list:
            path = os.path.join(directory_path, i)
            size = os.path.getsize(path)
            is_dir =  os.path.isdir(path)
            string = f"- {i}: file_size={size} bytes, is_dir={is_dir}"
            file_list.append(string)
        joined_file_list = "\n".join(file_list)
        return joined_file_list
    except Exception as e:
        return f'Error listing files: {e}'
