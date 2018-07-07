from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from app.models import Articulo
import json

# Muestra el indice

def index(request):
    context = {'articulos': 'inicio'}
    return render(request, 'landing-page.html', context)

# Pagina de test
def test_page(request):
    return render(request, 'landing-page.html')


# Muestra la pagina de login si el usuario no esta logeado
def login_page(request):
    if request.user.is_authenticated:
        # TODO: Otra pagina o algo así
        return index(request)
    else:
        return render(request, 'UserSys/login.html')


# Muestra la pagina de registro si el usuario no esta logeado
def register_page(request):
    if request.user.is_authenticated:
        # TODO: Otra pagina o algo así
        return index(request)
    else:
        return render(request, 'UserSys/register.html')


# Crea un usuario y lleva al landing page.
def create_user(request):
    # TODO: Los 5543 errores que deberia tirar un creador de usuarios estandar.
    # TODO: Dejar bien delimitados las cosas que definen un user...
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name'] # Esto es el Rut
    last_name = request.POST['last_name'] # Esto es el NOMBRE COMPLETO
    # Se fija el username como el mail de la persona por requisito 2.
    user = User.objects.create_user(username, username, password)
    user.last_name = last_name
    user.first_name = first_name
    user.save()
    return render(request, 'landing-page.html')


# Logea al usuario dentro de la página y lo lleva al landing page que corresponda.
def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # TODO: Llevar al landing page admin/user segun el tipo de usuario.
        return render(request, 'landing-page.html')
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
    return render(request, 'resultados_articulos.html', context)

