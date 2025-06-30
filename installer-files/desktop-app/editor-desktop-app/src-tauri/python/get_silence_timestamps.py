# In this file, I create a function that analyzes the original media files
# for when silences occur. I expect a specific input structure which is the
# dictionary produced by my get_audio_item_file_paths() function

import sys
import json
import os
import librosa
import numpy as np

import soundfile
import numba
import scipy
import audioread
import resampy
import pooch

def detect_silences_in_media(audio_tracks:dict, silence_thresh_db: float = -10.0, min_silence_len_sec: float = 1.0) ->dict:
    """
    Detects silence periods in  media files across multiple audio tracks.
    Note, this expects .WAV files
    Parameters:
        audio_tracks: dict[str, list[str]] — dictionary where keys are track names and values are lists of .wav paths
        silence_thresh_db: float — RMS dB threshold below which is considered silence
        min_silence_len_sec: float — minimum duration for silence to count (in seconds)

    Returns:
        dict[str, dict[str, list[tuple[float, float]]]] — nested dict of track → file → list of silence (start, end)

    Sample dictionary structure
    {
    1: {
        "clip_001.wav": [(2.3, 5.6), (10.1, 12.0)],  # silence ranges in seconds
        "clip_002.wav": [(0.0, 3.5), ...]
        },
    2: ...
    }
    """
    silence_timestamps = {}
    for track, file_list in audio_tracks.items():

        # create a dictionary mapping audio file to silence timestamps
        silence_timestamps[track] = {}

        for wav_path in file_list:
            # load audio as waveform y and have no sampling rate?
            y, sr = librosa.load(wav_path, sr = None)

            frame_len = 2048
            hop_len = 512
            # Compute RMS and convert to Decibels, RMS is a measure of average volume
            rms = librosa.feature.rms(y=y, frame_length=frame_len, hop_length=hop_len)[0]
            db = librosa.amplitude_to_db(rms, ref=np.max)

            # Get time stamps for each frame
            times = librosa.frames_to_time(np.arange(len(db)), sr=sr, hop_length=hop_len)

            # Mark silent frames
            silence_flags = db < silence_thresh_db

            # Group consecutive silent frames into ranges
            silences = []
            start_time = None
            for i, is_silent in enumerate(silence_flags):
                current_time = times[i]
                if is_silent and start_time is None:
                    start_time = current_time
                elif not is_silent and start_time is not None:
                    end_time = current_time
                    if (end_time - start_time) >= min_silence_len_sec:
                        silences.append((start_time, end_time))
                    start_time = None
            # Handle trailing silence
            if start_time is not None and (times[-1] - start_time) >= min_silence_len_sec:
                silences.append((start_time, times[-1]))

            silence_timestamps[track][wav_path] = silences

    return silence_timestamps

if __name__ == "__main__":
    
    # Read entire stdin as a single string
    json_input = sys.stdin.read()
    
    # Parse it into a Python dict
    wav_paths_dict = json.loads(json_input)

    result = detect_silences_in_media(wav_paths_dict)

    print(json.dumps(result))