import os
import subprocess

def run_python_file(
	working_directory: str, file_path: str, args: list[str] | None = None
	) -> str:
	try:
		working_dir_abs = os.path.abspath(working_directory)
		full_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

		if os.path.commonpath([working_dir_abs, full_path]) != working_dir_abs:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

		if not os.path.isfile(full_path):
			return f'Error: "{file_path}" does not exist or is not a regular file'

		name, _, ext = file_path.rpartition(".")

		if ext != "py":
			return f'Error: "{file_path}" is not a Python file'

		command = ["python", full_path]

		if args:
			command.extend(args)

		child = subprocess.run(command, capture_output=True, timeout=30, text=True)
		result = []

		if child.returncode != 0:
			result.append(f"Process exited with code {child.returncode}")

		if not child.stdout and not child.stderr:
			result.append("No output produced")

		if child.stdout:
			result.append(f"STDOUT: {child.stdout}")

		if child.stderr:
			result.append(f"STDERR: {child.stderr}")

	except Exception as e:
		return f"Error executing Python file: {e}"

	return "\n".join(result)

schema_run_python_file = {
	"type": "function",
	"function": {
		"name": "run_python_file",
		"description": "Execute a Python file, optionally passing a list of arguments",
		"parameters": {
			"type": "object",
			"properties": {
				"file_path": {
					"type": "string",
					"description": "Path to the target file, relative to the working directory",
                },
				"args": {
					"type": "array",
					"items": {
						"type": "string"
					},
					"description": "Optional list of strings that will be passed as arguments to the file being executed"
				},
			},
			"required": ["file_path"]
		},
	},
}
