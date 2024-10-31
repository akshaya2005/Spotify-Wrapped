from django.urls import path
from . import views
from .views import intro_view

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name=''),
    path('intro/', intro_view, name='intro'),  # Ensure you have a corresponding view
]