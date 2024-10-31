# login/urls.py
from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login_view, name='login'),  # URL for login view
    path('callback/', views.callback_view, name='callback'),  # URL for Spotify callback
]
