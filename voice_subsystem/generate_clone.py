from espnet_onnx import Text2Speech
import kaldiio
import time
import kaldiio
import subprocess
import sys

inputs = {"text": sys.argv[1], "x_dir": "/home/raffelm/capstone/Capstone/voice_subsystem/xvector/", "save_dir": "/home/raffelm/capstone/Capstone/voice_subsystem/wav/"}
fs = 16000
text2speech = Text2Speech(model_dir="/home/raffelm/capstone/Capstone/voice_subsystem/models/", use_quantized=False)
device = "cpu"

p = subprocess.Popen([sys.executable, './generate_embedding.py'])
                      
spembs = {k: v for k, v in kaldiio.load_ark(inputs["x_dir"] + "xvector.ark")}['0'][0]

start = time.time()
output_dict = text2speech(inputs["text"], spembs=spembs)
rtf = (time.time() - start) / (len(output_dict["wav"]) / fs)
print(f"RTF = {rtf:5f}")

#let us listen to generated samples
from IPython.display import Audio
audio = Audio(output_dict["wav"], rate=fs)
with open(inputs["save_dir"] + 'voiceOutput.wav', 'wb') as f:
    f.write(audio.data)

    
