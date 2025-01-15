from pyo import *


class HarmonizerVoiceSynth:
    def __init__(self, mic_in, mic_pitch, mul=0):
        self.note = Notein(poly=10, scale=0, first=0, last=127)
        self.pitch = self.note["pitch"]
        self.velo = self.note["velocity"]
        self.adsr = MidiAdsr(self.note['velocity'], attack=.005, decay=0.005, sustain=1, release=0.1)

        mic_midi_note = 69 + 12 * Log2(mic_pitch / 440)
        self.harm_voice = Harmonizer(mic_in, transpo=(self.pitch-mic_midi_note), winsize=0.1) * self.adsr

        self.output = self.harm_voice * mul

    def out(self):
        '''
        send signal to audio output, return object
        '''
        self.output.out()
        return self

    def sig(self):
        '''
        return signal for future processing
        '''
        return self.output