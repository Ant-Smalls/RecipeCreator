import os

from flask import Flask, render_template, request, redirect, url_for
from openai import audio

from ImageResponseService import ImageResponseService
from PreparingInstructionsChat import PreparingInstructionsChat
from ReadInstructions import ReadInstructions
from DishImageCreator import DishImageCreator

app = Flask(__name__, template_folder="FrontEndTemplates")
uploaded_image = None


# Global variables for recipe content
recipe_contents = {"recipeOne": None, "recipeTwo": None, "recipeThree": None}

@app.route("/", methods = ["GET", "POST"])
def main_page():
    global uploaded_image  # Allow access to the global variable
    response_message = None

    if request.method == "POST":
        if "image" in request.files:
            file = request.files["image"]
            if file:
                directory = "/Users/ant-smalls/Desktop/CPSC415AI/RecipeCreator/app/Static/Images"
                file_path = f"Images/{file.filename}"
                full_path = f"{directory}/{file.filename}"  # Full path for saving

                # Ensure the directory exists
                os.makedirs(directory, exist_ok=True)

                file.save(full_path)  # Save the image to the static/images directory
                uploaded_image = file_path

                try:
                    # Step 1: Process image with ImageResponseService
                    imageResponseService = ImageResponseService(os.getenv("OPENAI_API_KEY"),full_path)
                    response_message = imageResponseService.request_food_type()

                    # Step 2: Process the response with FoodInstructor
                    foodInstructor = PreparingInstructionsChat(os.getenv("OPENAI_API_KEY"))
                    all_responses = foodInstructor.get_dishes_for_food(response_message)
                    print(all_responses)

                    # Step 3: Split the long string into sections
                    split_content = all_responses.split("|||")
                    if len(split_content) > 1:  # Ensure there's at least one section
                        recipe_contents["recipeOne"] = split_content[1].strip()  # First section (after first ###)
                    if len(split_content) > 2:
                        recipe_contents["recipeTwo"] = split_content[2].strip()  # Second section (after second ###)
                    if len(split_content) > 3:
                        recipe_contents["recipeThree"] = split_content[3].strip()  # Third section (after third ###)
                    else:
                        print("Error: Not enough sections in the long string.")

                    #Step 4: Create audio files for the instructions
                    #reader = ReadInstructions(api_key=os.getenv("xi_api_key"))
                    #reader.convert_to_speech(recipe_contents["recipeOne"],"/Users/ant-smalls/Desktop/CPSC415AI/RecipeCreator/app/Static/Audio","recipeOneInstructions.mp3")
                    #reader.convert_to_speech(recipe_contents["recipeTwo"],"/Users/ant-smalls/Desktop/CPSC415AI/RecipeCreator/app/Static/Audio","recipeTwoInstructions.mp3")
                    #reader.convert_to_speech(recipe_contents["recipeThree"],"/Users/ant-smalls/Desktop/CPSC415AI/RecipeCreator/app/Static/Audio","recipeThreeInstructions.mp3")

                    #Step 5: Create images of the dishes
                    dishImageCreator = DishImageCreator(os.getenv("OPENAI_API_KEY"))
                    dishImageCreator.create_dish_image(recipe_contents["recipeOne"],"/Users/ant-smalls/Desktop/CPSC415AI/RecipeCreator/app/Static/DishImages","recipeOneDishImage.jpg")
                    dishImageCreator.create_dish_image(recipe_contents["recipeTwo"],"/Users/ant-smalls/Desktop/CPSC415AI/RecipeCreator/app/Static/DishImages","recipeTwoDishImage.jpg")
                    dishImageCreator.create_dish_image(recipe_contents["recipeThree"],"/Users/ant-smalls/Desktop/CPSC415AI/RecipeCreator/app/Static/DishImages","recipeThreeDishImage.jpg")

                except Exception as e:
                    print(f"Error processing image or response: {e}")


    recipes = {
        "Recipe One": "/RecipeCreator/recipeOne",
        "Recipe Two": "/RecipeCreator/recipeTwo",
        "Recipe Three": "/RecipeCreator/recipeThree",
    }
    return render_template("mainPage.html", page_title="Recipe Creator", recipes=recipes, response_message=response_message,uploaded_image=uploaded_image)


@app.route("/upload", methods=["POST"])
def upload_image():

    print("Files:", request.files)

    # Check if both fields are present in the request
    if "image" not in request.files or "recipe" not in request.form:
        return "Image and recipe selection are required.", 400

    file = request.files["image"]

    if file:
        filepath = f"static/images/{file.filename}"
        file.save(filepath)
        global uploaded_image
        uploaded_image = filepath

        return redirect(url_for("main_page"))


@app.route("/RecipeCreator/recipeOne", methods=["GET"])
def recipe_one():
    # Path to the new image for the left column
    left_column_image = "Static/DishImages/recipeOneDishImage.jpg"
    right_column_text = recipe_contents["recipeOne"]
    audio_file = "Static/Audio/recipeOneInstructions.mp3"

    return render_template(
        "recipeOne.html",
        left_column_image=left_column_image,
        right_column_text=right_column_text,
        audio_file=audio_file,
        page_title="Recipe One",
    )

@app.route("/RecipeCreator/recipeTwo", methods=["GET"])
def recipe_two():
    left_column_image = "Static/DishImages/recipeTwoDishImage.jpg"
    right_column_text = recipe_contents["recipeTwo"]
    audio_file = "Static/Audio/recipeTwoInstructions.mp3"

    return render_template(
        "recipeTwo.html",
        left_column_image=left_column_image,
        right_column_text=right_column_text,
        audio_file=audio_file,
        page_title="Recipe Two"
    )

@app.route("/RecipeCreator/recipeThree", methods=["GET"])
def recipe_three():
    left_column_image = "Static/DishImages/recipeThreeDishImage.jpg"
    right_column_text = recipe_contents["recipeThree"]
    audio_file = "Static/Audio/recipeThreeInstructions.mp3"

    return render_template(
        "recipeThree.html",
        left_column_image=left_column_image,
        right_column_text=right_column_text,
        audio_file=audio_file,
        page_title="Recipe Three"
    )

if __name__ == "__main__":
    app.run(debug=True, port=8080)
