from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import EmpleadoForm

# Verificar que el usuario sea administrador
def es_administrador(user):
    return user.is_authenticated and (user.is_superuser or user.user_type == 'administrador')

@user_passes_test(es_administrador)
def registrar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirigir al dashboard después de registrar
    else:
        form = EmpleadoForm()
    return render(request, 'parqueadero/registrar_empleado.html', {'form': form})