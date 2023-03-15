import resampy
import torch
import kaldiio
import numpy as np
from speechbrain.dataio.preprocess import AudioNormalizer
from speechbrain.pretrained import EncoderClassifier
import sys

import kaldiio
import numpy as np
import torch

# TODO(nelson): The model inference can be moved into functon.
inputs = {"wav": "/nfs/stak/users/raffelm/hpc-share/capstone/testing/source.wav", "save_dir": "/nfs/stak/users/raffelm/hpc-share/capstone/testing/xvector/"}

device = 'cpu'
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb", run_opts={"device": device}
)
audio_norm = AudioNormalizer()


writer_utt = kaldiio.WriteHelper(
    "ark,scp:{0}/xvector.ark,{0}/xvector.scp".format(inputs["save_dir"])
)

in_sr, wav = kaldiio.load_mat(inputs["wav"])
fs=16000
if fs is not None and fs != in_sr:
    # FIXME(kamo): To use sox?
    wav = resampy.resample(
        wav.astype(np.float64), in_sr, fs, axis=0
    )
    wav = wav.astype(np.int16)
    in_sr = fs
    
# Amp Normalization -1 ~ 1
amax = np.amax(np.absolute(wav))
wav = wav.astype(np.float32) / amax
# Freq Norm
wav = audio_norm(torch.from_numpy(wav), in_sr).to(device)
# X-vector Embedding
embeds = classifier.encode_batch(wav).detach().cpu().numpy()[0]

writer_utt["0"] = embeds

writer_utt.close()
    