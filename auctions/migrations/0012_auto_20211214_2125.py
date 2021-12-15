# Generated by Django 3.2.7 on 2021-12-14 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_user_watching'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='ended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_wins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_auctions', to=settings.AUTH_USER_MODEL),
        ),
    ]
