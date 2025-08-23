from Basic_Edit_Job.supporting_edit_tasks.add_media_to_new_timeline import addMediaToNewTimeline
from Basic_Edit_Job.supporting_edit_tasks.timelineState import TimelineState
from Basic_Edit_Job.supporting_edit_tasks.adapt_timestamps_to_pacing import adapt_timestamps_to_pacing
from Basic_Edit_Job.supporting_edit_tasks.recreate_finalized_timeline import recreate_finalized_timeline
from Basic_Edit_Job.supporting_edit_tasks.add_magiczoom_to_timestamps import determine_magic_zoom_timestamps
#from Basic_Edit_Job.supporting_edit_tasks.detect_silences import detect_silences_in_media

def execute_basic_edit_part_1(edit_configurations, resolve):
    try:
        # create the necessary objects to pass to support functions
        mediaStorage = resolve.GetMediaStorage()
        proj_manager = resolve.GetProjectManager()
        proj = proj_manager.GetCurrentProject()
        mediaPool = proj.GetMediaPool()
        
        #check if user has already added all media to the timeline:
        if edit_configurations['added_to_timeline'] =='true':
            #need to add proper error handling if this line fails
            timeline = proj.GetCurrentTimeline()
        # If not, create timeline and add clips assuming labeled order of clips
        else:
            mediaFolderPath = edit_configurations['clip_folder_path']
            print(f"Raw files: {mediaStorage.GetFileList(mediaFolderPath)}") # see the files from folder

            #if we need to work with absolute file paths in the future, get them from GetFileList call
            timeline = addMediaToNewTimeline(mediaStorage, mediaPool, mediaFolderPath)

        # gain understanding of timeline structure by creating a timelineState object
        # the object stores the timeline and its items as dictionaries of track index to list of corresponding items
        timelineState = TimelineState(timeline)

        # Now trim the timeline clips based on desired pacing from the user
        # Note, we need an understanding of the overall timeline state and media pool state 
        # in the case that the user has a custom setup 
        
        #First, get a list of media file paths in a dictionary that resembles  timeline structure
        original_audio_file_paths = timelineState.get_audio_item_file_paths()
        print(f"PATHS to AUDIO FILES{original_audio_file_paths}")

        # send the audio file paths to the GUI since scriptenvironment doesn't
        # have access to external dependencies like ffpmeg
        # The GUI will get .wav files and get silence timestamps and send them back to the script


        # This completes this part of the function because now we need to asynchronously
        # wait for GUI to complete creation of .wav files and silence analysis.

        # The GUI will send a message with the silence timestamps back to the script
        # which will trigger part 2 of the editing process which is trimming the footage.

        #return status string, simple message, and audio_file_paths for the GUI to contine edit process
        return "success", f"Started Basic Edit, Please get .wav files and silence timestamps", original_audio_file_paths


    except Exception as e:
        # This block will catch any exception and return them to the socket
        # This way, errors are caught and returned to the GUI rather than kill the 
        # GUI - script connection entirely
        return "failure", f"An error occurred: {type(e).__name__} - {e}", {}
    
def execute_basic_edit_part_2(edit_configurations, silence_timestamps, resolve, fusion):

    try:
        # create the necessary objects to pass to support functions
        mediaStorage = resolve.GetMediaStorage()
        proj_manager = resolve.GetProjectManager()
        proj = proj_manager.GetCurrentProject()
        mediaPool = proj.GetMediaPool()

        timeline = proj.GetCurrentTimeline()
        timelineState = TimelineState(timeline)
        
        #Based on the user's preffered pacing, cut different durations of the silences

        remove_silences = edit_configurations["silence_removal"]
        pacing = edit_configurations["pacing_choice"]
        print(silence_timestamps)
        if remove_silences == 'true':
            match pacing:
                case "calm":
                    # 1 second of silence in each silence timestamp is preserved
                    final_silence_timestamps = adapt_timestamps_to_pacing(silence_timestamps, pacing)
                case "normal":
                    final_silence_timestamps = adapt_timestamps_to_pacing(silence_timestamps, pacing)
                case "Fast":
                    # no processing, just remove silences
                    final_silence_timestamps = adapt_timestamps_to_pacing(silence_timestamps, pacing)
                case _:
                    raise ValueError("invalid pacing choice")
            
            print(final_silence_timestamps)

            #add markers to the finalized timestamps
            #timelineState.add_markers_to_timestamps(final_silence_timestamps)

            # Function to create new timeline with silences deleted based on silence timestamps
            new_timeline = recreate_finalized_timeline(mediaPool, timelineState, final_silence_timestamps)

            # new timeline with silences trimmed off
            new_timelineState = TimelineState(new_timeline)

            print(timelineState.audio_tracks)
            print(new_timelineState.audio_tracks)

        # At this point, we've handled silence removal and the pacing option for the video
        # Now, we need to focus on Zoom Cuts and Transitions, adding captions and brightness

        #Procedure for adding all zoom cut based on pacing
        # The function randomly adds magic zoom animations at a rate of 1 every x seconds based on the pacing
        # In the future, we need a method to do a great job of deermining when to implement the zoom in
        print("START OF PROCESS")
        determine_magic_zoom_timestamps(new_timelineState, pacing, resolve, fusion)
        print("End of Process")

        return "success", "Completed Basic Edit", {}
    except Exception as e:
        # This block will catch any exception and return them to the socket
        # This way, errors are caught and returned to the GUI rather than kill the 
        # GUI - script connection entirely
        return "failure", f"An error occurred: {type(e).__name__} - {e}", {}
