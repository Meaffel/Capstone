import sounddevice as sd
import soundfile as sf

def record_audio(time_sec):
    fs = 16000
    myrecording = sd.rec(int(time_sec*fs), samplerate=fs, channels=1, device=2)
    sd.wait()
    sf.write('wav/voiceInput.wav', myrecording, fs)

record_audio(10)
