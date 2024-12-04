import os

from openai import OpenAI

class PreparingInstructionsChat:
    def __init__(self, api_key, model="gpt-4o"):
        """
        Initializes the FoodDishChatModel class with API credentials and the model to use.
        :param api_key: OpenAI API key for authentication.
        :param model: The model to query (default is "gpt-4o").
        """
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)  # Initialize the OpenAI client

    def get_dishes_for_food(self, food_name):
        """
        Queries the chat model to get dish preparation instructions for a given food.
        :param food_name: The name of the food ingredient.
        :return: The response from the chat model as a string.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master chef who knows dishes from all over the world. "
                                   "With any ingredient, you can create dishes from any country."
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Give me instructions to prepare a dish using {food_name} from three separate countries. "
                            "First give me the name of the country that the dish is from, then give me the name of the dish, "
                            "and lastly list the instructions as steps that start from purchasing the ingredients to finally "
                            "eating the prepared dish. Enclose each country's response with three vertical bars before the country name to separate the three country responses."
                        )
                    }
                ]
            )
            # Accessing the response content
            content = response.choices[0].message.content
            return content
        except Exception as e:
            return f"Error querying the model: {e}"
