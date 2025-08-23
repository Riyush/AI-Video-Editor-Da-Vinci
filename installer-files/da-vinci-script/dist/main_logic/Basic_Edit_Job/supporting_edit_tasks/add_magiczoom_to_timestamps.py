import random


def convert_frame_to_timecode(frame_num, fps):
    """Convert absolute frame number to a timecode string HH:MM:SS:FF"""

    frames_in_an_hour = 60 * 60 * fps
    hours = frame_num // frames_in_an_hour
    remaining_frames = frame_num % frames_in_an_hour

    frames_in_a_min = 60 * fps
    mins = remaining_frames // frames_in_a_min
    remaining_frames = remaining_frames % frames_in_a_min

    frames_in_a_sec = fps
    secs = remaining_frames // frames_in_a_sec
    frames = remaining_frames % frames_in_a_sec

    return f"{hours:02}:{mins:02}:{secs:02}:{frames:02}"


def get_cut_frames(timelineState):
    """
    Helper function that tracks all cuts between timeline items.
    Return a dictionary of video track to list of frames. Each frames is a break in the track.
    {1: [30, 700]
     2: [25]
     ...
     }
    """
    cut_timecodes_dict = {}
    for trackindex, timeline_items in timelineState.video_tracks.items():
        breaks = []
        for vid_item in timeline_items:
            frame_end = vid_item.GetEnd()
            fps = timelineState.timeline.GetSetting("timelineFrameRate")
            #timecode_end = convert_frame_to_timecode(frame_end, fps)
            breaks.append(frame_end)

        cut_timecodes_dict[trackindex] = breaks

def implement_magic_zoom_in_at_timestamp(timeline, resolve, fusion, start_frame, fps, is_zoom_in):
    """
    Function to implement a magic zoom in or zoom out at a specific start frame on the timeline

    Args:
        timeline: timeline object in scripting env
        resolve: resolve object in scriptin env
        fusion: fusion object in scripting env
        start_frame [int]: the frame on the timeline that magic zoom will start
        fps [float]: timeline frame rate, we get the composition frame rate seperately in the function body
        is_zoom_in [boolean]: True indicates a zoom in, False indicates a zoom out
    """
    #instantiate all possible keyframe lists
    keyframes_24_fps = [1,1.00107, 1.004278, 1.009607, 1.017037, 1.026535, 1.03806, 1.051564, 1.066987, 1.084265, 1.12, 1.168, 1.236, 1.31, 1.36, 1.402, 1.433013, 1.448436, 1.46193, 1.473465, 1.482963, 1.49039, 1.495722, 1.49893, 1.5]
    keyframes_30_fps = [1, 1.001370, 1.005463, 1.012236, 1.021614, 1.033494, 1.047746, 1.064214, 1.082717, 1.103054, 1.125, 1.148316, 1.172746, 1.198022, 1.223868, 1.25, 1.276132, 1.301978, 1.327254, 1.351684, 1.375, 1.396946, 1.417283, 1.435786, 1.452254, 1.466506, 1.478386, 1.487764, 1.494537, 1.498630, 1.5]
    keyframes_60_fps = [1,1.000343, 1.001370, 1.003078, 1.005463, 1.008519, 1.012236, 1.016605, 1.021614, 1.027248, 1.033494, 1.040332, 1.047746, 1.055714, 1.064214, 1.073223, 1.082717, 1.092670, 1.103054, 1.113840, 1.125, 1.136502, 1.148316, 1.160408, 1.172746, 1.185295, 1.198022, 1.210891, 1.223868, 1.236916, 1.25, 1.263084, 1.276132, 1.289109, 1.301978, 1.314705, 1.327254, 1.339592, 1.351684, 1.363498, 1.375, 1.386160, 1.396946, 1.407330, 1.417283, 1.426777, 1.435786, 1.444286, 1.452254, 1.459668, 1.466506, 1.472752, 1.478386, 1.483395, 1.487764, 1.491481, 1.494537, 1.496922, 1.498630, 1.499657, 1.5]

    #Get to the start frame where we want to implement the magic zoom on the timeline
    start_timecode = convert_frame_to_timecode(start_frame, fps)
    timeline.SetCurrentTimecode(start_timecode)

    #Get the composition frame rate, composition object, and enter the fusion page
    current_video_item = timeline.GetCurrentVideoItem()
    resolve.OpenPage("fusion")
    composition_frame_rate = current_video_item.GetMediaPoolItem().GetClipProperty()["FPS"]
    comp = fusion.GetCurrentComp()

    # Based on comp frame rate, choose a list of keyframe zoom values
    match composition_frame_rate:
        case 24.0:
            keyframe_values = keyframes_24_fps
        case 30.0:
            keyframe_values = keyframes_30_fps
        case 60.0:
            keyframe_values = keyframes_60_fps
        case _:
            keyframe_values = keyframes_30_fps

    #Find existing media in vs out nodes
    mediaIn = comp.FindTool("MediaIn1")
    mediaOut = comp.FindTool("MediaOut1")

    # case where we add a new transform node
    if comp.FindTool("Transform1") == None:
        transform_node = comp.AddTool("Transform", True, 1.1)
        transform_node.Input = mediaIn.Output
        mediaOut.Input = transform_node.Output

        #Get the size input from the Transform node
        inputList = transform_node.GetInputList()
        
        for index, input in inputList.items():
            if input.ID == "Size":
                Size_input = input
                break
        
        #Add the Bezier Spline modifier to the Size input 
        transform_node.AddModifier(Size_input.ID, "BezierSpline")

    #Case where we use an existing transform node
    else:
        transform_node = comp.FindTool("Transform1")
        # assume the existing transform node is already connected

        #Get the size input which already has a bezier spline if already edited
        inputList = transform_node.GetInputList()

        for index, input in inputList.items():
            if input.ID == "Size":
                Size_input = input
                break
        
    # Our procedure for determining magic zoom-in timestamps makes it to where we don't
    # edit existing keyframes on the transform node

    #Now, use the keyframe values and the composition FPS to implement the magic zoom

    magic_zoom_in_start_frame = int(comp.CurrentTime)
    
    #if we are doing a zoom out, reverse the keyframe list
    if not is_zoom_in:
        keyframe_values.reverse()

    keyframe_index = 0

    for frame in range(magic_zoom_in_start_frame, magic_zoom_in_start_frame + len(keyframe_values)):
        comp.CurrentTime = frame
        Size_input[frame] = keyframe_values[keyframe_index]

        keyframe_index +=1


