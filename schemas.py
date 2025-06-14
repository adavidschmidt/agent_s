from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content within a file in specified directory truncating the output if it exceeds 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to read from relative to the working directory. If not provided an error will occur",
            ),
        },
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file within the the provided working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file to run relative to the working directory. If not provided, an error will occur",
            ),
        },
    ),
)


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a given file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file in which to write the gieven content, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the given file",
            ),
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)