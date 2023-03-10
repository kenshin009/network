
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('edit-post',views.edit_post,name='edit_post'),
    path('following',views.following,name='following'),
    path('follows',views.follows,name='follows'),
    path('posts/<int:post_id>',views.post_detail,name='post_detail'),
    path('like-posts',views.like_posts,name='like_posts'),
    path('like-post-detail/<int:post_id>',views.like_post_detail,name='like_post_detail'),
    path('profile-view/<str:user>',views.profile_view,name='profile_view'),
    path('create-post',views.create_post,name='create_post'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
