# Generated by Django 4.2.2 on 2023-07-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0012_remove_recipe_categoryingredient'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='categoryingredient',
            field=models.ManyToManyField(blank=True, related_name='categoryingredient', to='recipe.categoryingredient'),
        ),
    ]
