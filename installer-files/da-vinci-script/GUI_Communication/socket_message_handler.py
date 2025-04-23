
def message_handler(data):
    """This function receives the json data from the socket, evaluates the 
        'type' key and does some behavior to handle the message.
        Becuase all messages are standardized to json, this function exploits that
        structure to handle all unique messages.
        
        Args:
            data [dict]: contents of the data sent from the GUI via the socket
            
        Returns:
            response [dict]: message to be sent back to GUI after data is processed"""
    message_type = data['type']
    match message_type:
        case "GUI_Startup":
            # The script receives a message from GUI. If the GUI receives a response via this case,
            # then the GUI knows the script is running, the socket is running, and the GUI can 
            # prompt the user to login
            response = {}
            response["type"] = "GUI_Startup_Success"
            response["status"] = "success"
            response["payload"] = {}
        case _:
            response = {}
            response["type"] = "ERROR"
            response["status"] = "Failure"
            response["payload"] = {"Error": "Invalid Message sent via Socket"}
    
    return response