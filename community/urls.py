from django.urls import path
from .views import *

urlpatterns = [
    path('community/communityadd/',CommunityView.as_view(),name="community"),
    path('communityfollow/<int:pk>/',FollowCommunity.as_view(),name="communityfollow")
]