import os

from dotenv import load_dotenv
from elevenlabs import ElevenLabs


class ReadInstructions:
    def __init__(self, api_key, voice_id="EMqtGrcPkjW1YY37f3vS", model_id="eleven_multilingual_v2"):
        """
        Initialize the ReadInstructions class with API credentials, voice ID, and model ID.

        :param api_key: Your Eleven Labs API key.
        :param voice_id: The voice ID to use for text-to-speech.
        :param model_id: The model ID to use for text-to-speech.
        """
        self.client = ElevenLabs(api_key=api_key)
        self.voice_id = voice_id
        self.model_id = model_id

    def convert_to_speech(self, text, save_folder, filename):
        """
        Converts text to speech and saves it as an MP3 file.

        :param text: The text to convert to speech.
        :param save_folder: The folder where the MP3 file will be saved.
        :param filename: The name of the MP3 file. Default is "output.mp3".
        :return: Full path to the saved MP3 file.
        """
        if not os.path.exists(save_folder):
            os.makedirs(save_folder, exist_ok=True)  # Ensure the save folder exists

        # Generate the audio using Eleven Labs
        print(f"Sending text to Eleven Labs for conversion: {text[:50]}...")  # Preview the first 50 characters
        try:
            audio_generator = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                model_id=self.model_id,
                text=text,
            )

            # Save the audio data to a file
            output_path = os.path.join(save_folder, filename)
            with open(output_path, "wb") as audio_file:
                for chunk in audio_generator:
                    audio_file.write(chunk)

            print(f"Audio successfully saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"Error converting text to speech: {e}")
            raise