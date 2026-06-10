# limit the scope of directories and files that the LLM is able to view.
# Without this restriction, the LLM might run amok anywhere on the machine, reading sensitive files or overwriting important data. This is a very important step that we'll bake into every function the LLM can call.
import os
import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not target_dir.startswith(working_dir_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        contents = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            stat = os.stat(item_path)
            contents.append(
                f"- {item}: file_size={stat.st_size} bytes, is_dir={os.path.isdir(item_path)}"
            )
        return "\n".join(contents)

    except Exception as e:
        return f"Error: {e}"