from django.urls import path, include
from .views import router

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
]
