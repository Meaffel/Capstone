from espnet_onnx import Text2Speech
import kaldiio
import time
import kaldiio


inputs = {"text": "Aaugh", "x_dir": "/nfs/stak/users/raffelm/hpc-share/capstone/testing/xvector/", "save_dir": "/nfs/stak/users/raffelm/hpc-share/capstone/testing/"}
fs = 16000
text2speech = Text2Speech(model_dir="/nfs/stak/users/raffelm/hpc-share/capstone/testing/models/", use_quantized=False)
device = "cpu"

spembs = {k: v for k, v in kaldiio.load_ark(inputs["x_dir"] + "xvector.ark")}['0'][0]

start = time.time()
output_dict = text2speech(inputs["text"], spembs=spembs)
rtf = (time.time() - start) / (len(output_dict["wav"]) / fs)
print(f"RTF = {rtf:5f}")

#let us listen to generated samples
from IPython.display import Audio
audio = Audio(output_dict["wav"], rate=fs)
with open(inputs["save_dir"] + 'test.wav', 'wb') as f:
    f.write(audio.data)

    