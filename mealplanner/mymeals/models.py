from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


# Create a custom Django user model for more flexibility.  Remember to update settings file
# to override the default AUTH_USER_MODEL with the custom model
# DO THIS AT BEGINNING OF PROJECT BEFORE MAKING INITIAL MIGRATIONS
class User(AbstractUser):
    # Override AbstractUser default email field to be required field
    email = models.EmailField(_('email address'))
    favorite_recipes = models.ManyToManyField('Recipe')


class Category(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, blank=True, null=True, related_name='my_recipe_ingredients')

    def __str__(self):
        return f"{self.ingredient.name} x {self.quantity}"


class RecipeInstruction(models.Model):
    recipe_instruction = models.TextField()
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, null=True, related_name="recipe_instructions")
   

class Recipe(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    serves = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])


class MyListIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    grocery_list = models.ForeignKey('GroceryList', on_delete=models.CASCADE, related_name='my_ingredients')
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.ingredient.name



class GroceryList(models.Model):
    nickname = models.CharField(max_length=60)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_grocery_lists')
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('my-grocery-list', args=[str(self.id), 'az'])