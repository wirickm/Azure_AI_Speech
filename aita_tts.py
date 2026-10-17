"""Read a text file aloud (or to an audio file) with Azure AI Text-to-Speech."""

import argparse
import os
import sys

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

DEFAULT_VOICE = "en-US-KaiNeural"


def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def synthesize(text, key, region, voice=DEFAULT_VOICE, output=None):
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.speech_synthesis_voice_name = voice

    if output:
        if output.lower().endswith(".mp3"):
            speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
            )
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output)
    else:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.Canceled:
        details = result.cancellation_details
        message = f"Speech synthesis canceled: {details.reason}"
        if details.error_details:
            message += f" ({details.error_details})"
        raise RuntimeError(message)


def main(argv=None):
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Read an AITA story text file using Azure AI Text-to-Speech."
    )
    parser.add_argument("input", nargs="?", default=os.getenv("FILE_PATH"),
                        help="Text file to read (defaults to FILE_PATH env var)")
    parser.add_argument("-o", "--output",
                        help="Write audio to this file (.mp3 or .wav) instead of the speaker")
    parser.add_argument("--voice", default=os.getenv("AZURE_SPEECH_VOICE", DEFAULT_VOICE),
                        help="Neural voice name (default: %(default)s)")
    args = parser.parse_args(argv)

    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SERVICE_REGION")
    if not key or not region:
        parser.error("AZURE_SPEECH_KEY and AZURE_SERVICE_REGION must be set (.env)")
    if not args.input:
        parser.error("no input file given (pass a path or set FILE_PATH)")

    try:
        text = read_text_file(args.input)
    except OSError as e:
        parser.error(f"could not read {args.input}: {e}")
    if not text.strip():
        parser.error(f"{args.input} is empty")

    try:
        synthesize(text, key, region, voice=args.voice, output=args.output)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"Done: {args.output}" if args.output else "Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
