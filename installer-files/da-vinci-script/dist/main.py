import subprocess
import os

# This is the main file that will run with access to the script executable
script_dir = os.path.dirname(os.path.abspath(__file__))
binary_path = os.path.join(script_dir, "script")

if __name__ == "__main__":
    print("Hello in console")
    subprocess.run([binary_path], check=True)