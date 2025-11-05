import os

# PATHS FOR FILE MANIPULATION, need to change in windows version of application
home_dir = os.path.expanduser("~")
WAV_DIR = os.path.join(home_dir, "Library", "Application Support", "GameTime", "wav_files")
TXT_DIR = os.path.join(home_dir, "Library", "Application Support", "GameTime", "transcripts")

def add_captions(add_captions_option, timelineState, resolve, fusion):
    """
    Function to add captions to a timeline

    Args:
    add_captions_option: [str]: can be either "Key Moments" or "All Dialogue"
    resolve: resolve object
    timelineState: wrapper for the timeline object which allows easier timeline manipulation
    fusion: fusion object
    
    """
    pass
    # I have all transcript info for each media pool item's raw wav file

    # Now, I need to detect when the speech occurs within the media pool item, so that
    # I know when to apply captions in the fusion composition.

