from django import forms
from django.core.exceptions import ValidationError
from .models import Usuarios


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Correo',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400',
            'placeholder': 'correo@ejemplo.com',
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400',
            'placeholder': 'Contraseña',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                usuario = Usuarios.objects.get(email=email)
            except Usuarios.DoesNotExist:
                raise ValidationError('Correo o contraseña incorrectos.')

            from django.contrib.auth.hashers import check_password
            if not check_password(password, usuario.password):
                raise ValidationError('Correo o contraseña incorrectos.')

            if usuario.estado.lower() != 'activo':
                raise ValidationError('Tu cuenta está inactiva. Contacta al administrador.')

            self.usuario = usuario
        return cleaned_data


class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400',
            'placeholder': 'Mínimo 8 caracteres',
        })
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400',
            'placeholder': 'Repite la contraseña',
        })
    )

    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'email']
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400', 'placeholder': 'Apellido'}),
            'email':    forms.EmailInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400', 'placeholder': 'correo@ejemplo.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuarios.objects.filter(email=email).exists():
            raise ValidationError('Este correo ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data

    def save(self, commit=True, rol_seleccionado='usuario'):
        """
        Guarda el usuario con el rol seleccionado en el formulario de registro.
        rol_seleccionado puede ser 'admin' o 'usuario' (cliente).
        """
        from django.contrib.auth.hashers import make_password
        usuario = super().save(commit=False)
        usuario.password = make_password(self.cleaned_data['password1'])
        # Usar el rol que llegó del formulario (tarjeta de selección)
        ROLES_VALIDOS = ['admin', 'usuario']
        usuario.rol = rol_seleccionado if rol_seleccionado in ROLES_VALIDOS else 'usuario'
        usuario.estado = 'activo'
        if commit:
            usuario.save()
        return usuario


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'email']
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'apellido': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'email':    forms.EmailInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuarios.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este correo ya está en uso.')
        return email


class CambiarPasswordForm(forms.Form):
    password_actual = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'})
    )
    password_nueva = forms.CharField(
        label='Nueva contraseña',
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'})
    )
    password_confirmacion = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'})
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password_nueva') != cleaned_data.get('password_confirmacion'):
            raise ValidationError('Las contraseñas nuevas no coinciden.')
        return cleaned_data


class GestionUsuarioForm(forms.ModelForm):
    ROL_CHOICES = [('admin', 'Administrador'), ('usuario', 'Cliente')]
    ESTADO_CHOICES = [('activo', 'Activo'), ('inactivo', 'Inactivo')]

    rol = forms.ChoiceField(
        choices=ROL_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'})
    )
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'})
    )

    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'email', 'rol', 'estado', 'password']
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'apellido': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'email':    forms.EmailInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'password': forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
        }

    def save(self, commit=True):
        from django.contrib.auth.hashers import make_password
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            usuario.password = make_password(password)
        else:
            if usuario.pk:
                usuario.password = Usuarios.objects.get(pk=usuario.pk).password

        if commit:
            usuario.save()
        return usuario

from .models import Administradores, Eventos, Horarios, Invitados, Recursos, TipoEvento


class EventoForm(forms.ModelForm):
    class Meta:
        model = Eventos   # ✅ IMPORTANTE plural
        fields = '__all__'


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        fields = '__all__'


class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administradores
        fields = '__all__'



class HorariosForm(forms.ModelForm):
    class Meta:
        model = Horarios
        fields = '__all__'


import re
from django.core.exceptions import ValidationError

class InvitadosForm(forms.ModelForm):
    class Meta:
        model = Invitados
        fields = ['evento', 'nombre', 'apellido', 'telefono']  # ya no 'usuario'
        widgets = {
            'evento': forms.Select(attrs={'class': '...'}),
            'nombre': forms.TextInput(attrs={'class': '...'}),
            'apellido': forms.TextInput(attrs={'class': '...'}),
            'telefono': forms.TextInput(attrs={'class': '...'}),
        }

    def _validar_nombre(self, valor, campo):
        valor = valor.strip()
        if not valor:
            raise ValidationError(f'El {campo} no puede estar vacío.')
        # Solo letras (incluye tildes y ñ), espacios y guiones
        patron = r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s\-]+$'
        if not re.match(patron, valor):
            raise ValidationError(f'El {campo} solo puede contener letras.')
        if len(valor) < 2:
            raise ValidationError(f'El {campo} es demasiado corto.')
        return valor

    def clean_nombre(self):
        return self._validar_nombre(self.cleaned_data.get('nombre', ''), 'nombre')

    def clean_apellido(self):
        return self._validar_nombre(self.cleaned_data.get('apellido', ''), 'apellido')


class RecursosForm(forms.ModelForm):
    class Meta:
        model = Recursos
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError('El nombre no puede estar vacío.')

        query = Recursos.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise ValidationError('Ya existe un recurso con este nombre.')
        return nombre
    
    
from .models import Cotizacion

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        exclude = ['precio_total']
        widgets = {
            'evento': forms.Select(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'tipo_lugar': forms.Select(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'vestimenta': forms.Select(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'tipo_comida': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400', 'placeholder': 'Ej: Buffet, Bandeja paisa...'}),
            'tipo_bebida': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400', 'placeholder': 'Ej: Licor, Gaseosas, Jugos...'}),
            'precio_base': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
        }