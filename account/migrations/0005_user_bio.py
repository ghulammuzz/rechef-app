# Generated by Django 4.2.2 on 2023-06-10 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_interest_remove_user_interest_user_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]