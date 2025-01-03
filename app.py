from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import json

from helpers import apology, login_required, request_random_recipe, retrieve_recipe_data

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///recipevault.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def welcome():
    """Show the welcome page (if logged in)"""
    # POST method is for the two buttons
    if request.method == 'POST':
        # If the user clicks for a new suggestion
        if request.form.get("next_suggestion") == 'Next Suggestion':
            # Redo the API request for a random recipe
            random_recipe = request_random_recipe()
            # Store the data in the session object and redirect to show the new recipe teaser
            session["random_recipe"] = random_recipe
            return redirect("/")
        # If the user clicks to view the recipe
        if request.form.get("view_recipe") == 'View Recipe':
            return render_template("recipe.html", recipe_information=session["random_recipe"])

    # GET method for rendering the page
    else:
        # Get the user information
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )
        # Check if this session already has a recipe
        if "random_recipe" in session.keys():
            # If so, just render the teaser
            return render_template("welcome.html", user=user, recipe_information=session["random_recipe"])
        else:
            # If not, get a random recipe from the API
            random_recipe = request_random_recipe()
            # Store the data in the session object an show a teaser of the recipe
            session["random_recipe"] = random_recipe
            return render_template("welcome.html", user=user, recipe_information=session["random_recipe"])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["quotes"] = []

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure the two passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("password must match confirmation", 400)

        # Add the user to the database
        username = request.form.get("username")
        password_hash = generate_password_hash(request.form.get("password"))

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password_hash)
        except ValueError:
            return apology(f"user {username} already exists", 400)

        # Log the user in
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["quotes"] = []

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/recipe", methods=["GET", "POST"])
def recipe():
    """Show the recipe and save it to favorites if needed"""
    # If post, then save the data
    if request.method == 'POST':
        #request.form.get("add_favorite").startswith("favorite")
        spoon_id = int(request.form.get("add_favorite").split("_")[1])
        recipe_json = retrieve_recipe_data(database=db, spoon_id=spoon_id)
        # If data is available in the database, use it. Otherwise take the session recipe.
        if not recipe_json:
            recipe_json = session["random_recipe"]

        title = recipe_json["title"]
        image = recipe_json["image"]
        summary = recipe_json["summary"]
        recipe_string = json.dumps(recipe_json)

        try:
            db.execute(
                "INSERT INTO recipes (spoon_id, title, image, summary, recipe_information) VALUES(?, ?, ?, ?, ?)",
                spoon_id, title, image, summary, recipe_string)
        except ValueError:
            pass # If the recipe already exists, this is fine
        try:
            favorites = db.execute("SELECT spoon_id FROM favorites WHERE user_id = ?", session["user_id"])
            existing_fav = False
            for element in favorites:
                if element["spoon_id"] == spoon_id:
                    existing_fav = True
                else:
                    pass # If spoon_id doesn't match, it's fine
            if not existing_fav:
                db.execute("INSERT INTO favorites (user_id, spoon_id) VALUES(?, ?)", session["user_id"], spoon_id)
            else:
                pass # If it's already a favorite, this is fine.
        except ValueError:
            return apology(f"favorite could not be saved", 400)
        return render_template("recipe.html", recipe_information=recipe_json)

    # If get, then show the recipe
    else:
        return render_template("recipe.html", recipe_information=session["random_recipe"])


@app.route("/favorites", methods=["GET", "POST"])
def favorites():
    """Show a list of all the user's favorites; let the user remove favorites from the list"""
    if request.method == 'POST':
        # Remove a favorite
        if request.form.get("remove_favorite") and request.form.get("remove_favorite").startswith("remove"):
            spoon_id = request.form.get("remove_favorite").split("_")[1]
            print(spoon_id)
            try:
                db.execute("DELETE FROM favorites WHERE user_id = ? and spoon_id = ?", session["user_id"], spoon_id)
            except ValueError:
                return apology("Could not remove favorite")
            return redirect("/favorites")

        # Show a recipe
        elif request.form.get("view_recipe").startswith('view'):
            spoon_id = request.form.get("view_recipe").split("_")[1]
            recipe_json = retrieve_recipe_data(database=db, spoon_id=spoon_id)
            return render_template("recipe.html", recipe_information=recipe_json)

    else:
        # Show the favorites page
        favorites = db.execute(
            "SELECT spoon_id, title, image, summary FROM recipes WHERE spoon_id IN (SELECT spoon_id FROM favorites WHERE user_id = ?)",
            session["user_id"])

        return render_template("favorites.html", favorites=favorites)
