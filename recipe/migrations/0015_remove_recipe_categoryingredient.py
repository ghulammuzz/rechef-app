# Generated by Django 4.2.2 on 2023-07-05 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0014_remove_coreingredient_categoryingredient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='categoryingredient',
        ),
    ]
