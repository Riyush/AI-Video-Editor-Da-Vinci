import requests
import os
import wave
from pydub import AudioSegment
import re
from collections import defaultdict
import json
import sys

# Chunk length in milliseconds (30 seconds)
CHUNK_LENGTH_MS = 30 * 1000

# Need to update this for production environment in future
TRANSCRIPTION_ENDPOINT = "http://127.0.0.1:8000/api/audio_transcription/transcribe_audio_groq"

# PATHS FOR FILE MANIPULATION, need to change in windows version of application
home_dir = os.path.expanduser("~")
WAV_DIR_MAC = os.path.join(home_dir, "Library", "Application Support", "GameTime", "wav_files")
CHUNKED_WAV_DIR_MAC = os.path.join(home_dir, "Library", "Application Support", "GameTime", "chunked_wav_files")
TRANSCRIPTION_DIR_MAC = os.path.join(home_dir, "Library", "Application Support", "GameTime", "transcripts")
def get_transcriptions():
    """
    This function returns a dictionary mapping each media pool item to a transcript dictionary
    It assumes there are existing wav files in WAV_DIR. This function isolates the functionality
    of getting the transcripts from using that transcript to create captions on the timeline

    """
    # We ultimately want to create a mapping of media_pool_item_name to that item's transcript dictionary
    transcriptions = {}

    try:
        # Get a list of all wav files to be transcribed
        for wav_file_path in os.listdir(CHUNKED_WAV_DIR_MAC):
            #print(f"WAV file: {wav_file_path}")
            # Construct the full path to the entry
            wav_path = os.path.join(CHUNKED_WAV_DIR_MAC, wav_file_path)
            #transcribe the wav file
            #Remember, the transcript_dict for one wav file is a complex dictionary
            # with file metadata and a mapping of transcript words to timestamps
            transcript_dict = transcribe_wav_file(wav_path)
            #append transcription to mapping of audio file to 
            # Split the filename into (base, extension)
            base_media_file_name, ext = os.path.splitext(wav_file_path)
            transcriptions[base_media_file_name] = transcript_dict
        
        #print("Transcribed files:", list(transcriptions.keys()))

        transcriptions = merge_all_transcriptions(transcriptions)
        #print(f"Merged Transcript: \n {transcriptions["5. It's_a_bitt_too_much"]}")
        
        return transcriptions

    except Exception as e:
        print(f"Top-level error in get_transcriptions(): {e}")
        return None

def transcribe_wav_file(wav_path):
    """
    Helper function that produces a trasncript of a wav file
    This function simply sends a request to a specific endpoint on my django server
    with the wav file data. The backend server actually conducts the transcription 
    because it requires my openai API key. This function recieves the text of the 
    transcription and writes the transcript to a text file in the User's 
    Application Support/GameTime/transcripts directory

    Args:
        wav_path [str]: Path to the wav audio file to be transcribed

    Returns:
    output_txt_file_path [str]: Path to the outputted transcript
    """

    # Create logic to send the wav file to the endpoint in a readable manner
    try:
        with open(wav_path, "rb") as f:
            files = {"file": (os.path.basename(wav_path), f, "audio/wav")}
            response = requests.post(TRANSCRIPTION_ENDPOINT, files=files)
    except Exception as e:
        #print(f"[FATAL] Could not send {wav_path} to server: {e}")
        return None

    if response.status_code == 200:
        try:
            #print(response.json().get("transcript", ""))
            return response.json().get("transcript", "")
        except Exception as e:
            #print(f"[ERROR] JSON parsing failed for {wav_path}: {e}")
            return None
    else:
        failed_file = os.path.basename(wav_path)
        try:
            error_json = response.json()
            error_message = error_json.get("error", "")
        except Exception:
            error_message = response.text  # Fallback if HTML/plain

        #print(f"Failed file: {failed_file}")
        #print(f"Failed to get transcription: {error_message}")
        return None

def merge_all_transcriptions(transcriptions):
    """
    Recombine chunked transcriptions into single transcripts per original file.

    transcriptions: dict mapping chunked filenames to their transcript dicts.
    Returns: dict mapping base filenames to merged transcript dicts.
    """

    # Step 1: Group chunk keys by base file name
    grouped = defaultdict(list)
    pattern = re.compile(r"(.+)_Gametime_(\d+)$")  # capture base file and chunk number

    for key in transcriptions.keys():
        match = pattern.match(key)
        if match:
            base_file, chunk_num = match.groups()
            grouped[base_file].append((int(chunk_num), key))
        else:
            # Handle keys that don't match the expected pattern
            pass
            #print(f"Warning: key '{key}' does not match expected pattern")

    merged_transcriptions = {}

    # Step 2: Merge chunks for each base file
    for base_file, chunks in grouped.items():
        # Sort by chunk number
        chunks.sort(key=lambda x: x[0])

        merged = {
            "text": "",
            "task": None,
            "language": None,
            "duration": 0,
            "words": [],
            "segments": None,
            "x_groq": None
        }

        for chunk_num, key in chunks:
            chunk = transcriptions[key]

            # Concatenate text
            merged["text"] += chunk.get("text", "")

            # Copy other fields from the first chunk
            if merged["task"] is None:
                merged["task"] = chunk.get("task")
            if merged["language"] is None:
                merged["language"] = chunk.get("language")
            if merged["segments"] is None:
                merged["segments"] = chunk.get("segments")
            if merged["x_groq"] is None:
                merged["x_groq"] = chunk.get("x_groq")

            # Adjust word timestamps
            time_offset = (chunk_num - 1) * 30  # 30 seconds per chunk
            for word in chunk.get("words", []):
                adjusted_word = word.copy()
                adjusted_word["start"] += time_offset
                adjusted_word["end"] += time_offset
                merged["words"].append(adjusted_word)

            # Sum durations
            merged["duration"] += chunk.get("duration", 0)

        merged_transcriptions[base_file] = merged

    return merged_transcriptions

