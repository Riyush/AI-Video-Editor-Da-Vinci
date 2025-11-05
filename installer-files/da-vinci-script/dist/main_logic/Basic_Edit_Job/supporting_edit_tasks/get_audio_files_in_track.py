import os

# PATHS FOR FILE MANIPULATION, need to change in windows version of application
home_dir = os.path.expanduser("~")
WAV_DIR = os.path.join(home_dir, "Library", "Application Support", "GameTime", "wav_files")

def get_wav_files_for_track(timelineState, track_index_to_transcribe):
    """
    This function gets the wav files paths for all timeline items in the selected track
    This output list will instruct another function which wav files need to be transcribed
    """
    wav_paths = []
    #get a list of paths for the audio files that need to be transcribed
    timeline_items = timelineState.audio_tracks[track_index_to_transcribe]
    for timeline_item in timeline_items:
        underlying_media_file_name = timeline_item.GetMediaPoolItem().GetClipProperty()['File Name']
        base_name, ext = os.path.splitext(underlying_media_file_name)
        wav_filename = base_name + ".wav"
        wav_file_path = os.path.join(WAV_DIR, wav_filename)
        wav_paths.append(wav_file_path)
    
    return wav_paths