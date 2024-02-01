from django.urls import path
from .views import RegistrationView
from . import views

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('explore/', views.ExploreUsers.as_view(), name='explore_users'),
    path('<int:user_id>/follow/', views.FollowUser.as_view(), name='follow_user'),
    path('<int:user_id>/unfollow/', views.UnFollowUser.as_view(), name='unfollow_user'),
    path('<str:username>/followers/', views.UserFollowers.as_view(), name='user_followers'),
    path('<str:username>/following/', views.UserFollowing.as_view(), name='user_following'),
    path('search/', views.Search.as_view(), name='user_following'),
    path('<str:username>/', views.UserProfile.as_view(), name='user_profile'),
]