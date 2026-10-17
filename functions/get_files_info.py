import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "List files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                }
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_directory_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))

    common_path = os.path.commonpath([working_directory_abs, target_directory])
    if common_path != working_directory_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if False == os.path.isdir(target_directory):
        return f"Error: {target_directory} is not a directory"

    try:
        files_str = ""
        files_list = os.listdir(target_directory)
        for file_name in files_list:
            file_abs = os.path.join(target_directory, file_name)
            is_dir = str(os.path.isdir(file_abs))
            size = os.path.getsize(file_abs)
            files_str += f"- {file_name}: file_size={size} bytes, is_dir={is_dir}\n"

        return files_str
    except t:
        return f"Error: {t}"
