from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from decimal import Decimal
from .models import Vehiculo, RegistroPago

VALOR_MENSUALIDAD = Decimal('45000')

@login_required
def pagos_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        action = request.GET.get('action')
        
        if action == 'buscar_vehiculo':
            placa = request.GET.get('placa', '').upper()
            try:
                vehiculo = Vehiculo.objects.get(placa=placa)
                esta_al_dia = vehiculo.esta_al_dia()
                fecha_vencimiento = vehiculo.fecha_vencimiento()
                
                # Calcular meses de mora y monto a pagar
                meses_mora = 0
                if not esta_al_dia:
                    dias_mora = (now() - fecha_vencimiento).days
                    meses_mora = (dias_mora // 30) + 1
                
                monto_a_pagar = VALOR_MENSUALIDAD * meses_mora if meses_mora > 0 else VALOR_MENSUALIDAD

                return JsonResponse({
                    'status': 'success',
                    'vehiculo_id': vehiculo.id_vehiculo,
                    'placa': vehiculo.placa,
                    'propietario': vehiculo.usuario.nombre if vehiculo.usuario else 'Sin propietario',
                    'esta_al_dia': esta_al_dia,
                    'fecha_vencimiento': fecha_vencimiento.strftime('%Y-%m-%d'),
                    'meses_mora': meses_mora,
                    'monto_a_pagar': float(monto_a_pagar)
                })
            except Vehiculo.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Vehículo no encontrado'
                })

        elif action == 'registrar_pago':
            if request.method == 'POST':
                try:
                    vehiculo_id = request.POST.get('vehiculo_id')
                    meses = int(request.POST.get('meses', 1))
                    monto = Decimal(request.POST.get('monto'))
                    
                    vehiculo = Vehiculo.objects.get(id_vehiculo=vehiculo_id)
                    
                    # Crear el registro de pago
                    pago = RegistroPago.objects.create(
                        vehiculo=vehiculo,
                        empleado=request.user,
                        monto=monto,
                        meses_pagados=meses
                    )
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Pago registrado exitosamente'
                    })
                except Exception as e:
                    return JsonResponse({
                        'status': 'error',
                        'message': str(e)
                    })

        elif action == 'historial':
            try:
                # Obtener todos los vehículos
                vehiculos = Vehiculo.objects.all()
                vehiculos_data = []
                
                for vehiculo in vehiculos:
                    esta_al_dia = vehiculo.esta_al_dia()
                    fecha_vencimiento = vehiculo.fecha_vencimiento()
                    
                    # Calcular meses de mora si aplica
                    meses_mora = 0
                    if not esta_al_dia:
                        dias_mora = (now() - fecha_vencimiento).days
                        meses_mora = (dias_mora // 30) + 1
                    
                    # Obtener el último pago
                    ultimo_pago = vehiculo.pagos.order_by('-fecha_pago').first()
                    
                    vehiculos_data.append({
                        'placa': vehiculo.placa,
                        'propietario': vehiculo.usuario.nombre if vehiculo.usuario else 'Sin propietario',
                        'esta_al_dia': esta_al_dia,
                        'fecha_vencimiento': fecha_vencimiento.strftime('%Y-%m-%d'),
                        'meses_mora': meses_mora,
                        'ultimo_pago': ultimo_pago.fecha_pago.strftime('%Y-%m-%d') if ultimo_pago else 'Sin pagos',
                        'monto_adeudado': float(VALOR_MENSUALIDAD * meses_mora) if meses_mora > 0 else 0
                    })
                
                return JsonResponse({'vehiculos': vehiculos_data})
            except Exception as e:
                return JsonResponse({'error': str(e)})

    return render(request, 'parqueadero/pagos.html')