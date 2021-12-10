from typing import List
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from datetime import datetime

from .models import User, Category, Listing


def index(request, page = 1):

    p = page - 1
    lpp = 5
    auctions = Listing.objects.all().order_by("-id")[0+p*lpp:lpp+p*lpp]

    auctions = Listing.objects.all().order_by("-id")
    p = Paginator(auctions, lpp)
    page_obj = p.get_page(page)
    pages = p.get_elided_page_range(page_obj.number)



    return render(request, "auctions/index.html", {
        "test": page,
        "auctions": auctions,
        'page_obj': page_obj,
        "pages": pages,
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
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url = "/login")
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        cat = request.POST["category"]
        try:
            cat = Category.objects.get(category = cat)
        except:
            return render(request, "auctions/create.html", {
            "categories": Category.objects.all(),
            "message": "Something is not yes: Prosze wybrać kategorię",
            "description": description,
            "title": title,
            "cat": cat,
            })
        try:
            price = float(request.POST["price"])
        except:
            return render(request, "auctions/create.html", {
            "categories": Category.objects.all(),
            "message": "Something is not yes: Cos nie tak z ceną",
            })

        newList = Listing(title=title, description=description, starting_price = price, pub_date = datetime.today(), user = request.user)
        newList.save()
        newList.categories.add(cat)
        return HttpResponse("Done")
        pass

    else:
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all(),
            "message": "Strona podstawowa"
        })


def snippet():
    for i in range(10):
        obj = Listing.objects.get(pk=6)
        obj.pk = None
        obj.title = f"Różdżka {i+1}"
        obj.save()