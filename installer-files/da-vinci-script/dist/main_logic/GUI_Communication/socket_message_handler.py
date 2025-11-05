from Basic_Edit_Job.high_level_edit_function import execute_basic_edit_part_1, execute_basic_edit_part_2
from Basic_Edit_Job.supporting_edit_tasks.get_number_of_audio_tracks import get_audio_track_count

import json

def message_handler(data, resolve, fusion, state_dict):
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
            response["payload"] = {"message": response_message, "Media_File_Paths": media_file_paths_dict, }

            #update state_dict with configurations. This persists the user's edit preferences
            # for part 2 of the edit job
            state_dict["configurations"] = configurations
        
        case "Basic-Edit-Part-2-Get-Silence-Timestamps":
            silence_timestamps = data["params"]
            configurations = state_dict["configurations"]
            
            response_status, response_message, wav_paths_list = execute_basic_edit_part_2(configurations, silence_timestamps, resolve, fusion)

            # GUI matches on message 'type' key which we create here
            if response_status == "pending":
                response_type = "Need_Transcripts"      # NEED TO IMPLEMENT THIS CASE in receive_socket_message.rs
            else:
                response_type = "Completed_Basic_Edit_Job"
                
            response = {}
            response["type"] = response_type
            response["status"] = response_status
            response["payload"] = {"message": response_message, "wav_paths": wav_paths_list}

            print(response_type)
            # Need code here to delete the wav files in /Library/Application Support/GameTime/wav_files
        
        case "Basic-Edit-Part-3-Apply-Captions":
            
            # Receive the dictionary mapping media base paths to their transcription dictionaries
            # "5. It's_a_bitt_too_much : {}
            merged_transcripts = json.loads(data["params"])

            # Now I need to write the high level function that takes the transcripts and creates captions

        case "Get_Number_Of_Audio_Tracks":
           #Case for when the GUI wants to know how many audio tracks are on the timeline  
            num_audio_tracks = get_audio_track_count(resolve)

            response = {}
            response["type"] = "Get_Number_Of_Audio_Tracks"
            response["status"] = "success"
            response["payload"] = {"message": "Obtained number of audio tracks on timeline", "Audio_Tracks_Count": num_audio_tracks}

        case _:
            response = {}
            response["type"] = "ERROR"
            response["status"] = "Failure"
            response["payload"] = {"Error": "Invalid Message sent via Socket"}

    return response