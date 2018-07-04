from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Usuario, Articulo, Espacio, PedidoArticulo, PedidoEspacio
# Register your models here.


class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = (UsuarioInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Articulo)
admin.site.register(Espacio)
admin.site.register(PedidoArticulo)
admin.site.register(PedidoEspacio)

