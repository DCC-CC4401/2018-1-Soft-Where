from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='loginPage'),
    path('register', views.register_page, name='registerPage'),
    path('loginUser', views.login_user, name='login'),
    path('testpage', views.test_page, name='testPage'),
    path('adminlanding', views.admin_landing, name='adminLanding'),
    path('cambiar_estado_pendientes', views.cambiar_estado_pendientes, name='cambiar_estado_pendientes'),
    re_path(r'^searchArticulos/$', views.search_articulos, name='searchArticulos'),
]
