from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import view_dashboard
from .views_registro_empleados import registrar_empleado 
from .views_registro_vehiculo import registrar_vehiculo


urlpatterns = [
    path('login/', LoginView.as_view(template_name='parqueadero/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('dashboard/', view_dashboard.entrada_salida_vehiculo, name='dashboard'),
    path('registrar-empleado/', registrar_empleado, name='registrar_empleado'),
    path('registrar-vehiculo/', registrar_vehiculo, name='registrar_vehiculo'),
    
]