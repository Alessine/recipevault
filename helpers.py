import requests
import json

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def load_api_credentials():
    with open('credentials.json') as data_file:
        data = json.load(data_file)
    return data['api_key']


def clean_recipe_data(recipe_json):
    recipe = recipe_json["recipes"][0]
    recipe["summary"] = '. '.join(recipe["summary"].split(". ")[0:3]) + '.'
    return recipe


def request_random_recipe():
    """
    This function requests data on a random recipe from the Spoonacular API and returns it in JSON format.
    """
    # Credentials
    api_key = load_api_credentials()
    # Request a random recipe from the API
    random_recipe = requests.get(f"https://api.spoonacular.com/recipes/random?apiKey={api_key}")
    # Check if the API response is valid
    try:
        random_recipe_json = random_recipe.json()
        if 'status' in random_recipe_json.keys():
            api_response = f"API request returned status: '{random_recipe_json['status']}' with code: '{random_recipe_json['code']}' and message: '{random_recipe_json['message']}'"
            return apology(api_response)
        else:
            # If it is, clean the data and return it
            random_recipe = clean_recipe_data(random_recipe_json)
            return random_recipe
    except ValueError:
        # Otherwise return an apology
        return apology(f"ValueError when decoding JSON - API response reads: {random_recipe}.")


def retrieve_recipe_data(database, spoon_id):
    """"
    This function retrieves data on a specific recipe that was previously saved in the database and returns it in JSON format.
    """
    try:
        recipe_list = database.execute("SELECT recipe_information FROM recipes WHERE spoon_id = ?", spoon_id)
    except ValueError:
        return apology(f"Could not retrieve data from database", 400)
    if len(recipe_list) > 0:
        recipe_json = json.loads(recipe_list[0]["recipe_information"])
        return recipe_json
    else:
        return None
