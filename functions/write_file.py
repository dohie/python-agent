import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
	try:
		working_dir_abs = os.path.abspath(working_directory)
		full_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
		if os.path.commonpath([working_dir_abs, full_path]) != working_dir_abs:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
		if os.path.isdir(full_path):
			return f'Error: Cannot write to "{file_path}" as it is a directory'
		os.makedirs(os.path.dirname(full_path), exist_ok=True)
		with open(full_path, "w") as file:
			file.write(content)
	except Exception as e:
		return f"Error encountered: {e}"
	return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = {
	"type": "function",
	"function": {
		"name": "write_file",
		"description": "Write to a file, creating a new file or overwriting the contents if an existing file is	specified",
		"parameters": {
			"type": "object",
			"properties": {
				"file_path": {
					"type": "string",
					"description": "Path to the target file, relative to the working directory",
				},
				"content": {
					"type": "string",
					"description": "Content to be written to the file"
				},
			},
			"required": ["file_path", "content"]
		},
	},
}
