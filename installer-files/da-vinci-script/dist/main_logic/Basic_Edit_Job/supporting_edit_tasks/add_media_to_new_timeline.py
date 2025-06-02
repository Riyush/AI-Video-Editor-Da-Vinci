

def addMediaToNewTimeline(mediaStorage, mediaPool, mediaFolderPath):
    # put clips in media pool, clips is a list of media pool items
    clips = mediaStorage.AddItemListToMediaPool([mediaFolderPath])
    # create a new timeline
    timeline = mediaPool.CreateEmptyTimeline("GameTime")
    if not timeline:
        raise Exception("Failed to create new timeline")
    
    # Sort by name
    clips = sorted(clips, key = lambda clip : clip.GetClipProperty("File Name"))

    # add clips to timeline, each function call returns timeline items
    for clip in clips:
        mediaPool.AppendToTimeline(clip)
    
    return timeline

