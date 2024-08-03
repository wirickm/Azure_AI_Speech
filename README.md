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
    git clone https://github.com/wirickm/azure-tts-aita-reader.git
    cd azure-tts-aita-reader
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and add your Azure Speech API key, region, and the file path to the text file you want to read:

    ```env
    AZURE_SPEECH_KEY=your_azure_speech_api_key
    AZURE_SERVICE_REGION=your_azure_service_region
    FILE_PATH=path_to_your_text_file.txt
    ```

## Usage

Run the script to read the text file using Azure Text-to-Speech:

```sh
python text_to_speech.py
