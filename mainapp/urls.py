from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet

# Create router and register our viewset
router = DefaultRouter()
router.register(r'videos', VideoViewSet)

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]