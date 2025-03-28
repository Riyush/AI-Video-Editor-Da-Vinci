import sys
import socket
import json
import os

def setup_socket():
    """
    Setup a unix socket on the user's computer. This socket creates a server-client
    architecture where the 2 components can communicate. I will have to think about
    the socket file path carefully
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    socket_path = f"/tmp/gaminghighlights_{os.getpid()}.sock"  # Unique per process
    if os.path.exists(socket_path):
       os.remove(socket_path)
    try:
        sock.bind(socket_path)
        sock.listen(1)
    except socket.error as e:
        print(f"Socket setup failed: {e}")
        raise
    return sock


def listen_for_requests(socket, media_pool):
    """
    After creating a socket, setup a loop to indefinitely listen for new requests
    from the GUI. These requests are user commands indicating how they want a video edited.

    Args:
        socket: The Unix socket object from setup_socket().
        media_pool: Resolve MediaPool object for timeline actions (temporary arg).
    """

    print("Listening for UI connection...")
    try:
        conn, _ = socket.accept()
        with conn:
            print("Connected to GUI")
            while True:
                raw_data = conn.recv(1024).decode()
                if not raw_data:  # GUI disconnected
                    break
                try:
                    data = json.loads(raw_data)
                    print(f"Received payload: {data}")
                    # Here we need code to process the payload
                    response = {"status": "received", "payload": data}
                    conn.send(json.dumps(response).encode())
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON from GUI: {e}")
                    conn.send(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())
            
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        socket.close()
        print("Script exiting...")
