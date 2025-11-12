from django.urls import include, path

from rest_framework.routers import DefaultRouter

from reviews_app.api.views import ReviewListCreateAPIView


router = DefaultRouter()
router.register(r'reviews', ReviewListCreateAPIView, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
