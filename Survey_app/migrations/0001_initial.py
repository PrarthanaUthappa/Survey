# Generated by Django 5.0.7 on 2025-02-18 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254)),
                ('Created_Time', models.DateTimeField(auto_now_add=True)),
                ('Link', models.URLField()),
            ],
        ),
    ]
