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
    id_tipo = models.ForeignKey('TipoEvento', models.DO_NOTHING, db_column='id_tipo')
    def __str__(self):
     return self.titulo
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
    id_usuario = models.ForeignKey('Usuarios', on_delete=models.CASCADE, null=True, blank=True)

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

   