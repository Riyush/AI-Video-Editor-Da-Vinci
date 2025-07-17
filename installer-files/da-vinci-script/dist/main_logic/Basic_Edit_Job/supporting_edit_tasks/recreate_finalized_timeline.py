from Basic_Edit_Job.supporting_edit_tasks.timelineState import TimelineState
import os
"""
Once we have the adjusted timestamps and the existing state of the timeline,
we need to find a way to cut off the silences while preserving the timeline structure.
The most practical way to do this is to create a new timeline and add the relevant,
silence trimmed portions of each media clip 
to that new timeline by manipulating the in and out markers for each media clip
"""

def recreate_finalized_timeline(mediapool, timelineState, silence_timestamps):
    """
    Process: 
    Create new Timeline, 
    Look at the original timelineState, iterate through tracks and timeline items in order
    Determine which portions of each media pool item needs to be added to the timeline 
    by excluding portions that are marked as silence.
    For each portion of media pool item to be added, set the proper in and out markers,
    then add to the correct track on the new timeline.

    In effect, we are recreating the timeline state but excluding silences indicated by
    the timestamps using the In and Out Markers.
    """
    # new timeline starts with 1 video and audio track
    new_timeline = mediapool.CreateEmptyTimeline("GameTime - Rough Cut")

    # Set new timeline's frame rate to the previous timeline's frame rate
    # Might need to keep better track of the frame rate and set it by looking
    # at the frame rate of an media pool item at this point 
    prior_frame_rate = timelineState.timeline.GetSetting("timelineFrameRate")
    new_timeline_frame_rate = prior_frame_rate
    new_timeline.SetSetting("timelineFrameRate", prior_frame_rate)

    for track_index, audio_item_list in timelineState.audio_tracks.items():
        # video 1 and audio 1 already exist
        if track_index != 1:
            new_timeline.AddTrack("audio", {'index': track_index})
            # for now, assume all audio will have corresponding video on this video track
            new_timeline.AddTrack("video", {'index': track_index})

        # A parameter used to keep track of when the previous timeline item ended
        # The starting frame is 1 hour in seconds * project frame rate
        last_occupied_timeline_frame = 60 * 60 * new_timeline_frame_rate

        seperation_carry_flag = False
        seperation = 0
        previous_seperation = 0
        # anytime we append to the timeline, we have to first check for the carry flag
        # iterate through items in original timeline
        for aud_timeline_item in audio_item_list:
            # Determine if we there is dead space between the start of current timeline item and last occupied frame
            item_original_start_frame = aud_timeline_item.GetStart()

            seperation = item_original_start_frame - last_occupied_timeline_frame
            
            print(f'Seperation: {seperation}')
            #Get corresponding media pool item
            aud_media_pool_item = aud_timeline_item.GetMediaPoolItem()

            #Get Silence Timestamps for the item
            base_file_name = os.path.splitext(aud_timeline_item.GetName())[0]

            timestamps_for_item = silence_timestamps[str(track_index)][base_file_name]
            
            # Before iterating through each silence, check if the entire thing has no silence
            # This occurs when the timestamps_for_item list is completely empty
            if not timestamps_for_item:
                clip_info_dict = {"mediaPoolItem": aud_media_pool_item, "trackIndex": track_index}

                #Before appending here, check for leftover seperation indicated by carry flag
                if seperation_carry_flag and previous_seperation > 0:
                    record_frame = new_timeline.GetEndFrame() + seperation + previous_seperation
                    clip_info_dict["recordFrame"] = record_frame
                    #reset flags as all seperation has been used
                    seperation_carry_flag = False
                    seperation = 0
                    previous_seperation = 0

                mediapool.AppendToTimeline([clip_info_dict])
                # set new last occupied frame, remember its the end in the original timeline
                last_occupied_timeline_frame = aud_timeline_item.GetEnd()
                # Go to next media pool item 
                continue

            # iterate through each silence
            # For each silence pair, we want to add the non-silent portion of the media pool item 
            # occurring BEFORE the silence. The last silence is an edge case because we also have to add
            # the non-silent portion of the media occurring affter the silence. 

            # Set a variable for the start of the non-silence which carries over into
            # each subsequent loop iteration
            non_silence_start = 0.0
            for pair_index, pair in enumerate(timestamps_for_item):
                print(f'Pair Index: {pair_index}')
                silence_start = pair[0]
                silence_end = pair[1]

                non_silence_end = silence_start

                #Set In and Out Markers on the item's non silent portion to be added to timeline
                #Mark frames using the media pool items FPS property to convert timestamp to frame
                item_frame_rate = aud_media_pool_item.GetClipProperty('FPS')

                start_frame = round(non_silence_start * item_frame_rate)
                end_frame = round(non_silence_end * item_frame_rate)

                aud_media_pool_item.SetMarkInOut(start_frame, end_frame, type='audio')

                #Append the non-silent portion to the appropriate track
                # Note, this even works if the first silence timestamp occurs at 0.0           
                # because both the in and points become 0 and nothing gets appended

                #media type 2 is audio only
                # I have the option to specify a record frame which is the frame in the timeline
                # where the media pool item gets added. THIS MIGHT BE USEFUL for adding
                # video items after adding the audio adjusted to the silences
                # However, for the audio items, I leave this parameter blank because I just want
                # to append to the media pool item to the end of the track, as I am going sequentially
                clip_info_dict = {"mediaPoolItem": aud_media_pool_item, "startFrame": start_frame, "endFrame": end_frame, "trackIndex": track_index}

                # Seperation usually matters for the first non silence in the media pool item because 
                # seperation occurs between each item not within each item
                # However, there could be carry on seperation that we need to account for
                # We account for seperation by setting a record frame at the end of the timeline + seperation
                # The end of timeline is where the non silence normally would have appended, but
                # now we add the seperation that we found from the previous timeline item
                if pair_index == 0 and seperation !=0:
                    #WARNING: There is an edge cases where this doesn't work: if the first non silence is an empty range
                    # then, I'm not sure what happens
                    timeline_end_frame = new_timeline.GetEndFrame()
                    recordFrame = timeline_end_frame + seperation

                    #check for carry on seperation:
                    if seperation_carry_flag and previous_seperation > 0:

                        record_frame += previous_seperation
                        seperation_carry_flag = False
                        previous_seperation = 0

                    clip_info_dict["recordFrame"] = recordFrame

                if pair_index == 1:
                    print(f"TEST: {seperation_carry_flag}")
                #Before appending here, check for previous seperation
                if seperation_carry_flag and previous_seperation > 0:
                    print("Caught Previous Seperation")
                    timeline_end_frame = new_timeline.GetEndFrame()
                    record_frame = timeline_end_frame + previous_seperation
                    seperation_carry_flag = False
                    previous_seperation = 0

                    clip_info_dict["recordFrame"] = recordFrame



                print("Not the edge case")
                print(clip_info_dict)
                mediapool.AppendToTimeline([clip_info_dict])

                #check if this append didn't actually do anything because start frame >= end frame
                if start_frame >= end_frame and seperation > 0:
                    print("Need to add carry on!!")
                    # store the lost seperation for later append
                    seperation_carry_flag = True
                    previous_seperation = seperation
                    print(f"Previous Seperation to be considered: {previous_seperation}")
                
                
                # After appending, we need to move the start of the non-silence for the next non silence in the loop
                non_silence_start = silence_end

                #edge case for last non-silence of the media pool item
                if pair_index == len(timestamps_for_item) - 1:
                    end_frame = int(aud_media_pool_item.GetClipProperty("End"))
                    start_frame = round(non_silence_start * item_frame_rate)
                    if start_frame < end_frame:

                        clip_info_dict = {"mediaPoolItem": aud_media_pool_item, "startFrame": start_frame, "endFrame": end_frame, "trackIndex": track_index}
                        print("edge case ending")
                        print(clip_info_dict)
                        # before appending, check for carry flag:
                        if seperation_carry_flag and previous_seperation > 0:
                            clip_info_dict['recordFrame'] = new_timeline.GetEndFrame() + previous_seperation
                            seperation_carry_flag = False
                            previous_seperation = 0
                        mediapool.AppendToTimeline([clip_info_dict])

            #update last occupied frame for the next timeline item
            last_occupied_timeline_frame = aud_timeline_item.GetEnd()
        # Need to debug if this adds all the non-silence audio item portions properly

    return new_timeline




