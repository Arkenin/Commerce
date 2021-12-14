from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField


class User(AbstractUser):
    watching = ManyToManyField('Listing', blank=True, related_name="users")
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    starting_price = models.FloatField()
    actual_price = models.FloatField(default=-1)
    description = models.CharField(max_length=1024)
    picture_url = models.URLField(null=True)
    pub_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self.actual_price <= 0:
            self.actual_price = self.starting_price
        super().save(*args, *kwargs)

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_date = models.DateTimeField()
    bid_value = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.auction}: {self.bid_value}'

    def save(self, *args, **kwargs):
        super().save(self, *args, *kwargs)
        self.auction.actual_price = self.bid_value
        self.auction.save()
        

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    com_date = models.DateTimeField()
    text = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.com_date}, {self.text}'

class Category(models.Model):
    category = models.CharField(max_length = 64)
    auctions = models.ManyToManyField(Listing, blank=True, related_name="categories")

    def __str__(self) -> str:
        return self.category





