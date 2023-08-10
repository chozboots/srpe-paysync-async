# standard
import os

# dev
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


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

# Set the target directory
target_directory = os.environ.get("LOCAL_PATH")

# Print the file structure for the directory
print_directory_contents(target_directory)
