from GUI_Communication.socket import setup_socket,listen_for_requests
from GUI_Communication.open_GUI import launch_GUI

# Temporary Resolve setup - move to separate file later

#fusion_obj = fusion.Fusion()
#projectManager = resolve.GetProjectManager()
#project = projectManager.GetCurrentProject()

#mediaPool = projectManager.GetCurrentProject().GetMediaPool()
#timeline = project.GetCurrentTimeline()

if __name__ == "__main__":
    socket = setup_socket()     # Setup the unix socket for GUI to connect to
    #launch_GUI()                # This needs to be fixed to point to new GUI
    listen_for_requests(socket)
    