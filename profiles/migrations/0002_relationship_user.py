# Generated by Django 3.2 on 2021-05-16 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='relationship',
            name='user',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
