# Generated by Django 4.2.2 on 2023-07-05 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_categoryingredient_coreingredient_categoryingredient'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
    ]
