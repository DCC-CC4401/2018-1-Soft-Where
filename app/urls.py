from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.landing_page, name='index'),
    path('register', views.register_page, name='registerPage'),
    path('login', views.login_page, name='login'),
    path('testpage', views.test_page, name='testPage'),
    # path('adminlanding', views.admin_landing, name='adminLanding'),
    path('cambiar_estado_pendientes', views.cambiar_estado_pendientes, name='cambiar_estado_pendientes'),
    path('filtrar_prestamos', views.filtrar_prestamos, name='filtrar_prestamos'),
    re_path(r'^searchArticulos/$', views.search_articulos, name='searchArticulos'),
    # re_path(r'^cambiar_estado_pendientes/$', views.cambiar_estado_pendientes, name='cambiar_estado_pendientes'),
    path('ficha_articulo', views.ficha_articulo, name='ficha_articulo'),
    path('profile', views.user_profile, name='user_profile'),
    path('deleteprestamos', views.delete_prestamos, name='delete_prestamos')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
