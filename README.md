# CS50x Final Project: RecipeVault

## Basic Information
**Angela Niederberger**

GitHub username: Alessine<br>
EdX username: Alessine<br>
Greifensee, Switzerland<br>

Video Demo: [https://youtu.be/2aFnBx5FbdY](https://youtu.be/2aFnBx5FbdY)<br>
Date of Recording: 2. January 2025

## Description

### Summary
RecipeVault is a flask web app that allows logged in users to browse through recipe suggestions and save them to their page of favorite recipes. The recipe data displayed in the app is provided via the Spoonacular API and stored in a Sqlite database. The main technologies used are Python, Flask, Jinja, Sqlite, CSS, HTML and JavaScript.

### Features

#### Navigation
In order to allow for easy navigation, the site features a top navigation bar. When logged out, there are three clickable items:

* On the left there is a link that reloads the main page.
* In the right hand corner there are links leading to the registration and login pages.

When logged in, there are three slightly different clickable items:
* The main link on the left leads to the welcome page.
* There is a second tab right next to this link leading to the favorites page.
* In the right hand corner there is a log out link.

Depending on the width of the screen, the navigation collapses into a drop-down menu. The navigation (as well as a minimalistic footer) are defined in the file [layout.html](./templates/layout.html).

#### Login and Registration
When accessing the site for the first time, users need to register. All they need to do is choose a user name and password. The username and hashed password are stored in a database table. On subsequent visits, the users are required to log in.

If a user attempts to submit a registration or login form without filling in all the required information, an error screen is shown. The files used to set up these pages are: [login.html](./templates/login.html), [register.html](./templates/register.html) and [apology.html](./templates/apology.html).

#### Welcome Page
Once logged in, users are shown the welcome page, which addresses them by name and shows a recipe suggestion, including a summary and an image. The user can then choose to either generate a new suggestion, or visit the recipe page with detailed information about the suggested dish. Here's the file that displays the welcome page: [welcome.html](./templates/welcome.html).

#### Recipe Page
The recipe page is structured into three sections. In the top section the user will find the basic information that was already shown on the welcome page: the recipe title, the summary and an image. In addition to this, there are a few labels that qualify certain dishes as vegetarian, gluten free, etc. Just below the image, there is a button which allows the user to store this recipe as a favorite.

In the section on the lower left, there is a table showing all the ingredients needed to cook the recipe. In the third section on the lower right hand side, the user will find all the cooking instructions. This whole set up is defined in the file [recipe.html](./templates/recipe.html).

#### Favorites Page
As long as a user has not chosen any favorite recipes, this page just shows a note telling the user that there are so far no favorites. Once at least one recipe has been marked as this user's favorite, this page shows a similar recipe teaser that is shown on the welcome page, including the recipe title, the summary and an image. Below the image are two buttons that let the user either remove the recipe from the favorites or view the full recipe. The favorites page is displayed via the following file: [favorites.html](./templates/favorites.html).

### Technology

#### Python
The app script is written in Python (version 3.12.8) and can be viewed in the files [app.py](./app.py) and [helpers.py](helpers.py). In addition to the Python standard library, the following libraries are needed:

- Flask (3.1.0)
- Flask Session (0.8.0)
- requests (2.32.3)
- security from Werkzeug (3.1.3)
- SQL from CS50 (9.4.0)

All these requirements are documented in the [requirements file](./requirements.txt).

#### Spoonacular API
The [Spoonacular API](https://spoonacular.com/food-api/docs) is a REST API that offers a free plan with which it is possible to retrieve a wealth of information on thousands of recipes, including images. The data is returned in JSON format, it is public and it can be used for a multitude of purposes.

For this project, only the `Get Random Recipes` endpoint was accessed. A typical API response is shown in this [file](./static/api_example_response.txt).

#### Database Schema
To store the user and recipe data, a [sqlite database](./recipevault.db) was used. The database schema looks as follows:

<img src="./static/database_schema.png" alt="Screenshot of the Database Structure" width="800">

#### Navigation
For the navigation bar and footer a bootstrap template was used, which defines the necessary CSS and JavaScript to make the navigation responsive. Further information on this (including the Bootstrap Documentation) can be found [here](http://getbootstrap.com/docs/5.3/).

### Design
To give the app a beautiful, clean look, the following design choices were implemented using CSS and JavaScript:

#### Responsive Design
To ensure that the app is also shown correctly on smaller screens (and particularly on mobile devices), the <b>CSS flexbox approach</b> was used for structuring and positioning of elements. A few examples:
* The sizing of images happens in relation to the screen size.
* The buttons are positioned flexibly.
* The width of the columns of the ingredients table is dependent on the screen size.

In addition to this of course the site navigation is also responsive to the screen size, as mentioned before.

#### Stylesheet
The [stylesheet](./static/styles.css) ensures that the look of the app is chosen intentionally and that elements of the same type always look the same way. The most obvious style choices are the following:
* <b>Images</b> should always be presented in the same way: 1px border, with a 10px border radius and a maximum width of 700px. The width is constrained by the size of the image provided by the Spoonacular API.
* <b>Buttons</b> should look uniform: 1px border, with a border radius of 5px and padding of 7px. Text color, background color and border color are always identical. The positioning needs to be flexible.
* <b>Lists and tables</b> are styled to work well with the flexbox approach.


#### Colors
The use of the following simple color palette ensures that the look of the app is clean:
* <b>Text</b>: brown (#4a3831)
* <b>Borders</b>: petrol (#006165)
* <b>Button background and navigation</b>: light grey (#f8f9fA)
* <b>Button background on hover</b>: dark grey (#e9edf0)


### Difficulties and Further Development
Some of the shortcomings of the current version of the app are:
* **Content Formatting**: The content is provided by the Spoonacular API in the form of text, including HTML tags (for example ordered lists for the cooking instructions). In some cases, the tags were implemented in a very clean way and, when applied in the app, they give the recipe page an even more structured look. In other cases, the HTML tags are faulty and can create problems when rendering the text. Since the formatting is not uniform, it would require a lot of effort to clean this text and find a format that works well for the majority of recipes.

* **Recipe Updates**: The recipes coming from the Spoonacular API are not static. Spoonacular users can make adjustments and updates. However, in the database used for this project, these updates would not be reflected, because a recipe can only be stored once. Therefore, the recipes would slowly get outdated over time. To fix this issue, it would be necessary to introduce regular updates of the database, checking the existing information against the content returned by the API for every saved recipe.

### Outlook
There is a wealth of possibilities to introduce additional features in this app. For example, it would be useful to develop a **search functionality**, where user would be able to request recipes from the API based on certain criteria, for example only vegetarian recipes or similar.

Another feature that would add value would be to add a few onboarding questions in the registration process, which would allow for **personalized recipe suggestions**. For example, users could specify that they are only interested in low-sugar recipes.

One more option for further development could be a print button on the recipe page, which would **generate a pdf output** of the recipe page. This could be handy when wanting to try a recipe.
