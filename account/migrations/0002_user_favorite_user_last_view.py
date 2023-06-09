# Generated by Django 4.2.2 on 2023-07-06 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0020_remove_ingredient_coreingredient_and_more'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite', to='recipe.recipe'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_view',
            field=models.ManyToManyField(blank=True, related_name='last_view', to='recipe.recipe'),
        ),
    ]
