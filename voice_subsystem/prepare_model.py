# Export model
from onnxruntime.quantization import QuantFormat, QuantType, quantize_static
from onnxruntime.quantization.calibrate import CalibrationDataReader
from onnxruntime.quantization.shape_inference import quant_pre_process
from espnet2.tasks.tts import TTSTask
from espnet2.bin.tts_inference import Text2Speech

from typing import Union
from pathlib import Path
from typeguard import check_argument_types

import torch

from espnet_onnx.export.tts.models import (
    get_tts_model
)
from espnet_onnx.utils.config import (
    save_config,
)
from espnet_onnx.export.tts.get_config import (
    get_token_config,
    get_preprocess_config,
    get_vocoder_config,
    get_normalize_config
)

class VCTKDataReader(CalibrationDataReader):
    def __init__(self, loader):
        self.loader = iter(loader)

    def get_next(self):
        (keys, batch) = next(self.loader, (None, None))
        if batch is not None:
            assert isinstance(batch, dict), type(batch)
            assert all(isinstance(s, str) for s in keys), keys
            _bs = len(next(iter(batch.values())))
            assert _bs == 1, _bs

            # Change to single sequence and remove *_length
            # because inference() requires 1-seq, not mini-batch.
            batch = {k: v[0] for k, v in batch.items() if not k.endswith("_lengths")}
            batch["text"] = batch["text"].numpy()
            batch["spembs"] = batch["spembs"].numpy()
        print("batch")
        return batch

    def rewind(self):
        self.loader = None

