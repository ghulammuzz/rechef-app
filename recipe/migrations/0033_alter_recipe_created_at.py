# Generated by Django 4.2.2 on 2023-07-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0032_recipe_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]