def determine_magic_zoom_timestamps(timelineState, pacing, resolve, fusion):

    fps = timelineState.timeline.GetSetting("timelineFrameRate")
    cut_timecodes_dict = get_cut_frames(timelineState)
    print("FLAG 1")
    print(cut_timecodes_dict)
    print("Flag 2")
    # VERY IMPORTANT: For, now I will only implement magic zooms on media in the V1 video track
    # In the future, we can try to implement magic zooms on all video tracks at the same timecodes

    # fast pace = 1 zoom roughly every 10 second interval
    # normal pace = 1 zoom roughly every 20 second interval
    # calm pace = 1 zoom roughly every 30 second interval
    match pacing:
        case "calm":
            interval = 10
        case "normal":
            interval = 20
        case "Fast":
            interval = 30

    # Get timeline start and end time in secs
    timeline_end_frame = timelineState.timeline.GetEndFrame()
    timeline_end_in_secs = timeline_end_frame // fps
    timeline_start_frame = timelineState.timeline.GetStartFrame()
    timeline_start_in_secs = timeline_start_frame // fps

    #initialize the start of the timeline as the first zoom in candidate
    current_interval_start = timeline_start_frame
    cuts_in_first_track = cut_timecodes_dict[1]
    nearest_upcoming_cut_index = 0
    retries = 0     # when a candidate fails, try 3 more times max, if not, move to next interval

    END_Flag = False #when, a candidate frame becomes outside the timeline, we trigger the end flag
                     # and break out of the entire loop

    print("F")
    while current_interval_start < timeline_end_frame:

        #Check Retries counter to potentially move up the current interval start 10 seconds
        if retries == 4:
            current_interval_start += (interval * fps)
            retries = 0

        #Determine a zoom in point
        start_of_zoom_in_candidate = random.random.uniform(current_interval_start, current_interval_start + (interval * fps))
        # Steps to check if zoom in candidate is too close to the nearest cut

        
        # first, move the cut index to ensure the nearest cut is to the right of the candidate
        while start_of_zoom_in_candidate > cuts_in_first_track[nearest_upcoming_cut_index]:
            nearest_upcoming_cut_index += 1
            if nearest_upcoming_cut_index >= len(cuts_in_first_track):
                # In this case, our candidate frame is outside the timeline and we are done
                # carry the end flag to break out of the entire loop that implements magic zooms
                END_Flag = True
                break

        if END_Flag:
            break

        # Note, cuts_in_first_track_contains the last frame of the timeline, so it never exceeds max frame

        # Check that the candidate frame isn't too close to a cut making a magic zoom impossible
        if start_of_zoom_in_candidate + (1.5 * fps) > cuts_in_first_track[nearest_upcoming_cut_index]:
            retries +=1
            continue

        # Now, we know our candidate is a valid zoom in start point
        # Implement the zoom in at this point
        implement_magic_zoom_in_at_timestamp(timelineState.timeline, resolve, fusion, start_of_zoom_in_candidate, fps, True)

        #Now, we need to determine a magic zoom out point after the zoom in

        #Implement the magic zoom out at the determined magic zoom outstart point, 
        #note this zoom out could occur on a new timeline item within a new composition

        #Finally move the current interval starting point to the right for the next magic zoom
        # Note, the start point should be start of zoom out + 1.5 secs + (0.5 * interval)

        #placeholder for testing
        current_interval_start += (interval * fps)