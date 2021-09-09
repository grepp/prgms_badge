from django.urls import path
from .views import dark_profile

urlpatterns = [
    path('dark/<str:cover_name>', dark_profile),
]
