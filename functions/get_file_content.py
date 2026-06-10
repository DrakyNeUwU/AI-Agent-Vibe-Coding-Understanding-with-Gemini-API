import os
from google.genai import types
MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Bước 2: check path traversal
        if not target_file.startswith(working_dir_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Bước 3: check có phải file không
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Bước 4: đọc file, tối đa MAX_CHARS ký tự
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            # Check xem file có bị truncate không
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file at the given path, relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)    
