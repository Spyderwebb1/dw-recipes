# Generated by Django 3.1.4 on 2021-02-07 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymeals', '0017_auto_20210206_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeinstruction',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_instructions', to='mymeals.recipe'),
        ),
    ]
