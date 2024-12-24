from django.urls import path
from .views import *

urlpatterns = [
    path("login/",loginPage,name="login"),
    path("register/",registerPage,name="register"),
    path("logout/",logoutUser,name="logout"),
    path("", home, name="home" ),
    path("room/<str:pk>/", room, name="room" ),
    path("create-room/", create_room, name="create-room"),
    path("update-room/<str:pk>", update_room, name="update-room"),
    path("delete/<str:pk>", deleteRoom, name="delete-room"),
]