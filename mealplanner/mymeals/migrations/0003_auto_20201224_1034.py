# Generated by Django 3.1.4 on 2020-12-24 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymeals', '0002_category_grocerylist_ingredient_meal_mylistingredient_recipe_recipeingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mylistingredient',
            name='grocery_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_ingredients', to='mymeals.grocerylist'),
        ),
    ]
