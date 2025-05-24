from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import CustomUser
from .forms import EmpleadoForm
from django.db.models import Q

def es_administrador(user):
    return user.is_authenticated and (user.is_superuser or user.user_type == 'administrador')

@user_passes_test(es_administrador)
@login_required
def empleados_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            # Lógica para registrar empleado
            form = EmpleadoForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        
        action = request.GET.get('action')
        if action == 'list':
            # Lógica para listar empleados
            empleados = CustomUser.objects.filter(user_type='empleado')
            return JsonResponse({'empleados': list(empleados.values())})
        elif action == 'search':
            # Lógica para buscar empleado
            query = request.GET.get('query', '')
            empleados = CustomUser.objects.filter(
                Q(username__icontains=query) | 
                Q(first_name__icontains=query),
                user_type='empleado'
            )
            return JsonResponse({'empleados': list(empleados.values())})
        elif request.method == 'DELETE':
            empleado_id = request.GET.get('id')
            try:
                empleado = CustomUser.objects.get(id=empleado_id, user_type='empleado')
                empleado.delete()
                return JsonResponse({'status': 'success'})
            except CustomUser.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Empleado no encontrado'})
    
    form = EmpleadoForm()
    return render(request, 'parqueadero/empleados.html', {'form': form})