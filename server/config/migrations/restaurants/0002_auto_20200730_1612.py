# Generated by Django 3.0.8 on 2020-07-30 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='photo',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]
