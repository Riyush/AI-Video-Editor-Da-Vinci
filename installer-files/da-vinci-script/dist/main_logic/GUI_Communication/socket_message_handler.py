from Basic_Edit_Job.high_level_edit_function import execute_basic_edit_part_1

def message_handler(data, resolve):
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
            print("here")
            response = {}
            response["type"] = "GUI_Startup_Success"
            response["status"] = "success"
            response["payload"] = {}
        case "Basic-Edit-Job":
            # The socket has received a request to do a basic edit job with user
            # specified configurations. Execute the high level function part 1 which 
            # does the first subtasks associated with a Basic Edit Job
            # It sends a response to the GUI triggering the GUI to do subtasks that
            # the script envrionment can't do alone. 
            configurations = data["params"]

            response_status, response_message, media_file_paths_dict = execute_basic_edit_part_1(configurations, resolve)
            # any error we get is caught and returned to the GUI instead of killing the 
            # GUI-Socket Connection
            response = {}
            response["type"] = "Started_Edit_Job"
            response["status"] = response_status
            response["payload"] = {"message": response_message, "Media_File_Paths": media_file_paths_dict}
            
        case _:
            response = {}
            response["type"] = "ERROR"
            response["status"] = "Failure"
            response["payload"] = {"Error": "Invalid Message sent via Socket"}

    return response