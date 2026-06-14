from django.contrib import admin
from .models import Administradores, Eventos, Horarios, Invitados, Recursos, TipoEvento, Usuarios

admin.site.register(Administradores)
admin.site.register(Eventos)
admin.site.register(Horarios)
admin.site.register(Invitados)
admin.site.register(Recursos)
admin.site.register(TipoEvento)
admin.site.register(Usuarios)
