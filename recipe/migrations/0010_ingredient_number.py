# Generated by Django 4.2.2 on 2023-06-11 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_method_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
