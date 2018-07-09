from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from .models import Articulo, PedidoEspacio, Usuario, Espacio, PedidoArticulo
from .forms import UserForm, UsuarioForm
import json


# Muestra el indice
def index(request):
    context = {'articulos': 'inicio'}
    context = {**context, **user_context(request)} # Esto fusiona dos dict
    return render(request, 'landing-page.html', context)


# Pagina de test
def test_page(request):
    return render(request, 'adminlanding.html')


# Retorna los datos basicos del usuario logeado
def user_context(request):
    current_user=Usuario.objects.get(user=request.user)
    context = {'name': str(current_user),
               'rut' : current_user.rut,
               'mail' : current_user.user.email}
    return context


def user_profile(request):
    context = user_context(request)
    return render(request, 'user_profile.html', context)


# Muestra la pagina de login si el usuario no esta logeado
def login_page(request):
    if request.user.is_authenticated:
        # TODO: Otra pagina o algo así
        return index(request)
    else:
        return render(request, 'UserSys/login.html')


# Muestra la pagina de registro si el usuario no esta logeado
@transaction.atomic
def register_page(request):
    if request.user.is_authenticated:
        # TODO: Otra pagina o algo así
        return index(request)
    else:
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            usuario_form = UsuarioForm(request.POST)
            if user_form.is_valid() and usuario_form.is_valid():
                email = user_form.data['email']
                user = user_form.save(commit=False)
                user.username = email
                user.save()
                user.refresh_from_db()
                usuario_form = UsuarioForm(request.POST, instance=user.usuario)
                usuario_form.full_clean()
                usuario_form.save()
                return render(request, 'landing-page.html', user_context(request))
        else:
            user_form = UserForm()
            usuario_form = UsuarioForm()
        return render(request, 'UserSys/register.html',
                      {**{
                          'user_form': user_form,
                          'usuario_form': usuario_form
                      }, **user_context(request)})


# Logea al usuario dentro de la página y lo lleva al landing page que corresponda.
def login_user(request):
    user = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        # TODO: Llevar al landing page admin/user segun el tipo de usuario.
        return render(request, 'landing-page.html', user_context(request))
    else:
        # TODO: Crear la pagina de error (?)
        return render(request, 'fail-page.html')


# Desloguea al usuario y lo lleva al inicio.
@login_required
def logout_user(request):
    logout(request)
    return render(request, 'stater-page.html')


def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def search_articulos(request):
    search_term = request.GET.get('search')
    results = []
    if search_term == "":
        results = []
    elif isNum(search_term):
        results = Articulo.objects.filter(id=search_term) | Articulo.objects.filter(nombre__icontains=search_term)
    else:
        results = Articulo.objects.filter(nombre__icontains=search_term)
    context = {'articulos': results}
    context = {**context, **user_context(request)} # Esto fusiona dos dict
    return render(request, 'resultados_articulos.html', context)


def admin_landing(request):
    context = {**{'usuarios' : Usuario.objects.all(),
               'articulos' : Articulo.objects.all(),
               'espacios' : Espacio.objects.all(),
               'pedidoespacios' : PedidoEspacio.objects.all(),
               'pedidoarticulos' : PedidoArticulo.objects.all(), },
               **user_context(request)}
    return render(request, 'adminlanding.html', context)

def cambiar_estado_pendientes(request):
    if(request.method == 'POST'):
        for id in request.POST.getlist('id'):
            if 'entregado' in request.POST:
                pedidoespacio = PedidoEspacio.objects.get(id_espacio=id)
                pedidoespacio.estado = 3
                pedidoespacio.save()
            elif 'rechazado' in request.POST:
                pedidoespacio = PedidoEspacio.objects.get(id_espacio=id)
                pedidoespacio.estado = 2
                pedidoespacio.save()
        context = {**{'usuarios' : Usuario.objects.all(),
                   'articulos' : Articulo.objects.all(),
                   'espacios' : Espacio.objects.all(),
                   'pedidoespacios' : PedidoEspacio.objects.all().order_by('fecha_pedido'),
                   'pedidoarticulos' : PedidoArticulo.objects.all().order_by('fecha_pedido')},
                **user_context(request)}
        return render(request, 'adminlanding.html', context)

def filtrar_prestamos(request):
    if(request.method == 'POST'):
        pedidoarticulosfiltrados = PedidoArticulo.objects.all()
        if 'todo' in request.POST:
            pedidoarticulosfiltrados = PedidoArticulo.objects.all()
        elif 'vigentes' in request.POST:
            pedidoarticulosfiltrados =PedidoArticulo.objects.filter(estado=PedidoArticulo.VIGENTE)
        elif 'caducados' in request.POST:
            pedidoarticulosfiltrados =PedidoArticulo.objects.filter(estado=PedidoArticulo.CADUCADO)
        elif 'perdidos' in request.POST:
            pedidoarticulosfiltrados =PedidoArticulo.objects.filter(estado=PedidoArticulo.PERDIDO)

        context = {**{'usuarios' : Usuario.objects.all(),
                   'articulos' : Articulo.objects.all(),
                   'espacios' : Espacio.objects.all(),
                   'pedidoespacios' : PedidoEspacio.objects.all().order_by('fecha_pedido'),
                   'pedidoarticulos' : pedidoarticulosfiltrados.order_by('fecha_pedido')},
            **user_context(request)}
        return render(request, 'adminlanding.html', context)
