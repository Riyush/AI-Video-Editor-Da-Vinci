import subprocess
import os
import sys

# This is the main file that will run the main_logic code in /Library/Application Support/Gametime
# The user will only see GameTime.py and it will simple python function call to the
# main_logic which will have direct access to the Da Vinci Resolve objects.

# This is the path to the main_logic directory on the user's computer
logic_path = os.path.join("/Library", "Application Support", "GameTime", "main_logic")

# Add your tool's logic path to sys.path
if logic_path not in sys.path:
    sys.path.append(logic_path)

from script import run_tool

# Get the DaVinci Resolve scripting object
resolve = resolve
fusion = fusion

# Run main logic which is in Application Support
# We can easily interface with resolve using the resolve object when needed
if __name__ == "__main__":
    run_tool(resolve, fusion)
    