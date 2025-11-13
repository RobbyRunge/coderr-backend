from django.urls import path

from base_info_app.api.views import BaseInfoAPIView


urlpatterns = [
    path('base-info/', BaseInfoAPIView.as_view(), name='base-info'),
]
