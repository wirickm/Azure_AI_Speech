# Azure_AI_Speech
A Python project to read Reddit AITA stories using Azure AI Text-to-Speech.


# Bringing Reddit AITA Stories to Life with Azure AI Text-to-Speech

This project demonstrates how to use Azure AI Text-to-Speech (TTS) to read Reddit AITA (Am I The Asshole) stories. The project is written in Python and leverages environment variables to securely manage API keys and other sensitive information.

## Features

- Reads text files containing Reddit AITA stories.
- Uses Azure Cognitive Services to convert text to speech.
- Supports neural voices for a more natural and engaging audio experience.
- Keeps sensitive information secure using environment variables.

## Prerequisites

- Python 3.6 or higher
- An Azure Cognitive Services account with a Speech resource
- `pip` package manager

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/wirickm/Azure_AI_Speech.git
    cd Azure_AI_Speech
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Copy `env.env` to `.env` (which is git-ignored) and put your real Azure Speech API key, region, and the file path to the text file you want to read in `.env`. `env.env` is a placeholder template tracked in git, so never put real secrets in it:

    ```sh
    cp env.env .env
    ```

    ```env
    AZURE_SPEECH_KEY=your_azure_speech_api_key
    AZURE_SERVICE_REGION=your_azure_service_region
    FILE_PATH=path_to_your_text_file.txt
    ```

## Usage

Read a story and save it as an MP3:

```sh
python aita_tts.py samples/example_story.txt -o story.mp3
```

Play it through your default speaker instead (no `-o`):

```sh
python aita_tts.py samples/example_story.txt
```

Pick a different neural voice with `--voice` (or set `AZURE_SPEECH_VOICE`); the default is `en-US-KaiNeural`:

```sh
python aita_tts.py samples/example_story.txt --voice en-US-JennyNeural -o story.mp3
```

If you leave out the file path, the script uses `FILE_PATH` from `.env`. Output files ending in `.wav` are written as WAV.

### Notebook

Prefer Jupyter? Start `jupyter notebook`, open `Azure AITA Text-To-Speech.ipynb`, and run all cells.

## Running Tests

The tests run offline with a faked Speech SDK, so no Azure key is needed:

```sh
pip install -r requirements.txt -r requirements-dev.txt
pytest
```
