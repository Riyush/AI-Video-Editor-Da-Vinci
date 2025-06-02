import sys
import socket
import json
import os
import tempfile

from .socket_message_handler import message_handler

def setup_socket():
    """
    Setup a unix socket on the user's computer. This socket creates a server-client
    architecture where the 2 components can communicate. I will have to think about
    the socket file path carefully
    """
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    # Set the socket to non-blocking mode FOR NOW keep it blocking
    #server_socket.setblocking(True)

    socket_path = f"/tmp/gaminghighlights_{os.getpid()}.sock"  # Unique per process
    pid = os.getpid()
    #Cleanup an existing socket file
    if os.path.exists(socket_path):
        try:
            os.remove(socket_path)
        except OSError as e:
            print(f"Warning: Could not remove existing socket file: {e}")
    try:
        path_location = record_socket_path(socket_path, pid)
        server_socket.bind(socket_path)
        server_socket.listen(1)
    except socket.error as e:
        print(f"Socket setup failed: {e}")
        raise
    return server_socket, path_location

def record_socket_path(socket_path, pid):
    # Try to create record ipc_config file in Application Support
    config_dir = "/Library/Application Support/GameTime"
    if os.access(config_dir, os.W_OK):
        config_path = os.path.join(config_dir, "ipc_config.json")
    # Instead create it in /tmp
    else:
        config_dir = "/tmp"
        config_path = os.path.join(config_dir, "ipc_config.json")

    os.makedirs(config_dir, exist_ok=True)  # Now we make sure the chosen dir exists
    print(config_path)
    with open(config_path, "w") as f:
        json.dump({"socket_path": socket_path, "pid": pid}, f)

    return config_path

def listen_for_requests(sock, path_location, resolve):
    """
    After creating a socket, setup a loop to indefinitely listen for new requests
    from the GUI. These requests are user commands indicating how they want a video edited.

    Args:
        socket [socket.socket]: The Unix socket object from setup_socket().
        path_location [string]: Location of the ipc_config.json used to clean up code
    """

    try:
        print("Waiting for GUI Connection")
        # This line says: “I, the script (server), have created a Unix socket 
        # and I'm now waiting for a client (GUI) to connect to it.”
        conn, _ = sock.accept()
        with conn:
            # GUI client is connected
            while True:
                print("Listening for GUI Messages...")
                raw_data = conn.recv(1024).decode()
                if not raw_data:  # GUI disconnected
                    # If this block triggers, the GUI has closed, so we can safely delete .sock and ipc.config files
                    cleanup_socket_files(path_location)
                    break
                try:
                    # Get data which should be in the form of a dictionary
                    data = json.loads(raw_data)
                    print(f'data received: {data}')
                    # Pass the data which should be a dictionary to the message handler
                    response = message_handler(data, resolve)
                    print(f'response to send: {response}')
                    # Send a response back to the GUI once message is processed
                    conn.send((json.dumps(response) + '\n').encode('utf-8'))

                except json.JSONDecodeError as e:
                    print(f"Invalid JSON from GUI: {e}")
                    conn.send(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())
            
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        sock.close()
        print("Script exiting...")

# Code to delete lingering files upon termination of the script
def cleanup_socket_files(config_path):
    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                socket_path = config.get("socket_path")

                if socket_path and os.path.exists(socket_path):
                    try:
                        os.remove(socket_path)
                        print(f"Removed socket file: {socket_path}")
                    except OSError as e:
                        print(f"Failed to remove socket file: {e}")

            try:
                os.remove(config_path)
                print(f"Removed config file: {config_path}")
            except OSError as e:
                print(f"Failed to remove config file: {e}")
        else:
            print("No config file found. Nothing to clean up.")

    except Exception as e:
        print(f"Error during cleanup: {e}")