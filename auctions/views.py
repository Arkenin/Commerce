from typing import List
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.template.defaulttags import register

from datetime import datetime

from .models import Bid, Comment, User, Category, Listing


def index(request, page = 1):

    p = page - 1
    lpp = 5

    auctions = Listing.objects.all().order_by("-id")


    p = Paginator(auctions, lpp)
    page_obj = p.get_page(page)
    pages = p.get_elided_page_range(page_obj.number)

    max_prices = {}
    for auc in page_obj:
        max_prices[auc.pk] = get_auction_max_price(auc)



    return render(request, "auctions/index.html", {
        "test": page,
        "auctions": auctions,
        'page_obj': page_obj,
        "pages": pages,
        "max_prices": max_prices,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html", {
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def auction(request, nr):
    auc = Listing.objects.get(pk=nr)
    act_max_bid = get_auction_max_price(auc)


    

    message = None
    if request.method == 'POST':
        if 'search-bt' in request.POST:
            print(">>>>przycisk search")
        if 'bid-bt' in request.POST:
            print(">>>>przycisk bid")  
            bid_value = float(request.POST["bid_value"])
            

            if act_max_bid == None or bid_value > act_max_bid:
                bid = Bid(
                    user = request.user,
                    bid_date = datetime.today(),
                    bid_value = bid_value,
                    auction = auc
                )
                bid.save()
                act_max_bid = bid_value
                messages.success(request, "Bid placed.")
            else:
                messages.warning(request, "Your bid must be higher than actual price.")

                

        if 'comment-bt' in request.POST:
            print(">>>>przycisk comment")
            comment = request.POST["comment"]
            newComment = Comment(
                auction = Listing.objects.get(pk=nr),
                com_date = datetime.today(),
                text = comment,
                user = request.user)
            newComment.save()
            message = "Comment added."
            messages.success(request, "Comment added.")


    a = Listing.objects.get(pk=nr)

    return render(request, "auctions/auction.html", {
        "auc": Listing.objects.get(pk=nr),
        "message": message,
        "comments": Comment.objects.filter(auction = auc),
        "price": act_max_bid,
    })

@login_required(login_url = "/login")
def create(request):
    error = False
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        cat = request.POST["category"]
        try:
            cat = Category.objects.get(category = cat)
        except:
            messages.error(request, "Please choose at least one category.")
            error = True
        try:
            price = float(request.POST["price"])
        except:
            messages.error(request, "Invalid price.")
            error = True

        if error:
            return render(request, "auctions/create.html", {
                "categories": Category.objects.all(),
                "description": description,
                "title": title,
                "cat": cat,
                })

        newList = Listing(title=title, description=description, starting_price = price, pub_date = datetime.today(), user = request.user)
        newList.save()
        newList.categories.add(cat)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all(),
            "message": "Strona podstawowa"
        })


def get_auction_max_price(auc):
    act_max_bid = Bid.objects.filter(auction = auc).order_by('-bid_value').first()
    if act_max_bid == None:
        act_max_bid = auc.starting_price
    else:
        act_max_bid = act_max_bid.bid_value
    return act_max_bid

def snippet():
    for i in range(10):
        obj = Listing.objects.get(pk=6)
        obj.pk = None
        obj.title = f"Różdżka {i+1}"
        obj.save()



