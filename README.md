DW Recipes

Summary:
This is a recipe sharing application that is built with the Django framework and JavaScript.  Users can register to use the web application.  Once signed in, the users have access to a variety of recipes that other users have contributed to the web application.  Users also have the ability to create and edit their own recipes and share with other users.  Photos of recipes can be uploaded through the web application to show your creations!

Additional features:  
- Users can favorite any recipes shared across the web application.  They can access their favorite recipes through a nav menu item link.  
- Users also have access to a grocery list generator tool.  This is available by clicking the 'Lists' nav element.  Users can create a grocery list and add items and quantities using a form.  The best feature is that users can add items to their grocery list when viewing a recipe.  Each recipe page has a list of ingredients required for that particular recipe.  The user can then select any or all of the recipe ingredients and choose a grocery list to add the items to.
- Users can sort their grocery lists by alphabetical order or by recipe
- Users can edit/save their grocery lists


File list and description:

- forms.py: contains model forms and other forms needed for project. Also includes custom usercreation form.
- views.py: contains the logic of the application for the different views.  Includes function wrappers requiring user to be logged-in in order to access certain views.
- models.py: contains 8 models mapping to tables of data that will be used by the web application
- admin.py: gives access to models in the Django admin interface
- urls.py: contains the url patterns recognised by this application and maps to the correct views
- requirements.txt - Python packages that need to be installed in order to run this web application

Static files
- images:  backgound image used across web application
- styles.css: extra styling used across web application

Templates 
- create-list.html: form to create list title and a list of user's grocery lists (if created)
- create-recipe.html: form for creating recipe (including javascript for dynamically adding ingredients to form)
- favorite-recipes.html: displays list of user's favorite recipes
- index.html: homepage of web application
- layout.html: base template of web application includes the navbar and background image.
- my-grocery-list.html: user's grocery list page. User can add items and quantities using the form.  User can edit items in list using AJAX without refreshing entire page.  Sorting list alphabetically or by recipe is available.
- recipe-detail.html: recipe detail page.  If user is the author of the recipe, user can edit recipe.  User can also select ingredients to add to their grocery list using this view.
- recipes.html: list of all recipes available in web application.  Displayed by category.
- register.html:  user registration page
- logged_out.html: logged out page
- login.html:  Login page

Be sure to install Python packages in requirements.txt file before running the web application.
