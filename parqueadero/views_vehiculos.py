from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .forms import VehiculoForm
from .models import Vehiculo, RegistroAsignacion

@login_required
def vehiculos_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        action = request.GET.get('action')
        if action == 'list':
            try:
                vehiculos = Vehiculo.objects.all()
                vehiculos_data = []
                for vehiculo in vehiculos:
                    # Buscar la asignación de celda para este vehículo
                    celda_info = "Sin asignar"
                    try:
                        asignacion = RegistroAsignacion.objects.get(vehiculo=vehiculo)
                        celda_info = asignacion.celda.numero
                    except RegistroAsignacion.DoesNotExist:
                        pass

                    vehiculos_data.append({
                        'id': vehiculo.id_vehiculo,
                        'placa': vehiculo.placa,
                        'marca': vehiculo.marca,
                        'propietario': vehiculo.usuario.nombre if vehiculo.usuario else 'Sin propietario',
                        'celda': celda_info
                    })
                
                return JsonResponse({'vehiculos': vehiculos_data})
                
            except Exception as e:
                print(f"Error en list: {str(e)}")
                return JsonResponse({'error': str(e)})

        if request.method == 'POST':
            form = VehiculoForm(request.POST)
            if form.is_valid():
                vehiculo = form.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'errors': form.errors})

        if request.method == 'DELETE':
            vehiculo_id = request.GET.get('id')
            try:
                vehiculo = Vehiculo.objects.get(id_vehiculo=vehiculo_id)  # Cambiado de id a id_vehiculo
                vehiculo.delete()
                return JsonResponse({'status': 'success'})
            except Vehiculo.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Vehículo no encontrado'})

        elif action == 'search':
            query = request.GET.get('query', '').upper()  # Convertimos a mayúsculas
            vehiculos = Vehiculo.objects.filter(placa__iexact=query)  # Búsqueda exacta por placa
            vehiculos_data = []
            for vehiculo in vehiculos:
                # Buscar la asignación de celda para este vehículo
                celda_info = "Sin asignar"
                try:
                    asignacion = RegistroAsignacion.objects.get(vehiculo=vehiculo)
                    celda_info = asignacion.celda.numero
                except RegistroAsignacion.DoesNotExist:
                    pass

                vehiculos_data.append({
                    'id': vehiculo.id_vehiculo,
                    'placa': vehiculo.placa,
                    'marca': vehiculo.marca,
                    'propietario': vehiculo.usuario.nombre if vehiculo.usuario else 'Sin propietario',
                    'celda': celda_info
                })
            return JsonResponse({'vehiculos': vehiculos_data})

    form = VehiculoForm()
    return render(request, 'parqueadero/vehiculos.html', {'form': form})