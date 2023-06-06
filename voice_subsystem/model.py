from espnet_onnx import Text2Speech
import kaldiio
import time
import kaldiio
import subprocess
import sys
import resampy
import torch
import kaldiio
import numpy as np
from speechbrain.dataio.preprocess import AudioNormalizer
from speechbrain.pretrained import EncoderClassifier
import sys

import kaldiio
import numpy as np
from TTS.api import TTS

class TTSmodel():
    def __init__(self, input_wav_path, output_wav_path):
        self.embed_model = EncoderClassifier.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb", run_opts={"device": 'cpu'}
                )
        self.TTS_model = Text2Speech(model_dir="/home/raffelm/Capstone/voice_subsystem/models/", use_quantized=False)
        self.audio_norm = AudioNormalizer()
        self.fs = 16000
        self.input_wav_path = input_wav_path
        self.output_wav_path = output_wav_path
        self.rtf = None

    def get_rtf(self):
        return self.rtf

    def generate_embed(self):
        in_sr, wav = kaldiio.load_mat(self.input_wav_path)

        if self.fs is not None and self.fs != in_sr:
            wav = resampy.resample(
                    wav.astype(np.float64), in_sr, self.fs, axis=0
                    )
            wav = wav.astype(np.int16)
            in_sr = self.fs

        amax = np.amax(np.absolute(wav))
        wav = wav.astype(np.float32) / amax
        # Freq Norm
        wav = self.audio_norm(torch.from_numpy(wav), in_sr).to('cpu')
        # X-vector Embedding
        self.spembs = self.embed_model.encode_batch(wav).detach().cpu().numpy()[0][0]


    def generate_wav(self, text):
        start = time.time()
        output_dict = self.TTS_model(text, spembs=self.spembs)
        self.rtf = round((time.time() - start) / (len(output_dict["wav"]) / self.fs), 3)

        from IPython.display import Audio
        audio = Audio(output_dict["wav"], rate=self.fs)
        with open(self.output_wav_path + 'voiceOutput.wav', 'wb') as f:
            f.write(audio.data)

    def run(self, text, gen_embed):
        if gen_embed:
            self.generate_embed()

        self.generate_wav(text)

class PreTTSmodel():
    def __init__(self, voice, output_wav_path):
        self.output_wav_path = output_wav_path
        if voice == "Trump":
            self.TTS_model = TTS(model_path="pretrained_models/trump.pth", config_path= "pretrained_models/config.json")
        elif voice == "Obiwan":
            self.TTS_model = TTS(model_path="pretrained_models/obiwan.pth", config_path= "pretrained_models/config.json")
        elif voice == "David":
            self.TTS_model = TTS(model_path="pretrained_models/david.pth", config_path= "pretrained_models/config.json")

        self.rtf = None

    def run(self, text, gen_embed=False):
        self.TTS_model.tts_to_file(text=text, file_path=self.output_wav_path)


    def get_rtf(self):
        return self.rtf




