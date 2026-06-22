
from django.db import models


class Administradores(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    def __str__(self):
     return f"{self.nombre} {self.apellido}"

    class Meta:
        managed = True
        db_table = 'administradores'


class Eventos(models.Model):
    id_evento = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    fecha = models.DateField()
    lugar = models.CharField(max_length=100)

    cantidad_invitados = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

    id_tipo = models.ForeignKey(
        'TipoEvento',
        models.DO_NOTHING,
        db_column='id_tipo'
    )

    creado_por = models.ForeignKey(
        'Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_creados'
    )

    class Meta:
        managed = True
        db_table = 'eventos'

class Horarios(models.Model):
    id_horario = models.AutoField(primary_key=True)
    
    evento = models.ForeignKey('Eventos', on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'horarios'

class Invitados(models.Model):
    usuario = models.ForeignKey(
        'Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    evento = models.ForeignKey('Eventos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    class Meta:
        db_table = 'invitados'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Recursos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    tipoEvento = models.ForeignKey('TipoEvento', on_delete=models.CASCADE)  # ✅ CORREGIDO

    def __str__(self):
        return self.nombre


class TipoEvento(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre  # 🔥 clave para el select

    class Meta:
        managed = True
        db_table = 'tipo_evento'


class Usuarios(models.Model):

    ROLES = [
        ('admin', 'Administrador'),
        ('usuario', 'Usuario'),
    ]

    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)  # 🔥 ESTE FALTA
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

   
   
   
class Cotizacion(models.Model):
    TIPO_LUGAR = [
        ('casa', 'Casa particular'),
        ('salon', 'Salón de eventos'),
        ('casa_eventos', 'Casa de eventos'),
        ('exterior', 'Exterior'),
    ]
    VESTIMENTA = [
        ('formal', 'Formal'),
        ('semiformal', 'Semiformal'),
        ('casual', 'Casual'),
        ('tematico', 'Temático'),
    ]

    evento = models.OneToOneField('Eventos', on_delete=models.CASCADE, related_name='cotizacion')
    tipo_lugar = models.CharField(max_length=20, choices=TIPO_LUGAR)
    hay_ninos = models.BooleanField(default=False)
    hay_adultos_mayores = models.BooleanField(default=False)
    vestimenta = models.CharField(max_length=20, choices=VESTIMENTA)
    
    # Servicios
    incluye_dj = models.BooleanField(default=False)
    incluye_camarero = models.BooleanField(default=False)
    incluye_decoracion = models.BooleanField(default=False)
    
    # Comida y bebida
    tipo_comida = models.CharField(max_length=100, blank=True)
    tipo_bebida = models.CharField(max_length=100, blank=True)
    
    # Presupuesto
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'cotizaciones'

    def calcular_precio(self):
        total = self.precio_base
        if self.incluye_dj: total += 500000
        if self.incluye_camarero: total += 300000
        if self.incluye_decoracion: total += 400000
        self.precio_total = total
        return total