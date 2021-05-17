from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Ingredient, RecipeIngredient, Recipe, MyListIngredient, GroceryList, RecipeInstruction

admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Recipe)
admin.site.register(MyListIngredient)
admin.site.register(GroceryList)
admin.site.register(RecipeInstruction)