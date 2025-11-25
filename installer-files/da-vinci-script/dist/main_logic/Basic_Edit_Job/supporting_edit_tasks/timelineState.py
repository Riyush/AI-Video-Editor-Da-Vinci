import os
import subprocess

class TimelineState():
    """ Class to capture information about the timeline easily
        I will store the timeline object itself.

        I will also store the timeline items in 2 dictionaries.
        The vid_tracks dictionary will have keys corresponding to the
        track index. The value will be a list of timeline items on that track
        {video_track_index: [timeline_items]}
        """
    def __init__(self, timeline):
        self.timeline = timeline
        
        vid_tracks_count = timeline.GetTrackCount('video')
        aud_tracks_count = timeline.GetTrackCount('audio')
        self.vid_tracks_count = vid_tracks_count
        self.aud_tracks_count = aud_tracks_count

        #store video timeline item information in a dictionary 
        video_tracks = {}
        for index in range(1, vid_tracks_count + 1):
            video_tracks[index] = timeline.GetItemListInTrack('video', index)
    
        # each item in the dictionary represents an existing track on the timeline
        # the key is the track index as int and the value is a list of timelineItems on the track
        audio_tracks = {}
        for index in range(1, aud_tracks_count + 1):
            audio_tracks[index] = timeline.GetItemListInTrack('audio', index)

        self.video_tracks = video_tracks
        self.audio_tracks = audio_tracks

    def get_audio_item_file_paths(self):
        """ Get a list of file paths to all sources of audio for silence analysis
            The output structure of this call should resemble the structure of the timeline

            returns:
            audio_paths [dict]: dictionary of track index to list of file paths - matches audio_tracks structure
        """
        original_audio_file_paths = {}
        for key, values in self.audio_tracks.items():
            paths = []
            for timelineItem in values:
                #note, if an audio item and a video item come from the same media pool item, 
                # then calling GetMediaPoolItem on either will return the same MediaPoolItem object
                mediaPoolItem = timelineItem.GetMediaPoolItem()
                path = mediaPoolItem.GetClipProperty("File Path")
                paths.append(path)
            
            original_audio_file_paths[key] = paths

        return original_audio_file_paths

    def convert_media_to_wav(self, audio_file_paths_dict, output_dir = None, sample_rate=44100) -> dict:
        # I need to make the output dir, Gametime in the users/riyush/directory
        # This function needs to be done using GUI because it uses ffmpeg
        """
        Converts various media files (e.g., .mp4, .mov) to WAV format using ffmpeg.
    
        Parameters:
            audio_file_paths_dict: dict[int, list[str]] — input media file paths organized by track
            output_dir: str — destination folder for .wav files
            sample_rate: int — desired sample rate (default 44100Hz)
    
        Returns:
            dict[int, list[str]] — same structure but with paths to .wav files
        """
        # ONLY Works on MAC for now
        # create output directory for temporary wav files on user's home directory
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
                print(media_file)
                print(wav_file)
                # Convert using ffmpeg
                command = [
                    'ffmpeg',
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
    
    def add_markers_to_timestamps(self, silence_timestamps):
        """
        Iterate through all video tracks and add markers to each silence timestamps
        from the silence_timestamps dictionary. 

        Process: for each timeline item, match the item's name with the media file
        path key in silence timestamps, if its a match, that key's value is a 
        list of lists of all silence timestamps. 
        CONSIDER that each timestamp is in seconds and is within the context of the
        original media file's duration rather than place in timeline.
        Therefore, I convert the timestamp to a frameID based on frame rate of project
        and do: starting frame of timeline item + timestamp in frames to get the specific
        frame that I want to add the marker to.
        """
        print("hereherhehre")
        frame_rate = self.timeline.GetSetting("timelineFrameRate")

        for audio_track_index, audio_timeline_items in self.audio_tracks.items():
            for timeline_item in audio_timeline_items:
                # Now, I am at a specific item on teh timeline
                # match the item's name with the path name in timestamps to see
                # which timestamps need to be applied
                print()
                media_base_name = os.path.splitext(os.path.basename(timeline_item.GetName()))[0]
                print(media_base_name)
                
                flag = 0
                for media_file_path, timestamps_list in silence_timestamps[str(audio_track_index)].items():
                    # flag is used to not check excess media files
                    if flag == 1:
                        break
                    wav_base = media_file_path
                    print(wav_base)
                    if wav_base == media_base_name: # first check if correct, path, if not go to next path
                        print("PASSED!")
                        
                        flag = 1
                        if not timestamps_list: # now the strings match, check if there are any timestamps to mark
                            break      # If not, go to next timeline item
                        for timestamp_set in timestamps_list:
                            for timestamp in timestamp_set:
                                # convert timestamp in seconds to a specific frame
                                frameNum = round(timestamp * frame_rate)
                                print(frameNum)

                                # The addMarker method on timeline item adds the marker to the frame
                                # offset by the starting frame of the timeline item on the timelines
                                timeline_item.AddMarker(frameNum, "Blue", "MARK", "TEST", 1)

                                
                                
