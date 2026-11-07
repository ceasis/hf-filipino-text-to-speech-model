# QnVoice Filipino Text to Speech

This project packages the Filipino voice used in QnVoice. It uses OpenBMB’s pretrained VoxCPM2 with a Q4_K_M language graph, selective Q8_0 acoustic quantization, and an original synthetic Tagalog voice reference.

- [Exact QnVoice GGUF release on Hugging Face](https://huggingface.co/CholoAsis/qnvoice-filipino-voxcpm2-gguf/tree/5b912ca3328145b384134040dcc520114f000e32)
- [White paper](QnVoice-Filipino-Speech-Manuscript.pdf)
- [All versions of the preprint on Zenodo](https://doi.org/10.5281/zenodo.24022271)

## Download and run

Run the downloader with Python 3.9 or later. It saves the two GGUF files and the reference in `model/` and checks the SHA-256 digest of every file. The weights total about 2.08 GB and are hosted on Hugging Face. Inference runs offline after the download.

```sh
python3 fetch-model.py
python3 fetch-model.py --verify
voxcpm2-cli --text 'Magandang hapon po.' \
  --reference model/voice-reference.wav --output filipino.wav \
  --stream --steps 93 --timesteps 6 --seed 98000 \
  model/voice-language.gguf model/voice-acoustic.gguf
```

Use a VoxCPM2 GGUF runtime that accepts separate language and acoustic files. The example uses [the runtime revision used by QnVoice](https://github.com/tc-mb/llama.cpp-omni/tree/e0eca9d8f57ac8f5a5ad6191a8007b93436c1e71/tools/omni/voxcpm2). The paper describes the app’s text normalization and measured iPhone performance.

## License and attribution

The two GGUF weights are available under the [Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for upstream credits and changes to the acoustic graph.

QnSub Software Solutions permits personal and commercial use of the included synthetic voice reference and speech generated with it at no charge. An app that uses this reference for speech synthesis must cite the paper in its About screen, credits, or public documentation. [Published model and reference terms](https://huggingface.co/CholoAsis/qnvoice-filipino-voxcpm2-gguf/tree/5b912ca3328145b384134040dcc520114f000e32)
