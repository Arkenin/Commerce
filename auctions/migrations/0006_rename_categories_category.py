# Generated by Django 3.2.7 on 2021-11-01 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_categories_auctions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
    ]
