from .GUI_Communication.socket import setup_socket,listen_for_requests

# Temporary Resolve setup - move to separate file later
#resolve = app.GetResolve()
fusion_obj = fusion.Fusion()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

mediaPool = projectManager.GetCurrentProject().GetMediaPool()
timeline = project.GetCurrentTimeline()

if __name__ == "__main__":
    socket = setup_socket()
    listen_for_requests(socket, mediaPool)