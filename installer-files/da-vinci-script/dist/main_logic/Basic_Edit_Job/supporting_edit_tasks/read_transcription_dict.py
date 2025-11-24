import os
import json

home_dir = os.path.expanduser("~")
TRANSCRIPTS_PATH_MAC = os.path.join(home_dir, "Library", "Application Support", "GameTime", "transcripts", "merged_transcriptions.json")


def read_transcriptions_dict():
    with open(TRANSCRIPTS_PATH_MAC, "r") as f:
        contents = json.load(f)

    return contents