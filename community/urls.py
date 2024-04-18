from django.urls import path
from .views import *

urlpatterns = [
    path('communityadd/',CommunityAPIView.as_view(),name="community"),
    path('communities/<int:community_id>/', CommunityDetailAPIView.as_view(), name='community-detail'),
     path('communities/<int:community_id>/follow/', FollowCommunityAPIView.as_view(), name='follow-community'),
     path('community-posts/', CommunityPostAPIView.as_view(), name='community_post_list'),
    path('like/<int:post_id>/', LikePostAPIView.as_view(), name='like-post'),
    path('post/<int:post_id>/comments/', CommentCreateView.as_view(), name='post-comments'),
    path('post/<int:post_id>/comments/<int:comment_id>/',CommentDetailView.as_view(), name='comment-detail'),
]