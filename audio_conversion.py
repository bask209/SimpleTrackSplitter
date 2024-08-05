# This is a simple script you can use to convert an audio format to another.
# As I've left it, it converts a m4a file to an mp3 file. Read more on pydub
# documentation: https://github.com/jiaaro/pydub

from pydub import AudioSegment

song_name="MySong.m4a"

audio=AudioSegment.from_file(song_name).export(f'{song_name}.mp3',format='mp3')