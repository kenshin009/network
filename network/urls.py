
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('profile-view/<str:user>',views.profile_view,name='profile_view'),
    path('create-post',views.create_post,name='create_post'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
