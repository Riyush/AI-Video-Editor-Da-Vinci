import os
import cv2
# This file takes raw video and cuts it into 5 second long chunks ith consistent size and color
# Note, the audio is not preserved which needs to be worked out. 
def format_time(seconds):
    """Helper function to convert seconds to M:SS format"""
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins}:{secs:02d}"

def get_label_from_filename(filename):
    """Extract label from 6th character of filename"""
    base = os.path.basename(filename)
    if len(base) >= 6 and base[5].isdigit():
        digit = int(base[5])
        if digit in [1, 2, 3]:
            return "in_game"
        elif digit in [4, 5, 6]:
            return "not_in_game"
    return "unknown"


def preprocess_raw_clips(clip_duration, frame_increment, raw_footage_folder, to_grayscale, resize_dims=(224, 224)):
    """
    This function takes all the raw footage in a folder and converts it into 
    a collection of resized grayscale 5 second clips with a name specifying
    the collection of 5 frames. Use arguments to determine grayscale, frame increment,
    raw footage folder, 
    
    params:
        clip_duration [int]: expected duration of each sample clip
        frame_increment [int]: used to skip frames to test training capability
        raw_footage_folder [str]: path to raw footage folder
        to_grayscale [bool]: whether or not to convert the footage to grayscale
        resize_dims: Target dimensions (width, height) for each frame
    """
    for file in os.listdir(raw_footage_folder):
        if not file.lower().endswith((".mp4", ".mov", ".avi")):
            continue

        filepath = os.path.join(raw_footage_folder, file)
        cap = cv2.VideoCapture(filepath)

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps

        frames_per_clip = int(fps * clip_duration)
        step = frame_increment + 1

        base_name = os.path.splitext(file)[0]
        label = get_label_from_filename(base_name)

        clip_idx = 0
        current_frame = 0

        while current_frame + step < total_frames:
            frames = []
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

            for i in range(0, frames_per_clip, step):
                success, frame = cap.read()
                if not success:
                    break

                if to_grayscale:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

                frame = cv2.resize(frame, resize_dims)
                frames.append(frame)

            if len(frames) == 0:
                break

            start_sec = current_frame / fps
            end_sec = (current_frame + len(frames) * step) / fps

            start_str = format_time(start_sec)
            end_str = format_time(end_sec)

            clip_name = f"{label}_{base_name}_{start_str}-{end_str}.mp4"
            out_dir = os.path.join(raw_footage_folder, "processed")
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, clip_name)

            height, width = resize_dims[1], resize_dims[0]
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

            for frame in frames:
                out.write(frame)

            out.release()
            print(f"Saved: {clip_name}")
            current_frame += frames_per_clip

        cap.release()

preprocess_raw_clips(5, 0, "/Volumes/My Passport for Mac/Coding Projects/AI-Video-Editor-Da-Vinci/AI_tools/data/fortnite/raw_footage", True)