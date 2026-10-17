import os
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import aita_tts  # noqa: E402

sdk = aita_tts.speechsdk


class FakeSpeechConfig:
    def __init__(self, subscription, region):
        self.subscription = subscription
        self.region = region
        self.speech_synthesis_voice_name = None
        self.output_format = None

    def set_speech_synthesis_output_format(self, fmt):
        self.output_format = fmt


class FakeAudioOutputConfig:
    def __init__(self, filename=None, use_default_speaker=False):
        self.filename = filename
        self.use_default_speaker = use_default_speaker


@pytest.fixture
def fake_sdk(monkeypatch):
    calls = {"result": SimpleNamespace(reason=sdk.ResultReason.SynthesizingAudioCompleted)}

    class FakeSynthesizer:
        def __init__(self, speech_config, audio_config):
            calls["speech_config"] = speech_config
            calls["audio_config"] = audio_config

        def speak_text_async(self, text):
            calls["text"] = text
            return SimpleNamespace(get=lambda: calls["result"])

    monkeypatch.setattr(sdk, "SpeechConfig", FakeSpeechConfig)
    monkeypatch.setattr(sdk, "SpeechSynthesizer", FakeSynthesizer)
    monkeypatch.setattr(sdk.audio, "AudioOutputConfig", FakeAudioOutputConfig)
    return calls


@pytest.fixture
def clean_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # so env.env / .env from the repo are not loaded
    for name in ("AZURE_SPEECH_KEY", "AZURE_SERVICE_REGION", "FILE_PATH", "AZURE_SPEECH_VOICE"):
        monkeypatch.delenv(name, raising=False)
    return tmp_path


def test_synthesize_to_mp3_file(fake_sdk):
    aita_tts.synthesize("hello", "k", "eastus", output="out.mp3")
    assert fake_sdk["audio_config"].filename == "out.mp3"
    assert fake_sdk["speech_config"].output_format == \
        sdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
    assert fake_sdk["speech_config"].speech_synthesis_voice_name == "en-US-KaiNeural"
    assert fake_sdk["text"] == "hello"


def test_synthesize_to_speaker(fake_sdk):
    aita_tts.synthesize("hello", "k", "eastus", voice="en-US-JennyNeural")
    assert fake_sdk["audio_config"].use_default_speaker is True
    assert fake_sdk["audio_config"].filename is None
    assert fake_sdk["speech_config"].output_format is None
    assert fake_sdk["speech_config"].speech_synthesis_voice_name == "en-US-JennyNeural"


def test_synthesize_canceled_raises(fake_sdk):
    fake_sdk["result"] = SimpleNamespace(
        reason=sdk.ResultReason.Canceled,
        cancellation_details=SimpleNamespace(reason="Error", error_details="bad key"),
    )
    with pytest.raises(RuntimeError, match="bad key"):
        aita_tts.synthesize("hello", "k", "eastus")


def test_cli_missing_env_exits_2(fake_sdk, clean_env):
    story = clean_env / "story.txt"
    story.write_text("hi")
    with pytest.raises(SystemExit) as exc:
        aita_tts.main([str(story)])
    assert exc.value.code == 2
    assert "text" not in fake_sdk


def test_cli_uses_file_path_fallback(fake_sdk, clean_env, monkeypatch):
    story = clean_env / "story.txt"
    story.write_text("Once upon a time.")
    monkeypatch.setenv("AZURE_SPEECH_KEY", "k")
    monkeypatch.setenv("AZURE_SERVICE_REGION", "eastus")
    monkeypatch.setenv("FILE_PATH", str(story))
    assert aita_tts.main(["-o", "out.mp3"]) == 0
    assert fake_sdk["text"] == "Once upon a time."
    assert fake_sdk["audio_config"].filename == "out.mp3"


def test_cli_empty_file_errors(fake_sdk, clean_env, monkeypatch):
    story = clean_env / "empty.txt"
    story.write_text("   \n")
    monkeypatch.setenv("AZURE_SPEECH_KEY", "k")
    monkeypatch.setenv("AZURE_SERVICE_REGION", "eastus")
    with pytest.raises(SystemExit) as exc:
        aita_tts.main([str(story)])
    assert exc.value.code == 2
    assert "text" not in fake_sdk


def test_cli_synthesis_failure_returns_1(fake_sdk, clean_env, monkeypatch):
    story = clean_env / "story.txt"
    story.write_text("hi")
    monkeypatch.setenv("AZURE_SPEECH_KEY", "k")
    monkeypatch.setenv("AZURE_SERVICE_REGION", "eastus")
    fake_sdk["result"] = SimpleNamespace(
        reason=sdk.ResultReason.Canceled,
        cancellation_details=SimpleNamespace(reason="Error", error_details=""),
    )
    assert aita_tts.main([str(story)]) == 1
