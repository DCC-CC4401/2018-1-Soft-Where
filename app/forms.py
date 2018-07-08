from django.forms import ModelForm
from django.contrib.auth.models import User
from app.models import Usuario

class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = {'username'}
        fields = {'first_name', 'last_name', 'email', 'password'}

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = {'rut', 'foto_link'}
