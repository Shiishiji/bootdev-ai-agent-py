import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a python script providing script filename and it's arguments. Defaults to scripts in working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to a python script file relative to the working directory. (you do not specify the working directory)",
                },
                "args": {"type": "array", "description": "List of script arguments"},
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

    common_path = os.path.commonpath([working_directory_abs, target_file])
    if common_path != working_directory_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if False == os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]

    if None != args:
        command.extend(args)

    try:
        result = subprocess.run(
            args=command,
            capture_output=True,
            text=True,
            cwd=working_directory_abs,
            timeout=30.0,
        )

        output = ""
        if 0 != result.returncode:
            output += f"Process exited with code {result.returncode}\n"

        hasStdOut = "" != result.stdout
        hasStdErr = "" != result.stderr

        if not hasStdOut and not hasStdErr:
            output += f"No output produced\n"
        else:
            if hasStdOut:
                output += f"STDOUT: {result.stdout}\n"
            if hasStdErr:
                output += f"STDERR: {result.stderr}\n"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"

    return f"Success"
