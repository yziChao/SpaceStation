from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Categoria, Producto, Perfil

# *********************************************************************************************************#
#                                                                                                          #
# INSTRUCCIONES PARA EL ALUMNO, PUEDES SEGUIR EL VIDEO TUTORIAL, COMPLETAR EL CODIGO E INCORPORAR EL TUYO: #
#                                                                                                          #
# https://drive.google.com/drive/folders/1ObwMnpKmCXVbq3SMwJKlSRE0PCn0buk8?usp=drive_link                  #
#                                                                                                          #
# *********************************************************************************************************#

# LA PAGINA MANTENEDOR DE PRODUCTOS:
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [
            'categoria',
            'nombre',
            'descripcion',
            'precio',
            'descuento_subscriptor',
            'descuento_oferta',
            'imagen',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'imagen': forms.FileInput(attrs={'style': 'display:none;'}),
        }
        labels = {
            'nombre': 'Nombre',
            'descuento_subscriptor': 'Subscriptor(%)',
            'descuento_oferta': 'Oferta(%)',
        }

# El formulario de bodega está listo, no necesitas modificarlo
class BodegaForm(Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría')
    producto = forms.ModelChoiceField(queryset=Producto.objects.none(), label='Producto')
    cantidad = forms.IntegerField(label='Cantidad')
    class Meta:
        fields = '__all__'

# El formulario de ingreso está listo, no necesitas modificarlo
class IngresarForm(Form):
    username = forms.CharField(widget=forms.TextInput(), label="Cuenta")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

# LA PAGINA DE REGISTRO DE NUEVO CLIENTE:
class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("password1")
        contraseña2 = cleaned_data.get("password2")

        if contraseña and contraseña2 and contraseña != contraseña2:
            self.add_error('password2', "Las contraseñas no coinciden")

        return cleaned_data


# LA PAGINA DE REGISTRO DE NUEVO CLIENTE Y MIS DATOS:
class RegistroPerfilForm(ModelForm):

    class Meta:
        model = Perfil
        fields = ('rut','direccion','imagen', 'subscrito')
        exclude = ('tipo_usuario',)
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'imagen': forms.FileInput(attrs={'style': 'displaynone;'}),
        }
        labels = {
            'rut': 'RUT',
            'direccion': 'Direccion',
            'imagen': 'Foto',
            'subscrito': 'Suscribirse'
        }
# LA PAGINA MIS DATOS Y MANTENEDOR DE USUARIOS:
class UsuarioForm(ModelForm):
   class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'email': 'E-mail',
        }


# LA PAGINA MANTENEDOR DE USUARIOS:
class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ('tipo_usuario', 'rut', 'direccion', 'subscrito', 'imagen')
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'imagen': forms.FileInput(attrs={'style': 'displaynone;'}),
        }
