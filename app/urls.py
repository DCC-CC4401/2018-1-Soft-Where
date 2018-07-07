from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='loginPage'),
    path('register', views.register_page, name='registerPage'),
    path('registerUser', views.create_user, name='register'),
    path('loginUser', views.login_user, name='login'),
    re_path('.*', views.index),
]
