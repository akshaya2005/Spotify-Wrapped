from django.urls import path
from . import views
from django.views.i18n import set_language

app_name = 'frontend'

urlpatterns = [
    path('register/', views.register_view, name='register'),  # Registration URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('set_language/', set_language, name='set_language'),  # Language change view
]
