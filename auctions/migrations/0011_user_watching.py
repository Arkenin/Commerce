# Generated by Django 3.2.7 on 2021-12-13 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_actual_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watching',
            field=models.ManyToManyField(blank=True, related_name='users', to='auctions.Listing'),
        ),
    ]
