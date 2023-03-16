#Spawning child process
import sys
import subprocess

#Recording audio
import pyaudio
import wave

from playsound import playsound



#Spawning child -----------------------------------------------------
def run(*popenargs, **kwargs):
    input = kwargs.pop("input", None)
    check = kwargs.pop("handle", False)

    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr

def run_child(filename, args):
    run_args = ["python", filename] + args
    run_return = run(run_args)
    print("Child successfully executed with run with returned values:")
    print("(retcode, stdout, stderr)")
    print(str(run_return))



#Recording auidio ---------------------------------------------------
def record_audio(time_sec):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = time_sec
    WAVE_OUTPUT_FILENAME = '/home/raffelm/capstone/Capstone/voice_subsystem/wav/voiceInput.wav'
    device_index = 2
    audio = pyaudio.PyAudio()

    print("Input device list: to be removed once setup")
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

    print("Enter device to record with: ")

    index = int(input())
    print("Starting recording on device: "+str(index))
    
    RATE = int(audio.get_device_info_by_index(index).get('defaultSampleRate'))
    
    print("Sample rate: " + str(RATE))

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = index,
                    frames_per_buffer=CHUNK)

    print ("recording started: recording for "+str(RECORD_SECONDS)+" seconds")
    Recordframes = []
 
    for i in range(0, int((RATE / CHUNK) * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)

    print ("recording stopped")
 
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()



#Playing auidio -----------------------------------------------------
def play_audio():
    chunk = 512
    #open a wav format music  
    #wav = wave.open(r"./cannery.wav","rb")  
    wav = wave.open(r"./source.wav","rb")  
    #instantiate PyAudio
    audio = pyaudio.PyAudio()  
    #open stream  
    stream = audio.open(format = audio.get_format_from_width(wav.getsampwidth()),  
                    channels = wav.getnchannels(),  
                    rate = wav.getframerate(),  
                    output = True)  
    #read data  
    data = wav.readframes(chunk)  

    #play stream  
    while data:
        stream.write(data)  
        data = wav.readframes(chunk)

    #stop stream
    stream.stop_stream()  
    stream.close()

    #close PyAudio  
    audio.terminate()
    
def play_audio2():
    playsound('/home/raffelm/capstone/Capstone/voice_subsystem/wav/voiceOutput.wav')
