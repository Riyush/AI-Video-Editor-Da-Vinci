from .GUI_Communication.socket import setup_socket,listen_for_requests

# Temporary Resolve setup - move to separate file later
resolve = app.GetResolve()
projectManager = resolve.GetProjectManager()
mediaPool = projectManager.GetCurrentProject().GetMediaPool()

if __name__ == "__main__":
    socket = setup_socket()
    listen_for_requests(socket, mediaPool)