# Generated by Django 3.0.8 on 2020-08-03 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0007_dish_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dish_calories',
            field=models.FloatField(null=True),
        ),
    ]
