from django.urls import path
from . import views

app_name = 'frontend'
from django.conf.urls.i18n import set_language


urlpatterns = [
    path('register/', views.register_view, name='register'),  # Registration URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('i18n/setlang/', set_language, name='set_language'),
]