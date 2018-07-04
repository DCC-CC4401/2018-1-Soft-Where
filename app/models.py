from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=13, help_text="Rut con formato 12.345.678-9 aceptado")
    foto_link = models.CharField(max_length=100, help_text="Link a la foto perfíl del usuario")

    """
    class Meta:
        permissions = (
            ("permission_name", "Texto que describe que hace el permiso"),
        )
    """
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Usuario.objects.create(user=instance)
        instance.usuario.save()

    def __str__(self):
        return self.user.username

class Articulo(models.Model):
    DISPONIBLE = 1
    ENPRESTAMO = 2
    ENREPARACION = 3
    PERDIDO = 4
    ESTADOS = (
        (DISPONIBLE, "Disponible"),
        (ENPRESTAMO, "En préstamo"),
        (ENREPARACION, "En reparación"),
        (PERDIDO, "Perdido")
    )

    #Fields
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, help_text="Nombre del artículo")
    link_foto = models.CharField(max_length=100, help_text="Link a la foto del artículo")
    text_desct = models.CharField(max_length=100, help_text="Texto descriptivo del artículo")
    estado = models.PositiveSmallIntegerField(ESTADOS, help_text="Estado posible para un articulo o espacio")

    #Meta
    class Meta:
        ordering = ["id"]

    #Methods
    def __str__(self):
        return self.id

    #def get_absolute_url(self):

class Espacio(models.Model):
    VIGENTE = 1
    CADUCADO = 2
    PERDIDO = 3
    ESTADOS = (
        (VIGENTE, "Vigente"),
        (CADUCADO, "Caducado"),
        (PERDIDO, "Perdido")
    )
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, help_text="Nombre del espacio")
    link_foto = models.CharField(max_length=100, help_text="Link a la foto del espacio")
    text_desct = models.CharField(max_length=100, help_text="Texto descriptivo del espacio")
    estado = models.PositiveSmallIntegerField(ESTADOS, help_text="Estado posible para un articulo o espacio")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.id

class PedidoArticulo(models.Model):
    PENDIENTE = 1
    RECHAZADA = 2
    CONCRETADA = 3
    ESTADOS = (
        (PENDIENTE, "Pendiente"),
        (RECHAZADA, "Rechazada"),
        (CONCRETADA, "Concretada")
    )
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    id_articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True)
    estado = models.PositiveSmallIntegerField(ESTADOS, help_text="Estado posible para un articulo o espacio")

    class Meta:
        ordering = ["fecha_pedido", "id_usuario"]

    def __str__(self):
        return self.id_articulo + self.id_usuario

class PedidoEspacio(models.Model):
    PENDIENTE = 1
    RECHAZADA = 2
    CONCRETADA = 3
    ESTADOS = (
        (PENDIENTE, "Pendiente"),
        (RECHAZADA, "Rechazada"),
        (CONCRETADA, "Concretada")
    )
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    id_espacio = models.ForeignKey('Espacio', on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True)
    estado = models.PositiveSmallIntegerField(ESTADOS, help_text="Estado posible para un articulo o espacio")

    class Meta:
        ordering = ["fecha_pedido", "id_usuario"]

    def __str__(self):
        return self.id_espacio + self.id_usuario
