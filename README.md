# AutosColombia

AutosColombia es un sistema de gestión de parqueaderos desarrollado con Django. Permite registrar la entrada y salida de vehículos, gestionar empleados y usuarios, y realizar un seguimiento de las celdas disponibles en el parqueadero.

## Características

- Registro de entrada y salida de vehículos.
- Gestión de empleados y usuarios.
- Asignación de celdas de parqueo.
- Panel de administración para gestionar el sistema.
- Interfaz amigable y responsiva.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes programas en tu computadora:

- **Python 3.8 o superior**: Necesario para ejecutar el proyecto Django.
- **pip**: Administrador de paquetes de Python (generalmente incluido con Python).
- **Git**: Para clonar el repositorio desde GitHub.

---

## Instalación

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local:

### 1. Clonar el Repositorio

Clona el repositorio desde GitHub: 


1. Crear y Activar un Entorno Virtual
Crea un entorno virtual para evitar conflictos con otras dependencias de Python: python -m venv venv

Activa el entorno virtual: venv\Scripts\activate

3. Instalar las Dependencias
Instala las dependencias necesarias para el proyecto desde el archivo pip install -r requirements.txt

### 4️⃣ Configurar el Archivo `.env`

Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes configuraciones:

```plaintext
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

Reemplaza tu_clave_secreta con una clave secreta generada para Django. Puedes generar una clave secreta usando Django Secret Key Generator.

5️⃣ Configurar la Base de Datos
Aplica las migraciones para crear la base de datos:

python manage.py makemigrations
python manage.py migrate

6️⃣ Crear un Superusuario
Crea un superusuario para acceder al panel de administración de Django:
python manage.py createsuperuser

Sigue las instrucciones para ingresar un nombre de usuario, correo electrónico y contraseña.

7️⃣ Ejecutar el Servidor
Inicia el servidor de desarrollo de Django: 
python manage.py runserver

Accede al proyecto en tu navegador en http://127.0.0.1:8000/.