import youtube_dl
import sys
import random
import os
allformats = {'140': 'mp3 128k','141': 'mp3 256k','139': 'mp3 48', '17': 'gp3 144p', '36': 'gp3 240p', '5': 'flv', '43': 'webm', '18': 'mp4 360p', '22': 'mp4 720p'}

def search_video(url, output='audio', quiet=False):
    url = url.split("=")[-1]
    avaible={}
    avaible["bestaudio"]={"name":"Best AUDIO","url":"/download/{}/mp3-bestaudio".format(url)}
    avaible["audio"]={"name":"Normal AUDIO","url":"/download/{}/mp3-audio".format(url)}
    avaible["bestvideo"]={"name":"Best VIDEO","url":"/download/{}/mp4-bestvideo+bestaudio".format(url)}
    avaible["video"]={"name":"Normal VIDEO","url":"/download/{}/mp4-best".format(url)}

    return avaible


def download_source(url,type,id):
    url = "https://www.youtube.com/watch?v="+url
    print(id)
    if id == "bestaudio" or id == "audio":
        ydl_opts = {
            'outtmpl': 'database/music/%(title)s-%(upload_date)s-%(id)s.%(ext)s',
            'format': id+"/best",
            'ffmpeg_location':"paths/ffmpeg/",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }]}
    elif id == "bestvideo+bestaudio" or id == "best":
        ydl_opts = {
            'outtmpl': 'database/video/%(title)s-%(upload_date)s-%(id)s.%(ext)s',
            'format': id+"[ext=mp4]"+"/best"+"[ext=mp4]",
            'ffmpeg_location':"paths/ffmpeg/",
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                "preferedformat":"mp4"
                }]}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        result = ydl.extract_info(url, download=False)
        fn = ydl.prepare_filename(result)
        print(fn)
        #fn = ydl_opts["outtmpl"]
    if type == "mp4":
        name = os.path.splitext(fn)
        directory = fn
        if name[1] == ".mkv":
            videooutput = 'ffmpeg -i "./{}" -vcodec copy -acodec -f mp4 "{}"'.format(fn,name[0]+".mp4")
            os.system(videooutput)
            directory = name[0]+".mp4"
        if name[1] ==".webm":
            videooutput = 'ffmpeg -i "./{}" -f mp4 "{}"'.format(fn,name[0]+".mp4")
            os.system(videooutput)
            directory = name[0]+".mp4"
        if name[1] == ".mp4":
            directory = name[0]+".mp4"
        return directory
    if type == "mp3":
        name = os.path.splitext(fn)
        return str(name[0])+".mp3"


if __name__ == "__main__":
    pass
