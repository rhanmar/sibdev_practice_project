# Generated by Django 3.0.8 on 2020-08-05 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0012_auto_20200805_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='average_cost',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
