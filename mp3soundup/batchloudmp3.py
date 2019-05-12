import os
import sys
import pathlib
from pydub import AudioSegment
from pydub.playback import play
from subprocess import call
import colorama
from colorama import Fore, Style
from colorama import init

# You need:
# Python3.6+
# https://ffmpeg.org/
# ref:
# https://stackoverflow.com/questions/43679631/python-how-to-change-audio-volume
# 

# If you converted a song from YouTubeToMP3 and looking to increase volume, 5 is good.
# Bandcamp ripper 7 is good

# You can edit these variables
isListen = True

# TODO: Do fadeout and value
isFadeOut = False
# must be positive non-zero-number
FadeOutValue = 2
# Specify if you have own path to ffmpeg or put "none" to use default (set by pydub)
ffmpegPath = ""

# End of edit

# Define variables, Please do not edit below unless you know what you are doing...
init() # colorama
path = os.getcwd()
if (not ffmpegPath):
    AudioSegment.converter = path + "\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffmpeg = path + "\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffprobe = path + "\\ffmpeg\\bin\\ffprobe.exe" 
else:
    AudioSegment.converter = ffmpegPath
    AudioSegment.ffmpeg = ffmpegPath
    AudioSegment.ffprobe = ffmpegPath

mp3path = path + "\input"
mp3output = path
music_files = []
music_filenames = []

volume_input = 1
# End of defined variables

# START DRIVER CODE

print("Starting batch mp3 edits. Hope you have song in input folder. All songs go to output folder.")
print("You can cycle through the next song using ctrl + c when", Fore.BLUE, "isListen", Style.RESET_ALL, "is true.")
volume_input = eval(input("Enter a positive or negative number to increase or decrease song volume: "))

# r=root, d=directories, f = files
# get each song path of .mp3
for r, d, f in os.walk(mp3path):
    for file in f:
        if '.mp3' in file:
            music_files.append(os.path.join(r, file))
            music_filenames.append(str(file).strip('.mp3'))

if (len(music_files) < 1):
    print("You have no songs in the input folder. Exiting...")
    sys.exit()

print("Editing ", len(music_files), " songs...")

# go through each song and song name
# Use ctrl + c to go through each song
# ref: https://www.saltycrane.com/blog/2008/04/how-to-use-pythons-enumerate-and-zip-to/
for c, (music, name) in enumerate(zip(music_files, music_filenames)):
    song = AudioSegment.from_mp3(music)
    adjust_song = song
    # change song by x dB
    if volume_input > 0 or volume_input < 0:
        adjust_song = song + volume_input
    if isListen:
        print("Now Playing: ", name)
        play(adjust_song)
    # let user know that was the last song to stop ctrl + c going
    if (len(music_files) == (c + 1)):
        print("Do not ctrl + c. That was the last song. Please wait...")
    # save the song to output folder
    # ref: https://computer.howstuffworks.com/mp32.htm
    adjust_song.export(path + "\\output\\" + str(name) + ".mp3", format="mp3", bitrate="320k")

print("*** done ***")
sys.exit()

# END OF DRIVER CODE