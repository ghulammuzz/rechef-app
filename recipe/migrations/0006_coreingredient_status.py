# Generated by Django 4.2.2 on 2023-07-05 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_recipe_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='coreingredient',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Accepted', max_length=10),
        ),
    ]
