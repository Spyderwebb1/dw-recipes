# Generated by Django 3.1.4 on 2021-02-15 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymeals', '0018_auto_20210207_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
    ]
