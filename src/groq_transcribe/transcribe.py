"""Module for transcribing audio files using Groq API.

For more information, see: https://console.groq.com/docs/speech-text
"""

import sys

try:
    import argparse
    import os
    from groq import Groq, GroqError
    from dotenv import load_dotenv, find_dotenv
except ImportError as e:
    print(f"ImportError: {e}. Please install the required packages.")
    sys.exit(1)


load_dotenv(find_dotenv(), override=True)
api_key = os.getenv("GROQ_API_KEY")

try:
    client = Groq(api_key=api_key)
except GroqError:
    print("Error: GROQ_API_KEY not found in environment variables.")
    print("Please set the GROQ_API_KEY in your .env file or environment.")
    print("You can obtain an API key from: https://console.groq.com/keys")
    sys.exit(1)


def verbose_json_to_vtt(json_data):
    """Convert verbose JSON transcription data to VTT format."""
    vtt_lines = ["WEBVTT\n"]
    for segment in json_data.segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        start_h, start_rem = divmod(start, 3600)
        start_m, start_s = divmod(start_rem, 60)
        start_ms = (start - int(start)) * 1000

        end_h, end_rem = divmod(end, 3600)
        end_m, end_s = divmod(end_rem, 60)
        end_ms = (end - int(end)) * 1000

        start_time = (
            f"{int(start_h):02}:{int(start_m):02}:{int(start_s):02}.{int(start_ms):03}"
        )
        end_time = f"{int(end_h):02}:{int(end_m):02}:{int(end_s):02}.{int(end_ms):03}"

        vtt_lines.append(f"{start_time} --> {end_time}")
        vtt_lines.append(text)
        vtt_lines.append("")

    return "\n".join(vtt_lines)


def verbose_json_to_srt(json_data):
    """Convert verbose JSON transcription data to SRT format."""
    srt_lines = []
    for i, segment in enumerate(json_data.segments, start=1):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        start_h, start_rem = divmod(start, 3600)
        start_m, start_s = divmod(start_rem, 60)
        start_ms = (start - int(start)) * 1000

        end_h, end_rem = divmod(end, 3600)
        end_m, end_s = divmod(end_rem, 60)
        end_ms = (end - int(end)) * 1000

        start_time = (
            f"{int(start_h):02}:{int(start_m):02}:{int(start_s):02},{int(start_ms):03}"
        )
        end_time = f"{int(end_h):02}:{int(end_m):02}:{int(end_s):02},{int(end_ms):03}"

        srt_lines.append(str(i))
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(text)
        srt_lines.append("")

    return "\n".join(srt_lines)


def transcribe(filename, model, prompt, language, temperature):
    """
    Transcribe audio file and save results in multiple formats.

    Args:
        filename (str): Path to the audio file.
        prompt (str): Optional transcription prompt.
        language (str): Language of the audio.
        temperature (float): Temperature for transcription.
        model (str): Groq model to use for transcription.
    """
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model=model,
            prompt=prompt,
            response_format="verbose_json",
            language=language,
            temperature=temperature,
        )
        print(transcription)
        transcribed_text = transcription.text
        print("Original Transcription:", transcribed_text)

        base_filename = os.path.splitext(filename)[0]
        with open(f"{base_filename}.txt", "w", encoding="utf-8") as file:
            file.write(transcribed_text)

        vtt_output = verbose_json_to_vtt(transcription)
        with open(f"{base_filename}.vtt", "w", encoding="utf-8") as f:
            f.write(vtt_output)

        # Convert to SRT
        srt_output = verbose_json_to_srt(transcription)
        with open(f"{base_filename}.srt", "w", encoding="utf-8") as f:
            f.write(srt_output)


def main():
    """Main function to handle command-line arguments and transcribe the audio file."""
    parser = argparse.ArgumentParser(description="Transcribe audio to text.")

    parser.add_argument("file_path", type=str, help="Path to the input audio file")

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="w",
        choices=["d", "w"],
        help="Groq model: 'd' for distil-whisper-large-v3-en, 'w' for whisper-large-v3",
    )

    parser.add_argument(
        "-p", "--prompt", type=str, default="", help="Optional prompt for transcription"
    )

    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default=None,
        help=(
            "Language of the audio (e.g., 'en' for English, 'zh' for Chinese). "
            "If not specified, auto-detection will be used."
        ),
    )

    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=0.0,
        help="Temperature for transcription",
    )

    # try:
    #     args = parser.parse_args()
    # except SystemExit:
    #     if len(sys.argv) == 1:
    #         parser.print_help()
    #     sys.exit(1)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code == 2:  # argparse exits with code 2 for argument errors
            parser.print_usage()
            print(
                f"{parser.prog}: error: the following arguments are required: file_path"
            )
        sys.exit(e.code)

    model_map = {"d": "distil-whisper-large-v3-en", "w": "whisper-large-v3"}
    args.model = model_map[args.model]

    transcribe(args.file_path, args.model, args.prompt, args.language, args.temperature)


if __name__ == "__main__":
    main()
