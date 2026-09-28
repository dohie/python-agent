import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.exists(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            result = [f'Success: "{directory}" is within the working directory']
        if directory == ".":
            result.append("Result for current directory:")
        else:
            result.append(f"Result for '{directory}'")
        contents = os.listdir(target_dir)
        for item in contents:
            full_path = os.path.join(target_dir, item)
            result.append(f"{item}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}")
    except Exception as e:
        return f"Error encountered: {e}"
    return '\n'.join(result)

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
    
        
        
        
        
