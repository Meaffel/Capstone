from espnet_onnx import Text2Speech
import resampy
import torch
import kaldiio
import numpy as np
import time
from speechbrain.dataio.preprocess import AudioNormalizer
from speechbrain.pretrained import EncoderClassifier
import sys


inputs = {"text": "Hello World", "wav": "/nfs/stak/users/raffelm/hpc-share/capstone/testing/source.wav"}
text2speech = Text2Speech(model_dir="/nfs/stak/users/raffelm/hpc-share/capstone/testing/models/", use_quantized=True)
device = "cpu"
fs = 16000
#Convert wav to flac 
in_sr, wav = kaldiio.load_mat(inputs["wav"])
print("Input wav file sampling rate: ", in_sr)

if fs is not None and fs != in_sr:
    # FIXME(kamo): To use sox?
    wav = resampy.resample(
        wav.astype(np.float64), in_sr, fs, axis=0
    )
    wav = wav.astype(np.int16)
    in_sr = fs

# speaker encoder
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb", run_opts={"device": device}
)

#Data Preprocessing
audio_norm = AudioNormalizer()
# Amp Normalization -1 ~ 1
amax = np.amax(np.absolute(wav))
wav = wav.astype(np.float32) / amax
# Freq Norm
wav = audio_norm(torch.from_numpy(wav), in_sr).to(device)
# X-vector Embedding created by speaker encoder
spembs = classifier.encode_batch(wav).detach().cpu().numpy()[0][0]

x = inputs["text"]

start = time.time()
# Process text input
output_dict = text2speech(x, spembs=spembs)
time_dif = time.time() - start
rtf = (time_dif) / (len(output_dict["wav"]) / in_sr)
print(f"RTF = {rtf:5f}")

#Convert output to .wav file
from IPython.display import Audio
audio = Audio(output_dict["wav"], rate=in_sr)
with open('/nfs/stak/users/raffelm/hpc-share/capstone/testing/test.wav', 'wb') as f:
    f.write(audio.data)