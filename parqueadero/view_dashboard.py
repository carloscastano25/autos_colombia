from django.shortcuts import render
from django.utils.timezone import now
from .models import RegistroVehiculo, Vehiculo

def entrada_salida_vehiculo(request):
    mensaje = None

    if request.method == 'POST':
        print(request.POST)  # Bloque de depuración: imprime los datos enviados por el formulario

        placa = request.POST.get('placa')
        if not placa:
            mensaje = "Por favor, ingrese una placa válida."
            return render(request, 'parqueadero/dashboard.html', {'mensaje': mensaje})

        vehiculo = Vehiculo.objects.filter(placa=placa).first()

        if not vehiculo:
            mensaje = "La placa ingresada no está registrada en el sistema."
        else:
            if 'entrada' in request.POST:
                if vehiculo.estado:  # Si el vehículo ya está adentro
                    mensaje = f"El vehículo con placa {placa} ya se encuentra adentro. Presione 'Salir' si desea registrar una salida."
                else:
                    vehiculo.estado = True  # Cambia el estado a "adentro"
                    vehiculo.save()
                    RegistroVehiculo.objects.create(
                        vehiculo=vehiculo,
                        tipo='entrada',
                        fecha_hora_ingreso=now()
                    )
                    mensaje = f"Ingreso exitoso para el vehículo con placa {placa}."
            elif 'salida' in request.POST:
                if not vehiculo.estado:  # Si el vehículo ya está afuera
                    mensaje = f"El vehículo con placa {placa} ya se encuentra afuera. Presione 'Ingresar' si desea registrar una entrada."
                else:
                    vehiculo.estado = False  # Cambia el estado a "afuera"
                    vehiculo.save()
                    registro = RegistroVehiculo.objects.filter(vehiculo=vehiculo, fecha_hora_salida__isnull=True).first()
                    if registro:
                        registro.fecha_hora_salida = now()
                        registro.save()
                    mensaje = f"Salida exitosa para el vehículo con placa {placa}."

    return render(request, 'parqueadero/dashboard.html', {'mensaje': mensaje})