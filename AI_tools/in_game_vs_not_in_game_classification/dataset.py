from torch.utils.data import Dataset
from transformers import VideoMAEImageProcessor
import cv2
import torch
import os

#This class simply collects all files in a folder as a dataset.
# Transform is set to none because we do preprocessing in another file
# We simply collect the preprocessed video files into this dataset object
class GameDataset(Dataset):
    def __init__(self, 
                 directory, 
                 clip_duration: int = 5, 
                 fps: int = 30,
                 increment: int = 1, # used to only select a subset of frames
                 transform=None,
                 model_architecture = "Masked AutoEncoder"
                 ):
        """
        directory: path to either 'train' or 'test' folder
        transform: optional transform function for preprocessing frames

        Label Map:
        {   
            0: not in game
            1: in game
        }
        """
        super().__init__()
        self.transform = transform
        self.increment = increment
        self.clip_duration = clip_duration
        self.fps = fps
        self.model_architecture = model_architecture

        # get a list of file paths for the video clips
        self.directory = directory

        self.video_files = [
            os.path.join(directory, f) 
            for f in os.listdir(directory) 
            if f.endswith(".mp4")
        ]
    def __len__(self):
        return len(self.video_files)

    def __getitem__(self, index):
        video_path = self.video_files[index]
        label_str = os.path.basename(video_path).split("_")[0]
        label = 1 if label_str == "in" else 0  # crude string check for "in_game" vs "not_in_game"

        frames = self.load_video(video_path)     # [3, 150, 224, 224]

        if self.transform:
            frames = self.transform(frames)

        # based on corresponding model architecture, either return all 150 frames as one tensor
        # or split into groups of 16 frames for the Masked Autoencoder
        if self.model_architecture == "CNN":
            return frames, label
        
        clips = []
        stride = 16  # overlap; you can tune this
        for start in range(0, frames.shape[1] - 16 + 1, stride):
            clip = frames[:, start:start+16, :, :]  # [3, 16, 224, 224]
            clips.append(clip)

        # ✅ Skip if there are too few valid clips
        if len(clips) < 1:
            print(f"[Skipping] Not enough clips in: {video_path} (only {len(clips)} found)")
            # recursively get next index (wraps around with modulo)
            return self.__getitem__((index + 1) % len(self.video_files))

        clips = torch.stack(clips)  # [num_clips, 3, 16, 224, 224] # tensor splits 150 frames into 16 frame clips
        return clips, torch.tensor(label, dtype=torch.float32)
    
    def load_video(self, path):
        cap = cv2.VideoCapture(path)
        frames = []

        # only take a subset of frames based on increment, For example: every 2 frames 
        frame_num = 0
        
        while True:
            frame_num += 1
            if frame_num % self.increment != 0:
                continue
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            frame = cv2.resize(frame, (224, 224))   # just in case
            frame = torch.tensor(frame).permute(2, 0, 1)  # [H, W, C] -> [C, H, W]
            frames.append(frame)
        cap.release()

        if not frames:
            # Handle edge case: no frames were read
            empty_tensor = torch.zeros((1, 1, 224, 224))  # [C, T, H, W]
            return empty_tensor.float()


        video_tensor = torch.stack(frames, dim=1)  # [C, T, H, W] tensor

        # 🔹 Calculate target number of frames based on frame rate, clip duration, and increment
        target_frame_count = int(self.clip_duration * self.fps / self.increment)

        current_frame_count = video_tensor.shape[1]
        # add all black padding frames if video is shorter than expexted frame count
        if current_frame_count < target_frame_count:
            pad_count = target_frame_count - current_frame_count
            pad_tensor = torch.zeros((3, pad_count, 224, 224))  # [C, pad_T, H, W]
            video_tensor = torch.cat([video_tensor, pad_tensor], dim=1)
        # 🔸 Optionally crop if there are more than needed (not expected unless clips are too long)
        elif current_frame_count > target_frame_count:
            video_tensor = video_tensor[:, :target_frame_count, :, :]

        return video_tensor.float() / 255.0         # dividing by 255 normalizes the tensor values in the range [0,1]