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
    path('filtrar_prestamos', views.filtrar_prestamos, name='filtrar_prestamos'),
    re_path(r'^searchArticulos/$', views.search_articulos, name='searchArticulos'),
    # re_path(r'^cambiar_estado_pendientes/$', views.cambiar_estado_pendientes, name='cambiar_estado_pendientes'),
    path('profile', views.user_profile, name='userProfile'),
    path('articulo', views.ficha_articulo, name='articulo'),
]
