from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def cutvideo(videoname,OpeningTimestamp,EndingTimestamp):
    audio = AudioFileClip("Episodios/"+videoname).subclip(OpeningTimestamp, EndingTimestamp)
    video_clip = VideoFileClip("Episodios/"+videoname).subclip(OpeningTimestamp, EndingTimestamp)
    video_clip = video_clip.set_audio(audio)
    return video_clip

def createVideo(lista,frameList,openingDuration,fps):
    clips = []
    for i, video in enumerate(lista):
        clips.append(cutvideo(video,frameList[i][0]*fps+openingDuration,frameList[i][1]*fps))
    final = concatenate_videoclips(clips)
    final.write_videofile("Output/"+"Temporada "+os.listdir("Episodios/")[0].split("_")[0]+".mp4",codec="libx264")
