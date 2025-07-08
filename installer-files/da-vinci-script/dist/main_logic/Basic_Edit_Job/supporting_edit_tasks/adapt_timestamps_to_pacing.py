import os
"""
The user has the option between a calm, normal and fast pacing. 
To execute these differences in pacing, this function modifies the timestamps
to add some "buffer or padding silence" instead of just cutting all silences
directly which leads to fast pacing
"""

def adapt_timestamps_to_pacing(silence_timestamps, pacing_choice):
    """
    modify the silence timestamps to add buffer silence according to the pacing choice
    The rule is as follows: We want to preserve 1 second of silence in the 'calm' case.
    To do this, we move the timestamps for the start and stop of each silence
    closer to each other until we create the desired amount of silence
    Also, for the first and final silence in a media file's list of silences, no adjustment is made
    """
    print("adaptation")

    #first iterate through tracks on the timeline
    for track_index, track_items in silence_timestamps.items():
        for media_base_name, timestamps in track_items.items():
            for pair_index, pair in enumerate(timestamps):
                # skip the first and last pair
                if pair_index == 0 or pair_index == len(timestamps) - 1:
                    continue
                else:
                    match pacing_choice:
                        case 'calm':
                            pair[0] = pair[0] + 0.5
                            pair[1] = pair[1] - 0.5
                        case 'normal':
                            pair[0] = pair[0] + 0.25
                            pair[1] = pair[1] - 0.25
                        case 'Fast':
                            pass
                        case _:
                            raise ValueError("Invalid pacing choice")
                    
                    # if the silence is very short, then the adjustment causes the
                    # end to occur before the start. In this case, we keep the entire
                    # silence
                    if pair[0] > pair[1]:
                        del timestamps[pair_index]
    return silence_timestamps


"""

    for track_index, timestamps_dict in silence_timestamps.items():
        print(track_index)
        print(timestamps_dict)
        for media_file_wav_name, timestamps in timestamps_dict.items():
            #first, get the corresponding timeline_item
            items = timelineState.timeline.GetItemListInTrack("audio", int(track_index))
            for item in items:
                media_base_name = os.path.splitext(os.path.basename(item.GetName()))[0]
                wav_base_name = media_file_wav_name
                print(media_base_name)
                print(wav_base_name)
                if wav_base_name == media_base_name:
                    current_timeline_item = item
                    break

            # I use the name pair because each sublist contains 2 timestamps
            for pair_index, pair in enumerate(timestamps):
                #Beginning or end of clip is an edge case where we don't trim any silence
                # if the timestamp is the beginning or ending part of the clip,
                # it will always be cut out
                if pair[0] == 0.0:
                    continue

                if pair[1] +.2 >= current_timeline_item.GetSourceEndTime():
                    #In this case, we plan to cut any ending silences
                    continue
                match pacing_choice:

                    case "calm":
                        print("here")
                        # 1 second of silence is preserved
                        pair[0] = pair[0] + 0.5
                        pair[1] = pair[1] - 0.5
                        if pair[0] > pair[1]:
                            timestamps.pop(pair_index)
                    case "normal":
                        # 0.5 second of silence is preserved
                        pair[0] = pair[0] + 0.25
                        pair[1] = pair[1] - 0.25
                        if pair[0] > pair[1]:
                            timestamps.pop(pair_index)
                    case "Fast":
                        pass
                    case _:
                        raise ValueError("invalid pacing choice")

    return silence_timestamps
    """