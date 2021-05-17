from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create-list", views.create_list, name="create-list"),
    path("my-grocery-list/<int:list_id>/<sort>", views.my_list_detail, name="my-grocery-list"),
    path("my-grocery-list-ingredient/<int:pk>/remove", views.delete_grocery_list_ingredient, name="my-grocery-list-ingredient-remove"),
    path("my-grocery-list-ingredient/<int:pk>/update", views.update_grocery_list_ingredient, name="my-grocery-list-ingredient-update"),
    
    path("recipes", views.recipes, name="recipes"),
    path("create-recipe", views.create_recipe, name="create-recipe"), 
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe-detail"),
    path("update-recipe/<int:recipe_id>/", views.update_recipe, name="recipe-update"),
    path("recipes-add-to-favorites/<int:recipe_id>/", views.recipe_add_to_favorites, name="recipes-add-to-favorites"),
    path("recipes-remove-from-favorites/<int:recipe_id>/", views.recipe_remove_from_favorites, name="recipes-remove-from-favorites"),
    path("my-favorite-recipes", views.my_favorite_recipes, name="my-favorite-recipes"),

    path("register", views.register, name="register"),
]