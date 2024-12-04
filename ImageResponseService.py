import base64
import os

from openai import OpenAI

class ImageResponseService:
    def __init__(self, api_key, image_path):
        self.api_key = api_key
        self.image_path = image_path
        self.client = OpenAI(api_key=self.api_key)  # Initialize the OpenAI client

    def encode_image(self):
        """Encodes the image file as a base64 string."""
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def request_food_type(self):
        """Sends the image to the GPT-4o-mini model and retrieves the response."""
        # Encode the image
        base64_image = self.encode_image()

        # Create a chat completion request
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "This is an image of some type of food dish or food product. GIVE ME ONLY THE NAME OF THE FOOD PRODUCT.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )

        # Accessing the response content
        content = response.choices[0].message.content
        return content