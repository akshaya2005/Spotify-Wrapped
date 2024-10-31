# stats/urls.py
from django.urls import path
from . import views

app_name = 'stats'  # Set app_name to match the namespace
urlpatterns = [
    path('', views.stats_view, name='stats'),  # This name should match what you’re redirecting to
]
