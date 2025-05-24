from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import UsuarioForm
from .models import Usuario
from django.db.models import Q

@login_required
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario {usuario.nombre} registrado exitosamente')
            return redirect('registrar_vehiculo')  # Redirige a la vista de registro de vehículo
    else:
        form = UsuarioForm()
    return render(request, 'parqueadero/registrar_usuario.html', {'form': form})

@login_required
def usuarios_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'DELETE':
            usuario_id = request.GET.get('id')
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                usuario.delete()
                return JsonResponse({'status': 'success'})
            except Usuario.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'})
        
        if request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid():
                usuario = form.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        
        action = request.GET.get('action')
        if action == 'list':
            usuarios = Usuario.objects.all()
            return JsonResponse({'usuarios': list(usuarios.values())})
        elif action == 'search':
            query = request.GET.get('query', '')
            usuarios = Usuario.objects.filter(
                Q(nombre__icontains=query) | 
                Q(num_doc__icontains=query)
            )
            return JsonResponse({'usuarios': list(usuarios.values())})
    
    form = UsuarioForm()
    return render(request, 'parqueadero/usuarios.html', {'form': form})