# Generated by Django 4.2.2 on 2023-06-30 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_recipe_updated_at'),
        ('account', '0007_user_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_view',
            field=models.ManyToManyField(blank=True, related_name='last_view', to='recipe.recipe'),
        ),
    ]