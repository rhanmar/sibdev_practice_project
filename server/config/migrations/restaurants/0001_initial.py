# Generated by Django 3.0.8 on 2020-07-30 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('photo', models.ImageField(upload_to='')),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('address', models.CharField(max_length=128)),
                ('average_cost', models.FloatField()),
                ('owner', models.CharField(max_length=32)),
                ('point', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.Point')),
            ],
        ),
    ]