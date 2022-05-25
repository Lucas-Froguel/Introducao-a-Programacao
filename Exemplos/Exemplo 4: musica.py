import numpy as np
from scipy.io.wavfile import write
import simpleaudio as sa
import time
from pydub import AudioSegment
import random
import matplotlib.pyplot as plt


samplerate = 44100  # Frequecy in Hz


def get_wave(freq, duration=0.5):
    '''
    Function takes the "frequecy" and "time_duration" for a wave
    as the input and returns a "numpy array" of values at all points
    in time
    '''

    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)

    return wave


def get_piano_notes():
    '''
    Returns a dict object for all the piano
    note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']
    base_freq = 261.63  # Frequency of Note C4

    note_freqs = {octave[i]: base_freq * pow(2, (i / 12)) for i in range(len(octave))}
    note_freqs[''] = 0.0  # silent note

    return note_freqs


def get_song_data(music):
    '''
    Function to concatenate all the waves (notes)
    '''
    song = []
    for note in music:
        notes = note["notes"]
        if len(notes) == 1:
            wave = get_note_wave(notes)
        else:
            wave = get_chord_wave(notes)
        note["wave"] = wave
    return music


def get_note_wave(note):
    note_freqs = get_piano_notes()
    wave = get_wave(note_freqs[note])
    return wave


def get_chord_wave(notes):
    wave = None
    piano = get_piano_notes()
    for i in notes:
        if wave is not None:
            wave += get_wave(piano[i])
            continue
        wave = get_wave(piano[i])

    return wave


def play_song(song):
    for note in song:
        # Start playback
        play_obj = sa.play_buffer(note["wave"].astype(np.int16), 1, 2, samplerate)
        time.sleep(note["time"])

        # Wait for playback to finish before exiting
    play_obj.wait_done()


def save_song(song, name="twinkle"):
    waves = [note["wave"] for note in song]
    song = np.concatenate(waves)
    write(f'{name}.wav', samplerate, song.astype(np.int16))


def convert_wav_mp3(name):
    sound = AudioSegment.from_wav(f'{name}.wav')

    sound.export(f'{name}.mp3', format='mp3')


def generate_random_song(length=100, maximum_chord=3):
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']
    prob = [1, 0.1, 0.8, 0.1, 0.1, 0.7, 0.1, 0.6, 0.1, 0.5, 0.1, 0.4]
    prob = np.array(prob)
    prob = prob / np.sum(prob)
    song = []
    for i in range(length):
        num_notes = random.randint(1, maximum_chord+1)
        notes = random.choices(population=octave, weights=prob, k=num_notes)
        notes = "".join(notes)
        dt = random.random() / 3
        note = {"notes": notes, "time": dt}
        song.append(note)

    return song


def plot_song(song):
    waves = [note["wave"] for note in song]
    ranges = [range(100*i, 100*(i+1)) for i in range(len(waves))]
    for i in range(len(waves)):
        plt.plot(ranges[i], waves[i][0:int(44100/440)], "-r")
    plt.show()


def logistic_map(n=1000, r=4, x0=0.4):
    mapp = np.zeros(n)
    mapp[0] = x0
    for i in range(1, len(mapp)):
        mapp[i] = mapp[i-1]*r*(1-mapp[i-1])
    return mapp


def generate_chaotic_song(n=1000, base_freq=500, x0=0.4):
    song = []
    mapp = logistic_map(n, x0=x0)
    for val in mapp:
        freq = val * base_freq
        wave = get_wave(freq)
        dt = random.random() / 3
        note = {"wave": wave, "time": dt}
        song.append(note)
    return song



#music_notes = 'C-C-G-G-A-A-G--F-F-E-E-D-D-C--G-G-F-F-E-E-D--G-G-F-F-E-E-D--C-C-G-G-A-A-G--F-F-E-E-D-D-C'
#sinfonia = "E-E-F-G--G-F-E-D--C-C-D-E--E-D-D---E-E-F-G--G-F-E-D--C-C-D-E--D-C-C---D-D-E-C--D-E-F-E-C--D-E-F-E-D--C-D-G---D-D-E-C--D-E-F-E-C--D-E-F-E-D--C-D-G---E-E-F-G--G-F-E-D--C-C-D-E--D-C-C"
#song = get_song_data(sinfonia)


#song = generate_random_song(maximum_chord=1)
#song = get_song_data(song)

song = generate_chaotic_song(100, x0=0.34234243)

#plot_song(song)
name = "chaotic_song3"
play_song(song)
save_song(song, name=name)
convert_wav_mp3(name)


