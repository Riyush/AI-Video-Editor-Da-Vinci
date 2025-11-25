from Basic_Edit_Job.supporting_edit_tasks.timelineState import TimelineState;

def get_audio_track_count(resolve):
    """
    Simple helper function to get the total number of audio tracks on the timeline
    Returns the audio track count and a success or failure message
    """
    try:

        manager = resolve.GetProjectManager()
        proj = manager.GetCurrentProject()
        timeline = proj.GetCurrentTimeline()
        aud_tracks_count = timeline.GetTrackCount('audio')

        return aud_tracks_count
    
    except:
        # Any failure means there are 0 tracks
        return 0