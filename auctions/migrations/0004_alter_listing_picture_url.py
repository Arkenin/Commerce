# Generated by Django 3.2.7 on 2021-11-01 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211101_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='picture_url',
            field=models.URLField(null=True),
        ),
    ]
