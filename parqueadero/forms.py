from django import forms
from .models import RegistroVehiculo, CustomUser, Vehiculo

class RegistroEntradaForm(forms.ModelForm):
    class Meta:
        model = RegistroVehiculo
        fields = ['vehiculo']

class RegistroSalidaForm(forms.ModelForm):
    class Meta:
        model = RegistroVehiculo
        fields = ['fecha_hora_salida']
        
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nombre', 'tipo_doc', 'num_doc', 'telefono', 'correo', 'user_type']
        widgets = {
            'user_type': forms.Select(choices=[('empleado', 'Empleado')]),  # Solo permitir empleados
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo_vehiculo', 'marca', 'color', 'propietario']  # Campos existentes en el modelo
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la placa'}),
            'tipo_vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la marca'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el color'}),
            'propietario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el propietario'}),
        }

