from sys import byteorder
from array import array
from struct import pack
import select
import sys
import pyaudio
import wave
import os

__author__ = 'Emily Ahn and Elizabeth Hau'

''' *************************** utils.py ******************************
    This file allows users to record themselves using the microphone of
    their local computer and saves the recorded file as 'demo.wav' in 
    the data directory. Recording starts right after running the script
    and stops either if the user hits the 'Enter' key or is silent for 
    a long period of time (i.e. if continuous silence time > SILENT_THRESHOLD)
    sources: 
    1. http://stackoverflow.com/questions/892199/detect-record-audio-in-python
    2. http://stackoverflow.com/questions/292095/polling-the-keyboard-detect-a-keypress-in-python
    *******************************************************************
'''

THRESHOLD = 300  # threshold for when to "tag" something as silent
SILENT_THRESHOLD = 30  # threshold for when to stop recording
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 16000  # sampling rate
DATADIR = "data"


def heardEnter():
    "Returns 'True' if the 'Enter' key is pressed"
    i, o, e = select.select([sys.stdin], [], [], 0.0001)

    for s in i:
        if s == sys.stdin:
            input = sys.stdin.read(1)
            return True
    return False


def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i) > THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r


def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Stops recording when the silence count is over
    the SILENCE_THRESHOLD or when the 'Enter' key 
    is pressed

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
                    input=True, output=True,
                    frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False
    was_silent = False

    r = array('h')

    while 1:

        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
            was_silent = True

        elif not silent and not snd_started:
            snd_started = True

        # reset num_silent if was silent but now talking again
        elif not silent and was_silent:
            num_silent = 0
            was_silent = False

        # break if num_silence is over the threshold
        if snd_started and num_silent > SILENT_THRESHOLD:
            break

        # or break if enter key is pressed
        if heardEnter():
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


if __name__ == '__main__':
    print("*** please speak into the microphone ***\n")
    record_to_file(os.path.join(DATADIR, 'demo.wav'))
    print("\n*** done - result written to demo.wav in the data directory ***")
