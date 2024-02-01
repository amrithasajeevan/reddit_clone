from django.urls import path
from .views import *

urlpatterns = [
    path('communityadd/',CommunityView.as_view(),name="community")
]