class TTSModelExport:
    def __init__(self, cache_dir: Union[Path, str] = None):
        assert check_argument_types()
        
        self.cache_dir = Path(cache_dir)
        self.export_config = {}
        self.train_args = None

    def export(
        self,
        model: Text2Speech,
        quantize: bool = False,
        verbose: bool = False,
    ):
        assert check_argument_types()

        export_dir = self.cache_dir / 'onnx'

        # copy model files 
        model_config = self._create_config(model, export_dir)
        self.train_args = model.train_args

        # export encoder
        tts_model = get_tts_model(model.model.tts, self.export_config)
        self._export_model(tts_model, export_dir, verbose)
        model_config.update(tts_model=tts_model.get_model_config(export_dir))

        model_config.update(vocoder=get_vocoder_config(None))

        if quantize:
            self._quantize_model()
            model_config['tts_model'].update(quantized_model_path=str(self.cache_dir / 'quantize'/'vits.onnx'))

        config_name = self.cache_dir / 'config.yaml'
        save_config(model_config, config_name)
    
    def export_from_zip(self, path: Union[Path, str], quantize: bool = False, verbose: bool = False):
        assert check_argument_types()
        model = Text2Speech.from_pretrained(path)
        self.export(model, quantize, verbose)
    
    def _create_config(self, model, path):
        ret = {}
        ret.update(get_preprocess_config(model.preprocess_fn, path))
        ret.update(normalize=get_normalize_config(model.model.normalize, path))
        ret.update(token=get_token_config(model.preprocess_fn.token_id_converter))
        return ret

    def _export_model(self, model, path, verbose):     
        dummy_input = model.get_dummy_inputs()

        torch.onnx.export(
            model,
            dummy_input,
            str(path/'vits.onnx'),
            verbose=verbose,
            opset_version=15,
            input_names=model.get_input_names(),
            output_names=model.get_output_names(),
            dynamic_axes=model.get_dynamic_axes(),
        )

    def _quantize_model(self):
        #data_path_and_name_and_type= [('/nfs/stak/users/raffelm/hpc-share/capstone/espnet/egs2/libritts/tts1/dump/22k/raw/dev-clean/text', 'text', 'text'), ('/nfs/stak/users/raffelm/hpc-share/capstone/espnet/egs2/libritts/tts1/dump/22k/xvector/dev-clean/xvector.scp', 'spembs', 'kaldi_ark')]
        data_path_and_name_and_type= [('/nfs/stak/users/raffelm/hpc-share/capstone/testing/text', 'text', 'text'), ('/nfs/stak/users/raffelm/hpc-share/capstone/testing/xvector.scp', 'spembs', 'kaldi_ark')]
        #From tts_inference.py
        loader=TTSTask.build_streaming_iterator(
                data_path_and_name_and_type,
                dtype='float32',
                batch_size=1,
                key_file='/nfs/stak/users/raffelm/hpc-share/capstone/testing/text',
                num_workers=1,
                preprocess_fn=TTSTask.build_preprocess_fn(self.train_args, False),
                collate_fn=TTSTask.build_collate_fn(self.train_args, False),
                allow_variable_data_keys=False,
                ngpu=0,
                inference=True,
            )

        quant_pre_process(
            input_model_path=str(self.cache_dir) + "/onnx/vits.onnx",
            output_model_path=str(self.cache_dir) + "/optimized/vits.onnx",
            skip_symbolic_shape = True,
        )

        quantize_static(
            model_input=str(self.cache_dir) + "/optimized/vits.onnx",
            model_output=str(self.cache_dir) + "/quantize/vits.onnx",
            calibration_data_reader= VCTKDataReader(loader),
            quant_format=QuantFormat.QDQ,
            per_channel=True,
            reduce_range=True,
            op_types_to_quantize=['Conv'],
            activation_type=QuantType.QInt8,
            weight_type=QuantType.QInt8,
            optimize_model=False,
            nodes_to_exclude=['/generator/decoder/input_conv/Conv', '/generator/decoder/global_conv/Conv',
                              '/generator/decoder/blocks.2/convs1.0/convs1.0.1/Conv', '/generator/decoder/blocks.1/convs1.0/convs1.0.1/Conv', '/generator/decoder/blocks.0/convs1.0/convs1.0.1/Conv',
                              '/generator/decoder/blocks.2/convs2.0/convs2.0.1/Conv', '/generator/decoder/blocks.1/convs2.0/convs2.0.1/Conv', '/generator/decoder/blocks.0/convs2.0/convs2.0.1/Conv',
                              '/generator/decoder/blocks.2/convs1.1/convs1.1.1/Conv', '/generator/decoder/blocks.1/convs1.1/convs1.1.1/Conv', '/generator/decoder/blocks.0/convs1.1/convs1.1.1/Conv',
                              '/generator/decoder/blocks.2/convs2.1/convs2.1.1/Conv', '/generator/decoder/blocks.1/convs2.1/convs2.1.1/Conv', '/generator/decoder/blocks.0/convs2.1/convs2.1.1/Conv',
                              '/generator/decoder/blocks.2/convs1.2/convs1.2.1/Conv', '/generator/decoder/blocks.1/convs1.2/convs1.2.1/Conv', '/generator/decoder/blocks.0/convs1.2/convs1.2.1/Conv',
                              '/generator/decoder/blocks.2/convs2.2/convs2.2.1/Conv', '/generator/decoder/blocks.1/convs2.2/convs2.2.1/Conv', '/generator/decoder/blocks.0/convs2.2/convs2.2.1/Conv',
                              '/generator/decoder/blocks.5/convs1.0/convs1.0.1/Conv', '/generator/decoder/blocks.4/convs1.0/convs1.0.1/Conv', '/generator/decoder/blocks.3/convs1.0/convs1.0.1/Conv',
                              '/generator/decoder/blocks.5/convs2.0/convs2.0.1/Conv', '/generator/decoder/blocks.4/convs2.0/convs2.0.1/Conv', '/generator/decoder/blocks.3/convs2.0/convs2.0.1/Conv',
                              '/generator/decoder/blocks.5/convs1.1/convs1.1.1/Conv', '/generator/decoder/blocks.4/convs1.1/convs1.1.1/Conv', '/generator/decoder/blocks.3/convs1.1/convs1.1.1/Conv',
                              '/generator/decoder/blocks.5/convs2.1/convs2.1.1/Conv', '/generator/decoder/blocks.4/convs2.1/convs2.1.1/Conv', '/generator/decoder/blocks.3/convs2.1/convs2.1.1/Conv',
                              '/generator/decoder/blocks.5/convs1.2/convs1.2.1/Conv', '/generator/decoder/blocks.4/convs1.2/convs1.2.1/Conv', '/generator/decoder/blocks.3/convs1.2/convs1.2.1/Conv',
                              '/generator/decoder/blocks.5/convs2.2/convs2.2.1/Conv', '/generator/decoder/blocks.4/convs2.2/convs2.2.1/Conv', '/generator/decoder/blocks.3/convs2.2/convs2.2.1/Conv',
                              '/generator/decoder/blocks.8/convs1.0/convs1.0.1/Conv', '/generator/decoder/blocks.7/convs1.0/convs1.0.1/Conv', '/generator/decoder/blocks.6/convs1.0/convs1.0.1/Conv',
                              '/generator/decoder/blocks.8/convs2.0/convs2.0.1/Conv', '/generator/decoder/blocks.7/convs2.0/convs2.0.1/Conv', '/generator/decoder/blocks.6/convs2.0/convs2.0.1/Conv',
                              '/generator/decoder/blocks.8/convs1.1/convs1.1.1/Conv', '/generator/decoder/blocks.7/convs1.1/convs1.1.1/Conv', '/generator/decoder/blocks.6/convs1.1/convs1.1.1/Conv',
                              '/generator/decoder/blocks.8/convs2.1/convs2.1.1/Conv', '/generator/decoder/blocks.7/convs2.1/convs2.1.1/Conv', '/generator/decoder/blocks.6/convs2.1/convs2.1.1/Conv',
                              '/generator/decoder/blocks.8/convs1.2/convs1.2.1/Conv', '/generator/decoder/blocks.7/convs1.2/convs1.2.1/Conv', '/generator/decoder/blocks.6/convs1.2/convs1.2.1/Conv',
                              '/generator/decoder/blocks.8/convs2.2/convs2.2.1/Conv', '/generator/decoder/blocks.7/convs2.2/convs2.2.1/Conv', '/generator/decoder/blocks.6/convs2.2/convs2.2.1/Conv',
                              '/generator/decoder/blocks.11/convs1.0/convs1.0.1/Conv', '/generator/decoder/blocks.10/convs1.0/convs1.0.1/Conv', '/generator/decoder/blocks.9/convs1.0/convs1.0.1/Conv',
                              '/generator/decoder/blocks.11/convs2.0/convs2.0.1/Conv', '/generator/decoder/blocks.10/convs2.0/convs2.0.1/Conv', '/generator/decoder/blocks.9/convs2.0/convs2.0.1/Conv',
                              '/generator/decoder/blocks.11/convs1.1/convs1.1.1/Conv', '/generator/decoder/blocks.10/convs1.1/convs1.1.1/Conv', '/generator/decoder/blocks.9/convs1.1/convs1.1.1/Conv',
                              '/generator/decoder/blocks.11/convs2.1/convs2.1.1/Conv', '/generator/decoder/blocks.10/convs2.1/convs2.1.1/Conv', '/generator/decoder/blocks.9/convs2.1/convs2.1.1/Conv',
                              '/generator/decoder/blocks.11/convs1.2/convs1.2.1/Conv', '/generator/decoder/blocks.10/convs1.2/convs1.2.1/Conv', '/generator/decoder/blocks.9/convs1.2/convs1.2.1/Conv',
                              '/generator/decoder/blocks.11/convs2.2/convs2.2.1/Conv', '/generator/decoder/blocks.10/convs2.2/convs2.2.1/Conv', '/generator/decoder/blocks.9/convs2.2/convs2.2.1/Conv',
                              '/generator/decoder/output_conv/output_conv.1/Conv'
                              ]
        )

