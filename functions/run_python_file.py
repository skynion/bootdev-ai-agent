import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_dir_path = os.path.abspath(working_directory)

        if os.path.commonpath([working_dir_path, full_path]) != working_dir_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = [sys.executable, full_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_dir_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""

        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"

        if result.stderr:
            output += f"STDERR:\n{result.stderr}"

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"

        if not result.stdout and not result.stderr:
            output += "No output produced"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file with optional command line arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command line arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
