from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('user/<int:pk>', views.user_profile, name='user_profile'),
    path('twitter_feed/', views.twitter_feed, name='twitter_feed'),
    path('like_tweet/<int:pk>', views.like_tweet, name='like_tweet'),
    path('retweet/<int:pk>', views.retweet, name='retweet'),
]