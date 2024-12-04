import requests
import os
import re
from openai import OpenAI


class DishImageCreator:
    def __init__(self, api_key):
        """
        Initialize the DishCreator class with API credentials.

        :param api_key: Your OpenAI API key.
        """
        self.client = OpenAI(api_key=api_key)

    def create_dish_image(self, dish, save_folder, file_name, size="1024x1024", quality="standard", n=1):
        """
        Generate an image of a dish based on the provided dish name and save it locally.

        :param dish_name: The name of the dish to generate an image for.
        :param save_folder: The folder to save the generated image.
        :param size: The size of the generated image (default is 1024x1024).
        :param quality: The quality of the generated image (default is "standard").
        :param n: The number of images to generate (default is 1).
        :return: The local file path of the saved image or None if generation fails.
        """
        prompt = f"A realistic and visually appealing image of a dish with the included ingredients. Here is the dish with the country and cooking instructions. Disregard the instructions and find the country name and name of the dish to create the image: '{dish}'"
        try:
            # Generate the image URL using OpenAI
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=n,
            )
            image_url = response.data[0].url

            # Ensure the save folder exists
            os.makedirs(save_folder, exist_ok=True)

            # Download and save the image locally
            local_filepath = os.path.join(save_folder, file_name)

            response = requests.get(image_url)
            with open(local_filepath, "wb") as image_file:
                image_file.write(response.content)

            print(f"Image saved locally at {local_filepath}")
            return local_filepath
        except Exception as e:
            print(f"Error generating or saving image for {dish}: {e}")
            return None
