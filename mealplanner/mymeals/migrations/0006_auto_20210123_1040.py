# Generated by Django 3.1.4 on 2021-01-23 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymeals', '0005_auto_20210111_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('WE', 'Western'), ('AS', 'Asian'), ('ME', 'Middle Eastern'), ('IT', 'Italian'), ('OT', 'Other')], default='OT', max_length=2),
        ),
    ]
