import subprocess

# Define the paths to the Python files you want to open
file_path1 = r"C:\Users\Omar\Desktop\ParaFI\Radius.py"
file_path2 = r"C:\Users\Omar\Desktop\ParaFI\Website\app.py"

def run_python_script_non_blocking(path):
    try:
        # Starts the Python script and doesn't wait for it to finish
        subprocess.Popen(['python', path])
        print(f"Started {path} successfully")
    except Exception as e:
        print(f"Failed to start {path}: {e}")

run_python_script_non_blocking(file_path1)
run_python_script_non_blocking(file_path2)
