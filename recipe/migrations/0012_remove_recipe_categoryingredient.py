# Generated by Django 4.2.2 on 2023-07-05 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_recipe_categoryingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='categoryingredient',
        ),
    ]