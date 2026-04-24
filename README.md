# PushToWhisper

PushToWhisper is a high-performance, background voice dictation assistant that transforms your keyboard's F9 key into a push-to-talk mechanism. Powered by OpenAI's `large-v3-turbo` Whisper AI model locally on your GPU, it detects your speech, processes the audio with zero-delay, and pastes the flawlessly transcribed text directly into any active window or application you are currently focused on.

## Features

- Zero-Latency Recording: The microphone is initialized continuously in a background thread, meaning there is zero delay when you press F9. It captures your speech from the very first syllable.
- Tail Padding: Continues recording for a seamless 0.4 seconds after releasing the hotkey to prevent cutting off the final syllables or trailing speech echoes.
- Ghost Paste Integration: Built-in clipboard management and keyboard simulation instantly pastes your dictated text into web browsers, documents, IDEs, or configuration nodes (e.g., n8n).
- Intelligent Custom Dictionary (`kelimeler.txt`): Out-of-the-box support for domain-specific jargon. Adding terms to the auto-generated external text file strictly enforces the model to output your desired acronyms and edge-case words (e.g., "RAG", "LLM", "n8n") without any code modification.
- Advanced VAD Filtering: Voice Activity Detection filters out throat-clearing, deep breaths, and room static to maintain pristine AI context mapping.

## System Requirements

Due to the use of the `large-v3-turbo` model, your system should meet the following minimum specifications for optimal performance:
- **GPU:** NVIDIA GPU with at least 4-6 GB of VRAM (CUDA support is required for fast processing).
- **RAM:** Minimum 8 GB of system memory.
- **Storage:** ~3 GB of free disk space for downloading and caching the model weights.
- **OS:** Windows 10/11
- **Python:** Python 3.8 or higher

## Installation

We strongly recommend running this within an isolated virtual environment (venv).

To install the dependencies, navigate to the directory and run:

```powershell
pip install -r requirements.txt
```

Note: To guarantee lightning-fast transcription using GPU tensor cores, `PushToWhisper` utilizes the `ctranslate2` engine. Essential DLL structures (`nvidia-cublas-cu12` and `nvidia-cudnn-cu12`) are inherently managed inside the requirements, bypassing the need to natively install a dense full-system NVIDIA CUDA Toolkit.

## Usage

1. Execute the main program or run the provided batch script:
```powershell
python pushtowhisper.py
```
2. Wait for the model to be allocated into your VRAM. If this is the primary run, it will download the ~3 GB `large-v3-turbo` model files securely into your local cache. Afterwards, loading will be nearly instantaneous.
3. Once the "Sistem Tamamen Hazır!" (System Fully Ready) signal appears, click inside your desired text area (e.g., a Word document or Chrome search bar).
4. Press and hold down the `F9` key on your keyboard and dictate your message.
5. Release the key when finished. Within mere seconds, the accurately refined text will automatically map to your active cursor.

## Training the Vocabulary Engine

Upon execution, the script will map a `kelimeler.txt` file inside its root directory.
You may dynamically edit this text file to include specific abbreviations or technical jargon relevant to your workflow. The AI dynamically refers to this list upon every transcription cycle as its "initial prompt", guaranteeing words like "RAG" or "Excel" are never mistakenly transcribed phonetically.

## Warnings and Considerations

- Administrator Privileges: In strict IT environments or specific code editors, the `keyboard` module may fail to capture the `F9` keydown event passively. Ensure you grant "Run as Administrator" access to your executing terminal if this occurs.
- VRAM Constraints: If your system encounters an Out-Of-Memory (OOM) error resulting in unexpected crashes, you lack the dedicated VRAM for the `large-v3-turbo` dataset. Inside the Python configuration code, redefine the `MODEL_SIZE` variable from `"large-v3-turbo"` to either `"medium"` or `"small"` to drastically reduce memory usage.
