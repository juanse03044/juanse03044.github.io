from django.urls import path
from . import views
from .views import exportar_excel, exportar_pdf
from .views import carga_masiva_general

urlpatterns = [

    path('', views.inicio, name="inicio"),

    # AUTH
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
    path('perfil/password/', views.cambiar_password_view, name='cambiar_password'),

    # 📋 LISTAS
    path('administradores/', views.listaAdministradores.as_view(), name='listaAdministradores'),
    path('eventos/', views.listaEventos.as_view(), name='listaEventos'),
    path('tipoEvento/', views.listaTipoEvento.as_view(), name='listaTipoEvento'),  # ✅ ARREGLADO
    path('horarios/', views.listaHorarios.as_view(), name='listaHorarios'),

    path('invitados/', views.ListaInvitados.as_view(), name='listaInvitados'),
    path('recursos/', views.listaRecursos.as_view(), name='listaRecursos'),
    path('usuarios/', views.listaUsuarios.as_view(), name='listaUsuarios'),

    # ➕ CREAR
    path('administradores/crear/', views.createAdministradores.as_view(), name='crearAdministrador'),
    path('eventos/crear/', views.createEventos.as_view(), name='crearEvento'),
    path('tipoEvento/crear/', views.createTipoEventos.as_view(), name='crearTipoEvento'),  # ✅
    path('horarios/crear/', views.CreateHorarios.as_view(), name='crearHorario'),
    path('invitados/crear/', views.CreateInvitados.as_view(), name='crearInvitado'),
    path('recursos/crear/', views.createRecursos.as_view(), name='crearRecurso'),
    path('usuarios/crear/', views.createUsuarios.as_view(), name='crearUsuario'),

    # ✏️ EDITAR
    path('administradores/editar/<int:pk>/', views.updateAdministradores.as_view(), name='editarAdministrador'),
    path('eventos/editar/<int:pk>/', views.updateEventos.as_view(), name='editarEvento'),
    path('tipoEvento/editar/<int:pk>/', views.updateTipoEventos.as_view(), name='editarTipoEvento'),  # ✅
    path('horarios/editar/<int:pk>/', views.UpdateHorarios.as_view(), name='editarHorario'),
    path('invitados/editar/<int:pk>/', views.UpdateInvitados.as_view(), name='editarInvitado'),
    path('recursos/editar/<int:pk>/', views.updateRecursos.as_view(), name='editarRecurso'),
    path('usuarios/editar/<int:pk>/', views.updateUsuarios.as_view(), name='editarUsuario'),

    # ❌ ELIMINAR
    path('administradores/eliminar/<int:pk>/', views.deleteAdministradores.as_view(), name='eliminarAdministrador'),
    path('eventos/eliminar/<int:pk>/', views.deleteEventos.as_view(), name='eliminarEvento'),
    path('tipoEvento/eliminar/<int:pk>/', views.deleteTipoEvento.as_view(), name='eliminarTipoEvento'),  # ✅
    path('horarios/eliminar/<int:pk>/', views.deleteHorarios.as_view(), name='eliminarHorario'),
  path('invitados/eliminar/<int:pk>/', views.EliminarInvitado.as_view(), name='eliminarInvitado'),
    path('recursos/eliminar/<int:pk>/', views.deleteRecursos.as_view(), name='eliminarRecurso'),
    path('usuarios/eliminar/<int:pk>/', views.deleteUsuarios.as_view(), name='eliminarUsuario'),

    # 📊 REPORTE
    path('reporte/', views.reporte_eventos, name='reporte_eventos'),

    # 📊 DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
    # 📥 EXPORTACIÓN
    path('exportar-excel/', exportar_excel, name='exportar_excel'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf'),

    # CARGA MASIVA 
    path('carga-masiva/', carga_masiva_general, name='carga_masiva_general'),
    
    
    path('cotizaciones/', views.listaCotizaciones.as_view(), name='listaCotizaciones'),
    path('cotizaciones/crear/', views.CreateCotizacion.as_view(), name='crearCotizacion'),
    path('cotizaciones/editar/<int:pk>/', views.updateCotizacion.as_view(), name='editarCotizacion'),
    path('cotizaciones/eliminar/<int:pk>/', views.deleteCotizacion.as_view(), name='eliminarCotizacion'),
]