# m = TTSModelExport(cache_dir="/nfs/stak/users/raffelm/hpc-share/capstone/testing/modelsBig/")
# m.export_from_zip("/nfs/stak/users/raffelm/hpc-share/capstone/espnet/egs2/libritts/tts1/exp/22k/tts_train_speechbrain_xvector_vits_raw_phn_tacotron_g2p_en_no_space/tts_train_speechbrain_xvector_vits_raw_phn_tacotron_g2p_en_no_space_train.total_count.ave_10best.zip", quantize=True)

m = TTSModelExport(cache_dir="/nfs/stak/users/raffelm/hpc-share/capstone/testing/models/")
m.export_from_zip("/nfs/stak/users/raffelm/hpc-share/capstone/espnet/egs2/libritts/tts1/exp/16k/tts_train_speechbrain_xvector_vits_small_raw_phn_tacotron_g2p_en_no_space/tts_train_speechbrain_xvector_vits_small_raw_phn_tacotron_g2p_en_no_space_latest.zip", quantize=True)

# m = TTSModelExport(cache_dir="/nfs/stak/users/raffelm/hpc-share/capstone/testing/modelsBig16k/")
# m.export_from_zip("/nfs/stak/users/raffelm/hpc-share/capstone/espnet/egs2/libritts/tts1/exp/16k/tts_train_speechbrain_xvector_vits_raw_phn_tacotron_g2p_en_no_space/tts_train_speechbrain_xvector_vits_raw_phn_tacotron_g2p_en_no_space_latest.zip", quantize=True)


