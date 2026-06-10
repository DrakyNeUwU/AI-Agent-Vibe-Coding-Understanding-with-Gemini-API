import os
import subprocess
from google.genai import types
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Bước 2: check path traversal
        if not target_file.startswith(working_dir_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Bước 3: check file tồn tại
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Bước 4: check đuôi .py
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Bước 5+6: build command
        command = ["python", target_file]
        if args:
            command.extend(args)

        # Bước 7: chạy file
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )

        # Bước 8: build output string
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT: {result.stdout}"
            if result.stderr:
                output += f"STDERR: {result.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file at the given path, relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)