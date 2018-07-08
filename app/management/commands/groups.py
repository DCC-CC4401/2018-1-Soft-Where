from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app.models import Usuario


class Command(BaseCommand):
    help = 'Crea el grupo de administradores - Usar solo post migrations'

    def handle(self, *args, **options):
        try:
            administradores, created = Group.objects.get_or_create(name='Administradores')
            ct = ContentType.objects.get_for_model(Usuario)
            permission = Permission.objects.create(codename='is_admin',
                                                   name='Super permiso para hacer todo lo que haga un admin',
                                                   content_type=ct)
            administradores.permissions.add(permission)
            administradores.save()
        except:
            raise CommandError('algo raro paso, posiblemente el grupo ya existe')

        self.stdout.write(self.style.SUCCESS('Se crearon los grupos exitosamente.'))
