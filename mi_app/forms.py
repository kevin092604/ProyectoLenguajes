from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'Nombre',
            'Apellido',
            'Usuario',
            'Ncuenta',
            'Correo',
            'Contraseña',
        ]