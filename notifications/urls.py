from django.urls import path
from .views import *

urlpatterns = [
     path('message/',Notifications.as_view(), name='notifications'),
]