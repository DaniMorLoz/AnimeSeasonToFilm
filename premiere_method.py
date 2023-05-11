import pymiere
from pymiere import wrappers
from os import path

def colocarycortar(videolist,frameList,openingDuration):
    project_opened, sequence_active = wrappers.check_active_sequence(crash=False)
    if not project_opened:
        raise ValueError("please open a project")
    project = pymiere.objects.app.project
    sequences = wrappers.list_sequences()
    project.openSequence(sequences[0].sequenceID)
    project.activeSequence = sequences[0]

    #añadir videos
    for i, video in enumerate(videolist):
        videolist[i] = path.abspath("Episodios/"+video)
    success = project.importFiles(videolist,suppressUI=True,targetBin=project.getInsertionBin(),importAsNumberedStills=False)
    #meterlos en la secuencia
    videos = project.rootItem.findItemsMatchingMediaPath(path.abspath("Episodios"),ignoreSubclips=False)
    fps = 1/(float(project.activeSequence.timebase)/wrappers.TICKS_PER_SECONDS)
    currenttime = 0
    currentframe = 0
    for i, video in enumerate(videos):
        project.activeSequence.videoTracks[0].insertClip(video,currenttime)
        clip = wrappers.list_video(project.activeSequence)[-1]
        audioclip = project.activeSequence.audioTracks[0].clips[-1]
        openingFrames = int(openingDuration*fps)
        nextframe = currentframe + int(float(frameList[i][1]))-int(float(frameList[i][0]))-openingFrames
        wrappers.edit_clip(clip, currentframe, nextframe, int(float(frameList[i][0]))+openingFrames, int(float(frameList[i][1])), fps=fps)
        wrappers.edit_clip(audioclip, currentframe, nextframe, int(float(frameList[i][0]))+openingFrames, int(float(frameList[i][1])), fps=fps)
        currenttime = currenttime + (int(float(frameList[i][1]))-int(float(frameList[i][0]))-openingFrames)/fps
        currentframe = nextframe