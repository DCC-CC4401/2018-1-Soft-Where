from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from .models import Articulo, PedidoEspacio, Usuario, Espacio, PedidoArticulo
from .forms import UserForm, UsuarioForm


# Muestra el indice
def index(request):
    context = {'articulos': 'inicio'}
    if request.user.is_authenticated:
        context = {**context, **user_context(request)} # Esto fusiona dos dict
    else:
        return login_page(request)
    return render(request, 'landing-page.html', context)


# Pagina de test
def test_page(request):
    return render(request, 'adminlanding.html')


# Retorna los datos basicos del usuario logeado
def user_context(request):
    current_user = Usuario.objects.get(user=request.user)
    context = {'id': current_user.get_id(),
               'name': str(current_user),
               'rut' : current_user.rut,
               'mail' : current_user.user.email}
    return context


# TODO: :)
def user_profile(request):
    context = user_context(request)
    return render(request, 'user_profile.html', context)


@transaction.atomic
def login_page(request):
    if request.user.is_authenticated:
        # TODO: Otra pagina o algo así
        return index(request)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,
                                password=password,
                                request=request)
            if user is not None:
                login(request, user)
                return render(request, 'landing-page.html', user_context(request))
            else:
                # TODO: Mensaje de error por password
                return render(request, 'UserSys/login.html')
        # TODO: No se como se llega aqui...
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
                password = user_form.cleaned_data['password']
                user = user_form.save(commit=False)
                user.username = email
                user.set_password(raw_password=password)
                user.save()
                user.refresh_from_db()
                usuario_form = UsuarioForm(request.POST, instance=user.usuario)
                usuario_form.full_clean()
                usuario_form.save()
                username = user.username
                user = authenticate(username=username,
                                    password=password,
                                    request=request)
                if user is not None:
                    login(request, user)
                    return render(request, 'landing-page.html', user_context(request))
                return render(request, 'landing-page.html')
        else:
            user_form = UserForm()
            usuario_form = UsuarioForm()
        return render(request, 'UserSys/register.html',
                      {
                          'user_form': user_form,
                          'usuario_form': usuario_form}
                      )


@login_required
def update_user(request):
    # TODO: completar el cambio de password
    if request.method == 'POST':
        current_user = Usuario.objects.get(user=request.user)
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        username = current_user.username
        current_user.set_password(new_password)
        current_user.save()
        renewed_user = authenticate(username=username,
                                    password=new_password,
                                    request=request)
        if renewed_user is not None:
            login(request, renewed_user)
            return render(request, 'landing-page.html', user_context(request))



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


def ficha_articulo(request):
    if request.method == 'GET':
        articulo_id = request.GET['articulo_id']
        articulo = Articulo.objects.get(id=articulo_id)
        historial_reservas_articulo = PedidoArticulo.objects.filter(id_articulo=1).order_by('fecha_pedido')
        context = {'articulo' : articulo,
                   'historial_reservas': historial_reservas_articulo}
        return render(request, 'ficha-articulo.html', context)

@transaction.atomic
def pedir_articulo(request):
    if request.method == 'GET':
        articulo = Articulo.objects.get(id=request.GET['articulo_id'])
        articulo_id = articulo.id
        user_id = user_context(request).id
        if (articulo.estado == 1):
            PedidoArticulo.objects.create(id_articulo=articulo_id, id_usuario=user_id, estado=1)
        else:
            pass