import os
from google.genai import types
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Bước 2: check path traversal
        if not target_file.startswith(working_dir_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Bước 3: check có phải directory không
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Bước 4: tạo parent directories nếu chưa có
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Bước 5: ghi file
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at the given path, relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)