from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page>", views.index, name="index"),
    path("watchlist/<int:page>", views.index, {'name':'watchlist'}, name="watchlist"),
    path("watchlist/", views.index, {'name':'watchlist'}, name="watchlist"),
    path("watchlist_add/<int:pk>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:pk>", views.watchlist_remove, name="watchlist_remove"),
    path("end_auction/<int:pk>", views.end_auction, name="end_auction"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("auction/<int:nr>", views.auction, name="auction")
    
]
#name="watchlist", 