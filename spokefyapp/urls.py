from . import views
from django.urls import path

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("spotify/", views.spotify_log, name="spotify_log"),
    path("spotify/redirect", views.spotify_callback, name="spotify_callback"),

]