def split_wav_into_chunks(input_path, output_dir=CHUNKED_WAV_DIR_MAC, slice_length_ms=CHUNK_LENGTH_MS):
    """
    Splits a .wav file specified by input_path into fixed-length slices and saves them with a
    naming pattern: <base>_Gametime_<index>.wav
    Currently I convert wav files into 30 second slices and save the slices as their own wav files
    If a wav file doesn't need to be sliced, the name still gchanges to the pattern.
    If a wav file needs to be chunked, then create the chunked wav files and delete the original wav file
    """

    filename = os.path.basename(input_path)
    base_name, ext = os.path.splitext(filename)

    if ext.lower() != ".wav":
        #print(f"Skipping non-wav file: {filename}")
        return

    # Load audio
    try:
        audio = AudioSegment.from_wav(input_path)
    except Exception as e:
        #print(f"❌ Failed to load {filename}: {e}")
        return
    # Get Duration
    duration_ms = len(audio)
    if duration_ms == 0:
        #print(f"⚠️ Skipping empty file: {filename}")
        return
    
    # Number of chunks (round up)
    num_chunks = (duration_ms + slice_length_ms - 1) // slice_length_ms

    #print(f"✅ Splitting {duration_ms/1000:.1f} second wav file: {filename} into {num_chunks} parts. ")
    # Chunking Logic, get start and end of 30 sec interval. 
    # Chunk the interval and create a new filename for the new chunked wav file. 
    for i in range(num_chunks):
        start_ms = i * slice_length_ms
        end_ms = min(start_ms + slice_length_ms, duration_ms)
        chunk = audio[start_ms:end_ms]
        chunk_filename = f"{base_name}_Gametime_{i+1}.wav"
        chunk_path = os.path.join(output_dir, chunk_filename)

        try:
            chunk.export(chunk_path, format="wav")
            #print(f"   → Created {chunk_filename}")
        except Exception as e:
            pass
            #print(f"❌ Error exporting {chunk_filename}: {e}")

def split_select_wav_files(wav_files_path_list):
    """
    Loops the throught the wav files in the path list and splits those wav files
    into 30 second chunks. This way, they are small enough to reliably be sent to the
    transcription API. The chunked files need to be put in a new folder for easy processing

    wav_files_path_list: list[str], each str is the absolute path to the wav file
    """
    # First, create Chunked Wav Dir if it doesn't exist
    os.makedirs(CHUNKED_WAV_DIR_MAC, exist_ok=True)

    for file_path in wav_files_path_list:
        if file_path.lower().endswith(".wav"):
            # Skip files that already match the Gametime chunk pattern
            if "_Gametime_" in file_path:
                continue
            split_wav_into_chunks(file_path)
    

def validate_wav(path):
    """
    Helper Function to validate any wav files that get uploaded
    """
    try:
        with wave.open(path, "rb") as wf:
            channels = wf.getnchannels()
            framerate = wf.getframerate()
            nframes = wf.getnframes()
            duration = nframes / float(framerate)
            size = os.path.getsize(path)
        return {
            "valid": True,
            "channels": channels,
            "framerate": framerate,
            "frames": nframes,
            "duration": duration,
            "size": size
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}

def save_transcripts_to_file(merged_transcriptions):
    try:
        os.makedirs(TRANSCRIPTION_DIR_MAC, exist_ok=True)
        output_path = os.path.join(TRANSCRIPTION_DIR_MAC, "merged_transcriptions.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(merged_transcriptions, f, indent=2) 
        
        print("success")
    except Exception as e:
        print(f" Failed to save transcripts: {e}")


if __name__ == "__main__":
    #For now, create the wav files list
    # List all files (not folders) in the directory
    # Read entire stdin as a single string
    json_input = sys.stdin.read().strip()

    wav_paths_list = json.loads(json_input)

    if not isinstance(wav_paths_list, list):
        raise ValueError("Expected list of wav file paths")
    
    split_select_wav_files(wav_paths_list)
    merged_transcripts = get_transcriptions()
    save_transcripts_to_file(merged_transcripts)