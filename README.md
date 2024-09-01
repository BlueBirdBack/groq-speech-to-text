# groq_transcribe

A Python library for transcribing audio files using Groq's Speech-to-Text API, with support for VTT and SRT subtitle formats.

## Features

- Transcribe audio files using Groq's Speech-to-Text API
- Generate VTT and SRT subtitle files from transcriptions
- Support for various audio formats (mp3, mp4, wav, etc.)
- Customizable transcription parameters (language, prompt, temperature)

## Installation

```bash
pip install groq_transcribe
```

## Usage

### Basic Transcription

```python
from groq_transcribe import transcribe

transcribe("path/to/audio_file.mp3")
```

This will generate three files:
- `audio_file.txt`: Plain text transcription
- `audio_file.vtt`: WebVTT subtitle file
- `audio_file.srt`: SRT subtitle file

### Advanced Usage

```python
from groq_transcribe import transcribe

transcribe(
    "path/to/audio_file.mp3",
    prompt="Transcribe the following medical lecture",
    language="en",
    temperature=0.2
)
```

### Command Line Interface

```bash
groq_transcribe path/to/audio_file.mp3 --prompt "Optional prompt" --language en --temperature 0.2
```

## Configuration

Set your Groq API key as an environment variable:

```bash
export GROQ_API_KEY=your_api_key_here
```

## Requirements

- Python 3.7+
- groq
- python-dotenv

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

This library uses the Groq API for speech-to-text transcription. Visit [Groq's documentation](https://console.groq.com/docs/speech-text) for more information on their Speech-to-Text capabilities.
