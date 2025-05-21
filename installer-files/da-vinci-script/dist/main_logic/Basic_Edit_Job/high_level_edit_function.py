

fusion_obj = fusion.Fusion()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

mediaPool = projectManager.GetCurrentProject().GetMediaPool()
timeline = project.GetCurrentTimeline()

def execute_basic_edit(edit_configurations, fusion_obj = fusion_obj, project_manager = projectManager, project = project, media_pool = mediaPool, timeline = timeline):
    print(edit_configurations["add_captions"])
    print(timeline.GetTrackCount("video"))
    print(timeline.GetItemListInTrack("video"))
