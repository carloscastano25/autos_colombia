from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import view_dashboard
from .views_empleados import empleados_view
from .views_vehiculos import vehiculos_view
from .views_usuarios import  usuarios_view
from .views_celdas import celdas_view


urlpatterns = [
    path('login/', LoginView.as_view(template_name='parqueadero/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('dashboard/', view_dashboard.entrada_salida_vehiculo, name='dashboard'),
    # URLs de empleados
    path('empleados/', empleados_view, name='empleados'),
    # URLs de usuarios
    path('usuarios/', usuarios_view, name='usuarios'),
    # URLs existentes
    path('vehiculos/', vehiculos_view, name='vehiculos'),
    path('celdas/', celdas_view, name='celdas'),
]