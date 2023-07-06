# Generated by Django 4.2.2 on 2023-07-05 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_recipe_categoryingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coreingredient',
            name='categoryingredient',
        ),
        migrations.AddField(
            model_name='categoryingredient',
            name='coreingredient',
            field=models.ManyToManyField(blank=True, related_name='coreingredient', to='recipe.coreingredient'),
        ),
    ]
