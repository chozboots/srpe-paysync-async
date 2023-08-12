# standard
import os

os.mkdir('./app')

def print_directory_contents(path, indent=""):
    for child in os.listdir(path):
        child_path = os.path.join(path, child)
        if any([child == ".venv", child== ".git"]):
            continue
        if os.path.isdir(child_path):
            print(f"{indent}{child}/")
            print_directory_contents(child_path, indent + "  ")
        else:
            print(f"{indent}{child}")

# Print the file structure for the directory
print_directory_contents(os.getcwd())
