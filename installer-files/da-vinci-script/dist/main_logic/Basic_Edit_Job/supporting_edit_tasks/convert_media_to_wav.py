import sys
import json
import os
import subprocess
import imageio_ffmpeg as ffmpeg

def convert_media_to_wav_files(audio_file_paths_dict, output_dir = None, sample_rate = 44100):
    if output_dir is None:
        home_dir = os.path.expanduser("~")
        output_dir = os.path.join(home_dir, "Library", "Application Support", "GameTime", "wav_files")

    os.makedirs(output_dir, exist_ok=True)

    wav_paths = {}
    for track, files in audio_file_paths_dict.items():
        wav_paths[track] = []
        for media_file in files:
            #create output filename
            base_name = os.path.splitext(os.path.basename(media_file))[0]
            wav_file = os.path.join(output_dir, f"{base_name}.wav")
            # Convert using ffmpeg
            command = [
                    ffmpeg.get_ffmpeg_exe(),
                    '-i', media_file,
                    '-vn',                   # no video
                    '-acodec', 'pcm_s16le',  # standard uncompressed WAV
                    '-ar', str(sample_rate), # sampling rate
                    '-ac', '1',              # mono
                    wav_file,
                    '-y'                     # overwrite
            ]

            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            wav_paths[track].append(wav_file)

    return wav_paths
    
if __name__ == "__main__":
    json_input = sys.stdin.read()

    audio_paths_dict = json.loads(json_input)
    result = convert_media_to_wav_files(audio_paths_dict)

    print(json.dumps(result))