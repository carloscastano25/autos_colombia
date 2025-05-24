from django.apps import AppConfig


class ParqueaderoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parqueadero'
    
    def ready(self):
        from django.db.utils import OperationalError, ProgrammingError
        from .models import Celda  # Asegúrate de que el modelo esté en el archivo models.py
        try:
            # Verifica si ya existen celdas
            if not Celda.objects.exists():
                for i in range(1, 101):  # Crear 100 celdas
                    Celda.objects.get_or_create(numero=str(i), disponible=True)
        except (OperationalError, ProgrammingError):
            # Evita errores si la base de datos no está migrada o aún no lista
            pass
        except Exception as e:
            print(f"Error inesperado al crear celdas: {e}")