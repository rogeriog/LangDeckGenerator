import wave
import sys
from pydub import AudioSegment
import soundfile as sf
import pyrubberband as pyrb
## based on code from: https://stackoverflow.com/users/2866150/lokesh-deshmukh

def ChangeAudioSpeed(mp3file : str, speed : float):
    """ this will rewrite mp3 file with update speed """
    sound = AudioSegment.from_mp3(mp3file)
    sound.export("tmp.wav", format="wav")
    y, sr = sf.read("tmp.wav")
    # Play back at extra low speed
    y_stretch = pyrb.time_stretch(y, sr, speed)
    # Play back extra low tones
    y_shift = pyrb.pitch_shift(y, sr, speed)
    sf.write("tmp_stretched.wav", y_stretch, sr, format='wav')

    sound = AudioSegment.from_wav("tmp_stretched.wav")
    mp3file=mp3file.split('.')[0]+"-"+str(speed)+".mp3"
    sound.export(mp3file, format="mp3")
    return mp3file

