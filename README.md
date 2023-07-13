# TechTest
TechTest es una aplicación web desarrollada en Django para gestionar pruebas técnicas.


# Características
 - Gestión de usuarios: Registro, inicio de sesión y roles de usuario.
 - Gestión de vehículos: Agregar, editar, buscar y activar/desactivar vehículos.
 - Gestión de seguimientos: Registrar y buscar seguimientos de vehículos.
 - Mapa de vehículos: Visualización de vehículos en un mapa interactivo.
# Requisitos previos
 - Python 3.x
 - Django 3.x
 - Otros requisitos de paquetes y dependencias se pueden encontrar en el archivo requirements.txt

# Instalación
### Clona el repositorio de techTest:
```git clone https://github.com/tuusuario/techTest.git```
 
### Accede al directorio del proyecto:
`cd techTest`

### Crea y activa un entorno virtual (opcional, pero se recomienda):
`python -m venv env`
#### - Linux
`source venv/bin/activate`

#### - Windows
`.\env\Scripts\activate`

### Instala las dependencias del proyecto:
`pip install -r requirements.txt`

### Configurar acceso a base de datos
Accede al archivo `techTest\app\settings.py`, busca la configuración: DATABASES, y modifica la estructura segun tus necesidades.

### Gestiona las migraciones de las entidades:
`python manage.py makemigrations`

### Realiza las migraciones de la base de datos:
`python manage.py migrate`

### Crea un super usuario que te ayude a gestionar el sistema:
`python manage.py createsuperuser`
- Coloca los datos que se te solicitaran, user, email, password, y confirmación de password

### Inicia el servidor de desarrollo:
`python manage.py runserver`
Abre tu navegador y accede a http://127.0.0.1:8000/admin/ para ver la aplicación en funcionamiento.

# Notas adicionales
- Es necesario configurar el archivo: `techTest\vehicle\templates\vehicle_map.html`, remplazar YOUR_API_KEY de 
 `<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>`, por tu api key.
