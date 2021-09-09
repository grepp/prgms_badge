from django.urls import path
from .views import dark_profile, light_profile

urlpatterns = [
    path('dark/<str:cover_name>', dark_profile),
    path('light/<str:cover_name>', light_profile),
]
