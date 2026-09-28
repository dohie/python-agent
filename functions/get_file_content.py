import os

def get_file_content(working_directory: str, file_path: str) -> str:
    contents = ""
    try:
        working_dir_abs = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, full_path]) != working_dir_abs:
            return f'Error: Cannot list "{file_path}" as it is outside thde permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        file = open(full_path)
        contents = file.read(10000)
        if file.read(1):
            contents += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error encountered: {e}"
    return contents

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of the specified file, with a limit of 10,000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the target file, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
