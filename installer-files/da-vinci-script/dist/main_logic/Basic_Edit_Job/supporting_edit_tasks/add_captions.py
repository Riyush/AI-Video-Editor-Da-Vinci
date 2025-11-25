import os
from Basic_Edit_Job.supporting_edit_tasks.add_magiczoom_to_timestamps import convert_frame_to_timecode
def add_captions(transcript_dict, track, timelineState, resolve, fusion):
    """
    Function to add captions to a timeline

    Args:
    transcript_dict: dictionary mapping media pool items on the track to a complex 
    dictionary of transcripts:
    {
    "media_pool_item_1": {words transcript_dict}
    "media_pool_item_2": {words transcript_dict}
    }
    track: The specific track index whose timeline items we want to add captions to
    timelineState: wrapper for the timeline object which allows easier timeline manipulation
    fusion: fusion object
    
    """
    try:
        fps = timelineState.timeline.GetSetting('timelineFrameRate')
        # iterate through audio items on the specified track
        for timeline_item in timelineState.audio_tracks[track]:

            item_fps = timeline_item.GetMediaPoolItem().GetClipProperty()['FPS']
            #First, move the playhead to the starting position of the current audio timeline item
            timeline_item_start_frame = timeline_item.GetStart()
            start_timecode = convert_frame_to_timecode(timeline_item_start_frame, fps)
            timelineState.timeline.SetCurrentTimecode(start_timecode)
            resolve.OpenPage("fusion")
            comp = fusion.GetCurrentComp()

        #Process to add captions
            #First, get the first word that occurs in the timeline item
            true_start_frame = timeline_item.GetSourceStartFrame()
            end_frame = timeline_item.GetSourceEndFrame()
            print(f"start frame: {true_start_frame}")
            start_second = true_start_frame / item_fps
            end_second = end_frame / item_fps

            # Iterate through words until the we get to the first word that occurs
            # after the start second of the timeline item
            # save a reference to that word within the transcription dictionary to word_index
            name = os.path.splitext(timeline_item.GetName())[0] 

            captions_list = get_captions_per_frame(transcript_dict[name]["words"], start_second, end_second, item_fps)
            print(captions_list)
            #Now, we know the index of the first and last word for our captions

            comp.CurrentTime = 0
            # First setup the text node and merge node in the node tree
            mediaOut = comp.FindTool("MediaOut1")
            previous_node = mediaOut.FindMainInput(1).GetConnectedOutput().GetTool()

            text_node = comp.AddTool("TextPlus", True, 3, 0)
            merge_node = comp.AddTool("Merge", True, 3, 1)

            merge_node.ConnectInput("Foreground", text_node.Output)
            merge_node.ConnectInput("Background", previous_node.Output)

            mediaOut.Input = merge_node.Output


            #Move the text to the bottom of the screen
            text_node.Center = (0.5, 0.1)

            #Apply BezierSpline modifier to create keyframes
            text_node.AddModifier("StyledText", "BezierSpline")

            # Get the StyledText Input of the text node so I can modify the actual display text
            inputList = text_node.GetInputList()
            for index, input in inputList.items():
                if input.ID ==  "StyledText":
                    styled_text_input = input
                    break
            
            #Now, i need to iterate through the captions list and apply the captions

            for caption_frame in captions_list:
                caption = caption_frame['Caption_String']
                start_frame = caption_frame['start_frame']
                end_frame = caption_frame['end_frame']


                #styled_text_input[start_frame - 1] = ""
                styled_text_input[start_frame - true_start_frame] = caption
                styled_text_input[end_frame - true_start_frame] = caption
                #styled_text_input[end_frame + 1] = ""

            #Return back to Cut page
            resolve.OpenPage("cut")
    except Exception as e:
        print(f"Error: {e}")

def get_captions_per_frame(words, start_second, end_second, fps, 
    max_words= 6,
    max_duration = 5.0,
    min_duration = 0.8,
    max_chars = 70,):
    """
    Convert a list of word dicts (with 'word', 'start', 'end') into a list of
    caption-frame dicts:
      {"Caption_String": str, 
      "start_frame": int, 
      "end_frame": int}

    words: list of dictionaries with schema: {"word": str, "start": float, "end": float}
    (timestamps are in seconds relative to the original file)
    start_second, end_second: clip boundaries (seconds)
    fps: frames per second for conversion
    The goal is to get information for each consecutive caption frame to create using fusion api
    """
    captions = []
    n = len(words)
    if n == 0:
        return captions
        
    # Find the index of the first word that starts >= start_second
    start_idx = 0
    for i, w in enumerate(words):
        if w.get("start", 0) >= start_second:
            start_idx = i
            break
        # if last word still before start_second, start_idx should be n (no words)
        if i == n - 1 and w.get("start", 0) < start_second:
            return captions

    i = start_idx
    last_caption_end_time = start_second  # to prevent overlaps; start at clip start

    while i < n:
        # Skip words that start >= end_second (outside clip)
        if words[i].get("start", 0) >= end_second:
            break

        caption_words = []
        caption_start_time = max(words[i].get("start", 0), start_second)
        caption_end_time = caption_start_time

        # Accumulate words until any stop condition triggers
        j = i
        while j < n:
            w = words[j]
            w_start = w.get("start", 0)
            w_end = w.get("end", w_start)

            # Stop if this next word begins at/after the clip end
            if w_start >= end_second:
                break

            # GAP CHECK — do not attach this word if there's a time gap
            if j - 1 >= i and w['start'] != words[j-1]['end']:
                break

            # tentative new end if we include this word
            tentative_end = min(w_end, end_second)
            tentative_duration = tentative_end - caption_start_time

            # Build tentative caption text to evaluate length
            tentative_text = " ".join([wd["word"] for wd in caption_words] + [w["word"]])
            tentative_chars = len(tentative_text)

            # Stop conditions
            if (len(caption_words) + 1) > max_words:
                break

            if tentative_duration > max_duration:
                break

            if tentative_chars > max_chars and len(caption_words) > 0:
                break

            # ACCEPT WORD
            caption_words.append(w)
            caption_end_time = tentative_end
            j += 1

            # PUNCTUATION CHECK — end caption AFTER this word
            if w["word"][-1] in ['.', ',', '!', '?']:
                break

        # If no words were added (rare), move one word forward to avoid infinite loop
        if not caption_words:
            i += 1
            continue

        # Ensure minimum display duration
        display_duration = caption_end_time - caption_start_time
        if display_duration < min_duration:
            # extend end time (clamped by clip end) to satisfy min_duration
            caption_end_time = min(caption_start_time + min_duration, end_second)

        # Avoid overlapping previous caption: ensure start >= last_caption_end_time
        if caption_start_time < last_caption_end_time:
            caption_start_time = last_caption_end_time
            if caption_end_time <= caption_start_time:
                caption_end_time = caption_start_time + min_duration

        # Convert seconds to frames (rounding to nearest frame)
        start_frame = int(round(caption_start_time * fps))
        end_frame = int(round(caption_end_time * fps))
        if end_frame <= start_frame:
            end_frame = start_frame + 1  # ensure at least 1 frame length

        caption_text = " ".join([w["word"] for w in caption_words]).strip()

        captions.append({
            "Caption_String": caption_text,
            "start_frame": start_frame,
            "end_frame": end_frame
        })

        last_caption_end_time = caption_end_time

        # Next iteration starts at the next word after j-1
        i = j

    return captions