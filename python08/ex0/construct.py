import sys
import os
import site

#When in virtual environment, sys.prefix is relocated to the current virtual env
def is_virtual() -> bool:
    return sys.base_prefix != sys.prefix

def main() -> None:
    if is_virtual():
    #get the basename part of the prefix
        venv_name = os.path.basename(sys.prefix)
        package_path = site.getsitepackages()[0]
        print(
            "\nMATRIX STATUS: Welcome to the construct\n\n"
            f"Current Python: {sys.executable}\n"
            f"Virtual Environment: {venv_name}\n"
            f"Environment Path: {sys.prefix}\n\n"
            "SUCCESS: You're in an isolated environment!\n"
            "Safe to install packages without affecting\n"
            "the global system.\n\n"
            f"Package installation path:\n{package_path}"
        )
    else:
        print(
            "\nMATRIX STATUS: You're still plugged in\n\n"
            f"Current Python: {sys.executable}\n"
            "Virtual Environment: None detected\n\n"
            "WARNING: You're in the global environment!\n"
            "The machines can see everything you install.\n\n"
            "To enter the construct, run:\n"
            "python -m venv matrix_env\n"
            "source matrix_env/bin/activate # On Unix\n"
            "matrix_env\\Scripts\\activate # On Windows\n\n"
            "Then run this program again."
        )


if __name__ == "__main__":
    main()