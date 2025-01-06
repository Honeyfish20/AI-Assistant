import os

def get_python_files(path):
    python_files_dict = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                python_files_dict[file] = os.path.join(root, file)
    return python_files_dict

def read_python_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {e}"

def save_python_code(file_path, python_code):
    try:
        with open(file_path, 'w') as file:
            file.write(python_code)
        return f"Python code saved to {file_path} successfully."
    except Exception as e:
        return f"An error occurred while saving the Python code: {e}"