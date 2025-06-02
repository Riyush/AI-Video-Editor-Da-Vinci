import subprocess
import os

PATH_TO_GUI_APP = "~/Library/Application Support/AI-Video-Editor/main_window"
expanded_path = os.path.expanduser(PATH_TO_GUI_APP)

# function to check if the application is already running 
def is_app_running(app_path):
    try:
        # List all running processes and search for the app path
        output = subprocess.check_output(["ps", "aux"], text=True)
        return app_path in output
    except Exception as e:
        print(f"Error checking if app is running: {e}")
        return False

def launch_GUI():
    if not is_app_running(expanded_path):
        subprocess.Popen([expanded_path])
    else:
        print("App is already running.")
