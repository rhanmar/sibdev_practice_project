# Generated by Django 3.0.8 on 2020-08-13 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0016_auto_20200810_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='photo',
            field=models.ImageField(help_text='Фотография заведения', null=True, upload_to=''),
        ),
    ]
