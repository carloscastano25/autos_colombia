from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .forms import CeldaForm
from .models import Celda, RegistroAsignacion

@login_required
def celdas_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            form = CeldaForm(request.POST)
            if form.is_valid():
                celda = form.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        
        action = request.GET.get('action')
        if action == 'list':
            celdas = Celda.objects.all()
            celdas_data = []
            for celda in celdas:
                data = {
                    'id': celda.id,
                    'numero': celda.numero,
                    'disponible': celda.disponible,
                    'vehiculo': None
                }
                # Si la celda está ocupada, obtener información del vehículo
                if not celda.disponible:
                    try:
                        asignacion = RegistroAsignacion.objects.get(celda=celda)
                        data['vehiculo'] = {
                            'placa': asignacion.vehiculo.placa,
                            'marca': asignacion.vehiculo.marca,
                            'propietario': asignacion.vehiculo.usuario.nombre
                        }
                    except RegistroAsignacion.DoesNotExist:
                        pass
                celdas_data.append(data)
            return JsonResponse({'celdas': celdas_data})
            
        elif action == 'search':
            query = request.GET.get('query', '')
            celdas = Celda.objects.filter(numero__icontains=query)
            celdas_data = []
            for celda in celdas:
                data = {
                    'id': celda.id,
                    'numero': celda.numero,
                    'disponible': celda.disponible,
                    'vehiculo': None
                }
                if not celda.disponible:
                    try:
                        asignacion = RegistroAsignacion.objects.get(celda=celda)
                        data['vehiculo'] = {
                            'placa': asignacion.vehiculo.placa,
                            'marca': asignacion.vehiculo.marca,
                            'propietario': asignacion.vehiculo.usuario.nombre
                        }
                    except RegistroAsignacion.DoesNotExist:
                        pass
                celdas_data.append(data)
            return JsonResponse({'celdas': celdas_data})
        
        if request.method == 'DELETE':
            celda_id = request.GET.get('id')
            try:
                celda = Celda.objects.get(id=celda_id)
                # Verificar si la celda está ocupada
                if not celda.disponible:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'No se puede eliminar una celda ocupada'
                    })
                celda.delete()
                return JsonResponse({'status': 'success'})
            except Celda.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Celda no encontrada'})
    
    form = CeldaForm()
    return render(request, 'parqueadero/celdas.html', {'form': form})