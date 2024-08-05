import yt_dlp
import demucs.separate

def download_audio(link:str)->str:
  '''
  yt-dlp wrapper function that downloads the audio of a youtube video.

  Args:
    link: A string containing the link of the song you want.

  Returns:
    A string with the name of the downloaded file. In this uses the title of the video from
    YouTube. Then I use this name to run Demucs.
  '''
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    print(video_title)
    video.download(link)   
    print("Successfully Downloaded")

    return video_title+'.mp3'

route=download_audio('https://www.youtube.com/watch?v=HbzXVq9WgbY') # Hey, have a listen, you got this far... 

print(route)

# Run demucs to separate using the default values.
demucs.separate.main([route])
