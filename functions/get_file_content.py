from config import READ_MAX_CHARS
import io
import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read content from a file by specifing it's filepath",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to a target file relative to the working directory. (you do not specify the working directory)",
                }
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

    common_path = os.path.commonpath([working_directory_abs, target_file])
    if common_path != working_directory_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if True == os.path.isdir(target_file):
        return f'Error: {target_file} is not a regular file: "{file_path}"'

    try:
        f = open(target_file, "r", encoding="utf-8")

        content = f.read(READ_MAX_CHARS)

        if f.read(1):
            content += (
                f'[...File "{file_path}" truncated at {READ_MAX_CHARS} characters]'
            )

    except Exception as t:
        return f"Error: Unexpected exception {t}"

    return content
