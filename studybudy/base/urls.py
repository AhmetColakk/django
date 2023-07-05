from django.urls import path
from . import views

app_name = "base"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("room/<str:pk>", views.room, name="room"),
    path("create-room/", views.create_room, name="create-room"),
    path("update-room/<str:id>", views.update_room, name="update-room"),
    path("delete-room/<str:id>", views.delete_room, name="delete-room"),
]
