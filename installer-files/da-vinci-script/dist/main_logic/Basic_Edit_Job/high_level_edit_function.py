from Basic_Edit_Job.supporting_edit_tasks.add_media_to_new_timeline import addMediaToNewTimeline

def execute_basic_edit(edit_configurations, resolve):

    # create the necessary objects to pass to support functions
    mediaStorage = resolve.GetMediaStorage()
    proj_manager = resolve.GetProjectManager()
    proj = proj_manager.GetCurrentProject()
    mediaPool = proj.GetMediaPool()
    
    #check if user has already added all media to the timeline:
    if edit_configurations['added_to_timeline'] =='true':
        timeline = proj.GetCurrentTimeline()
    # If not, create timeline and add clips assuming labeled order of clips
    else:
        mediaFolderPath = edit_configurations['clip_folder_path']
        print(f"Raw files: {mediaStorage.GetFileList(mediaFolderPath)}") # see the files from folder
        timeline = addMediaToNewTimeline(mediaStorage, mediaPool, mediaFolderPath)
        # see the media pool items
        print(f"Media Pool Items: {mediaPool.GetSelectedClips()}")
    
    # see the timeline objects
    print(timeline.GetTrackCount("video"))
    print(f"Timeline Items: {timeline.GetItemListInTrack('video', 1)}")

    # Now trim the timeline clips based on desired pacing from the user

    print(mediaPool.GetRootFolder())