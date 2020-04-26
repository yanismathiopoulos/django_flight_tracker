# Generated by Django 2.1.5 on 2020-04-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InputNumbers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_number', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OutputAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output_answer', models.FloatField()),
            ],
        ),
    ]