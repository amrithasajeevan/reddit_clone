from django.urls import path
from . import views


urlpatterns = [
    path('image/', views.Images.as_view(), name='feed'),
    path('<int:image_id>/', views.ImageDetail.as_view(), name='image_detail'),
    path('<int:image_id>/likes/', views.LikeImage.as_view(), name='like_image'),
    path('<int:image_id>/unlikes/', views.UnLikeImage.as_view(), name='unlike_image'),
    path('<int:image_id>/comments/', views.CommentOnImage.as_view(), name='comment_image'),
    path('<int:image_id>/comments/<int:comment_id>/', views.ModerateComments.as_view(), name='moderate_comments'),
    path('comment/<int:comment_id>/', views.Comments.as_view(), name='comment'),
    path('search/', views.Search.as_view(), name='search'),
]

