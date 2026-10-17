import os
from pathlib import Path

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write a content to a file completely overriding it by specifing target filename and it's new content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to a target file relative to the working directory. (you do not specify the working directory)",
                },
                "content": {
                    "type": "string",
                    "description": "Content that will be written to specified file",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

    common_path = os.path.commonpath([working_directory_abs, target_file])
    if common_path != working_directory_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if True == os.path.isdir(target_file):
        return f'Error: Cannot write to "{target_file}" as it is a directory'

    try:
        directory = os.path.dirname(target_file)

        os.makedirs(directory, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as t:
        return f'Error: exception occured "{t}"'
