from django.urls import path
from .views import *

app_name = 'wraps'  # Add this to name the app, which can be helpful for namespacing

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),  # Ensure this matches
]