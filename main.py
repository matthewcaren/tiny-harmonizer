from pyo import *
from synth import HarmonizerVoiceSynth

if __name__ == "__main__": 
    inputs, outputs = pa_get_devices_infos()
    print('- Inputs:')
    for index in sorted(inputs.keys()):
        print('  Device index:', index)
        for key in ['name', 'default sr', 'latency']:
            print('    %s:' % key, inputs[index][key])
    print('- Outputs:')
    for index in sorted(outputs.keys()):
        print('  Device index:', index)
        for key in ['name', 'default sr', 'latency']:
            print('    %s:' % key, outputs[index][key])
            
    # setup   
    s = Server(sr=44100, buffersize=512, ichnls=1, nchnls=2)
    s.setMidiInputDevice(99)  # open all input devices.
    s.boot()

    # mic input
    mic = Input().play()*0.5
    mic_highpass = Biquadx(mic, freq=100, q=1, type=1, stages=4)

    mic_pitch = Yin(mic_highpass, tolerance=0.1, minfreq=80, maxfreq=800, cutoff=800, winsize=1024)
    freq = Tone(mic_pitch, freq=8)   # lowpass on pitch tracking

    harm_synth = HarmonizerVoiceSynth(mic_highpass, freq, mul=1.2).sig()
    mixed = Mix([harm_synth, mic_highpass], voices=1, mul=0.5)

    verb = STRev(mixed, revtime=2, cutoff=5000, bal=0.15).out()

    s.gui(locals())