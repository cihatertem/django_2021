# Generated by Django 4.0.1 on 2022-01-14 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='social_twitter',
            field=models.URLField(blank=True, default='https://twitter.com/', null=True),
        ),
    ]