from django.db import models
import datetime

class Usuario(models.Model):
    rut = models.CharField(primary_key=True, max_length=13, help_text="Rut con formato 12.345.678-9 aceptado")
    nombre = models.CharField(max_length=100, help_text="Nombre del usuario")
    correo = models.EmailField()
    foto_link = models.CharField(max_length=100, help_text="Link a la foto perfíl del usuario")
    clave = models.CharField( 'password' , max_length=128, help_text="Clave del usuario")

    def __str__(self):
        return self.nombre

    """
    def set_password(self, raw_password):
        import random
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.clave = '%s$%s$%s' % (algo, salt, hsh)
    """

class Articulo(models.Model):
    #Fields
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, help_text="Nombre del artículo")
    link_foto = models.CharField(max_length=100, help_text="Link a la foto del artículo")
    text_desct = models.CharField(max_length=100, help_text="Texto descriptivo del artículo")
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE, null=False)

    #Meta
    #class Meta:

    #Methods
    def __str__(self):
        return self.nombre

    #def get_absolute_url(self):

class Espacio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, help_text="Nombre del espacio")
    link_foto = models.CharField(max_length=100, help_text="Link a la foto del espacio")
    text_desct = models.CharField(max_length=100, help_text="Texto descriptivo del espacio")
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE)

    #class Meta:

    #Methods
    def __str__(self):
        return self.nombre

    #def get_absolute_url(self):

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=100, help_text="Estado posible para un articulo o espacio")

class PedidoArticulo(models.Model):
    rut_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    id_articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True)
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE)

class PedidoEspacio(models.Model):
    rut_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    id_espacio = models.ForeignKey('Espacio', on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True)
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE)