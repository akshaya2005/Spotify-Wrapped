from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.intro_view, name='dashboard'),
    path('register/', views.register_view, name='register'),  # Registration URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
