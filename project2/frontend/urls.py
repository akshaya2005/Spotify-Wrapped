from django.urls import path
from . import views
from .views import intro_view

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name=''),
    path('dashboard/', intro_view, name='dashboard'),
    # Ensure you have a corresponding view
]