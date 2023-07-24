from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.filters import CustomFilter
from app.paginations import CustomPagination
from app.user_verification import UserVerification
from user.serializers import UserSerializers
from vehicle.models import Vehicle
from vehicle.serializers import VehicleDetailSerializers

viewName = 'Vehicle'


"""
La clase VehiclesView hereda de UserVerification y ListAPIView y define un método post para manejar la solicitud POST. 
Dentro de este método, se obtienen los datos de la solicitud y se realiza un filtrado de los objetos Vehicle utilizando 
la función custom_filter de CustomFilter. Luego, se paginan los resultados utilizando la función paginate de 
CustomPagination, pasando el nombre de la vista (viewName), los datos de paginación y el conjunto de resultados filtrados. 
Finalmente, se devuelve la respuesta paginada utilizando Response.
"""


class VehiclesView(UserVerification, ListAPIView):
    def post(self, request, format=None):
        # Obtener los datos de la solicitud
        data = self.request.data
        if request.user.is_superuser:
            # Si el usuario es un superusuario, obtener todos los vehículos
            vehicles = Vehicle.objects.all()
        elif request.user.is_staff:
            # Si el usuario es un miembro del personal, obtener los vehículos asociados a ese usuario
            vehicles = Vehicle.objects.filter(users=request.user)
        else:
            # Si el usuario no es un superusuario ni un miembro del personal, no tiene acceso a ningún vehículo
            vehicles = []

        # Filtrar los datos de acuerdo a los parámetros proporcionados
        queryset = CustomFilter.custom_filter(self, data, vehicles)
        # Paginar los resultados
        response = CustomPagination.paginate(self, viewName, data, queryset)
        # Devolver la respuesta paginada
        return Response(response, status=200)


"""
La clase SearchByIdentifier hereda de UserVerification y APIView y se utiliza para buscar un vehículo por su identificador (ID). 
Se define el método get que se ejecuta cuando se realiza una solicitud GET al endpoint correspondiente. 
En el método, se obtiene el valor del parámetro id de la consulta y se realiza lo siguiente:
    1. Se intenta obtener el objeto de vehículo correspondiente al ID proporcionado.
    2. Si se encuentra el vehículo, se serializa utilizando VehicleDetailSerializers.
    3. Se devuelve la respuesta con los datos serializados del vehículo.
    4. Si no se encuentra ningún vehículo con el ID proporcionado, se devuelve una respuesta de error indicando que no existe un objeto con ese identificador.
    5. Si no se proporciona un ID en la consulta, se devuelve una respuesta de error indicando que la solicitud no cumple con los parámetros requeridos.
Este algoritmo permite buscar un vehículo por su identificador y devolver los datos serializados del mismo en caso de encontrarlo.
"""


class SearchByIdentifier(UserVerification, APIView):
    def get(self, request, format=None):
        # Obtener el valor del parámetro 'id' de la consulta
        id = self.request.query_params.get('id', None)

        if id is not None:
            try:
                # Obtener el objeto de vehículo utilizando el ID proporcionado
                vehicle = Vehicle.objects.get(pk=id)

                # Serializar el objeto de vehículo
                serializer = VehicleDetailSerializers(vehicle)

                # Devolver los datos serializados del vehículo
                return Response(serializer.data, status=200)
            except Vehicle.DoesNotExist:
                return Response({'Error': 'ER-VEHICLE-000',
                                 'Message': 'There is no object with identifier: ' + str(id)}, status=404)
        else:
            return Response({'Error': 'ER-VEHICLE-001',
                             'Message': 'The request does not meet the required parameters'}, status=400)


"""
La clase EnableOrDisable hereda de UserVerification y APIView y se utiliza para habilitar o deshabilitar
un vehículo mediante la actualización del campo alive. 
Se define el método put que se ejecuta cuando se realiza una solicitud PUT al endpoint correspondiente. 
En el método, se obtienen los datos de la solicitud, incluyendo el ID del vehículo y el estado alive.
A continuación, se realiza lo siguiente:
    1. Se verifica si se proporcionaron los parámetros requeridos (vehicle_id y is_alive).
    2. Se intenta obtener el objeto de vehículo correspondiente al ID proporcionado.
    3. Se actualiza el estado de "alive" del vehículo y se establece el campo "lastModifiedBy" con el nombre del usuario de la solicitud.
    4. Se intenta guardar los cambios en el objeto de vehículo.
    5. Si se guarda exitosamente, se prepara un mensaje de estado en función del valor de is_alive y se devuelve una respuesta exitosa con el mensaje.
    6. Si ocurre algún error durante el proceso, se devuelve una respuesta de error indicando el mensaje de error correspondiente.
    7. Si no se encuentra ningún vehículo con el ID proporcionado, se devuelve una respuesta de error indicando que no existe un objeto con ese identificador.
Este algoritmo permite habilitar o deshabilitar un vehículo cambiando el valor de "alive" y guardando los cambios en la base de datos.
"""


class EnableOrDisable(UserVerification, APIView):
    def put(self, request, format=None):
        data = self.request.data
        vehicle_id = data.get('id')
        is_alive = data.get('alive')

        if not vehicle_id or is_alive is None:
            return Response({'Error': 'ER-VEHICLE-001',
                             'Message': 'The request does not meet the required parameters'}, status=400)

        try:
            # Obtener el objeto de vehículo utilizando el ID proporcionado
            vehicle = Vehicle.objects.get(pk=vehicle_id)

            # Actualizar el estado de "alive" del vehículo y el campo "lastModifiedBy"
            vehicle.alive = is_alive
            vehicle.lastModifiedBy = self.request.user.name

            try:
                # Guardar los cambios en el objeto de vehículo
                vehicle.save()

                # Preparar el mensaje de estado en función del valor de "is_alive"
                status_msg = 'Registration was activated successfully' if is_alive else 'Registration was successfully deactivated'

                # Devolver una respuesta exitosa con el mensaje de estado
                return Response({'OK': 'Activated' if is_alive else 'Deactivated', 'Message': status_msg}, status=200)
            except Exception as e:
                return Response({'Error': 'ER-VEHICLE', 'Message': str(e)}, status=400)
        except Vehicle.DoesNotExist:
            return Response({'Error': 'ER-VEHICLE-000',
                             'Message': 'There is no object with identifier: ' + str(id)}, status=404)


"""
La clase AddOrEdit hereda de UserVerification y APIView y se utiliza para agregar o editar un vehículo en el sistema. 
Se define el método post que se ejecuta cuando se realiza una solicitud POST o PUT al endpoint correspondiente.

    ° El método POST llama a la función edit para editar el vehículo existente. 
    ° El método PUT llama a la función create para crear un nuevo vehículo.
    
    ° La función edit actualiza los campos del vehículo en función de los datos proporcionados,
    incluyendo la relación de usuarios si se proporciona.
    Luego, se guarda el vehículo actualizado en la base de datos y se devuelve una respuesta exitosa con el
    mensaje y el ID del vehículo actualizado.
    
    ° La función create crea un nuevo objeto de vehículo con los datos proporcionados, 
    establece los campos correspondientes y lo guarda en la base de datos. 
    Si se proporciona una relación de usuarios, también se actualiza. Luego, se devuelve una respuesta exitosa con el mensaje, 
    el ID y la placa del vehículo creado.

En caso de que ocurra algún error durante el proceso de edición o creación, se devuelve una respuesta
 de error con el mensaje correspondiente.
"""


class AddOrEdit(UserVerification, APIView):
    def post(self, request, format=None):
        user_session = UserSerializers(self.request.user)
        return self.create(self.request.data, user_session)

    def put(self, request, format=None):
        user_session = UserSerializers(self.request.user)
        return self.edit(self.request.data, user_session)

    def edit(self, data, user_session):
        # Campos que se pueden actualizar
        update_fields = ['plates', 'brand', 'colour', 'model', 'serialNumber', 'alive']

        try:
            # Obtener el objeto de vehículo utilizando el ID proporcionado
            vehicle = Vehicle.objects.get(pk=data['id'])

            # Actualizar los campos del vehículo en función de los datos proporcionados
            for field in update_fields:
                if field in data:
                    setattr(vehicle, field, data[field])

            # Actualizar la relación de usuarios si se proporciona
            users = data.get('users')

            # Asignar los nuevos grupos al usuario
            if users:
                # Limpiar los usuarios existentes relacionados al vehiculo
                vehicle.users.clear()
                for user in users:
                    vehicle.users.add(user)

            # Actualizar el campo "lastModifiedBy" con el nombre del usuario de la sesión
            vehicle.lastModifiedBy = user_session.data['name']

            # Guardar los cambios en el objeto de vehículo
            vehicle.save()

            # Devolver una respuesta exitosa con el mensaje y el ID del vehículo actualizado
            return Response({'OK': 'Update', 'Message': 'The registry was updated successfully', 'entity': vehicle.id}, status=200)
        except Vehicle.DoesNotExist:
            return Response({'Error': 'ER-VEHICLE-000', 'Message': 'There is no object with identifier: ' + str(id)}, status=404)

    def create(self, data, user_session):
        # Campos requeridos para la creación de un vehículo
        required_fields = ['plates', 'brand', 'colour']

        for field in required_fields:
            if field not in data or not data[field]:
                return Response({'Error': f'ER-USER-00{required_fields.index(field) + 2}', 'Message': f'{field.capitalize()} is required'}, status=400)

        # Crear un nuevo objeto de vehículo con los datos proporcionados
        vehicle = Vehicle()
        vehicle.plates = data['plates']
        vehicle.brand = data['brand']
        vehicle.colour = data['colour']

        # Establecer campos adicionales si se proporcionan
        additional_fields = ['model', 'serialNumber', 'alive']
        for field in additional_fields:
            if field in data:
                setattr(vehicle, field, data[field])

        # Establecer los campos "createdBy" y "lastModifiedBy" con el nombre del usuario de la sesión
        vehicle.createdBy = user_session.data['name']
        vehicle.lastModifiedBy = user_session.data['name']

        try:
            # Guardar el objeto de vehículo en la base de datos
            vehicle.save()

            # Actualizar la relación de usuarios si se proporciona
            users = data.get('users')

            # Asignar los nuevos grupos al usuario
            if users:
                # Limpiar los usuarios existentes relacionados al vehiculo
                vehicle.users.clear()
                for user in users:
                    vehicle.users.add(user)

            # Devolver una respuesta exitosa con el mensaje, el ID y la placa del vehículo creado
            return Response({'OK': 'Save', 'Message': 'The Vehicle: ' + str(data['plates']) + ' was saved successfully', 'entity': vehicle.id}, status=201)
        except Exception as e:
            return Response({'Error': 'ER-VEHICLE', 'Message': str(e)}, status=400)


"""
La función vehicle_map es una vista que requiere autenticación (@login_required) y se 
utiliza para mostrar un mapa de vehículos en el sistema.
Primero, se obtiene el usuario de la solicitud (request.user). Luego, se verifica el tipo de usuario:
    ° Si el usuario es un superusuario, se obtienen todos los vehículos en el 
    sistema utilizando Vehicle.objects.all().
    ° Si el usuario es un miembro del personal, se obtienen los vehículos asociados a 
    ese usuario utilizando Vehicle.objects.filter(users=user).
    ° Si el usuario no es un superusuario ni un miembro del personal, no se le asigna 
    ningún vehículo y la lista de vehículos se deja vacía.
    
Finalmente, se crea un contexto con los vehículos obtenidos y se renderiza el template "vehicle_map.html" con ese contexto. 
La respuesta renderizada se devuelve al cliente.
"""


@login_required
def vehicle_map(request):
    # Obtener el usuario de la solicitud
    user = request.user

    if user.is_superuser:
        # Si el usuario es un superusuario, obtener todos los vehículos
        vehicles = Vehicle.objects.all()
    elif user.is_staff:
        # Si el usuario es un miembro del personal, obtener los vehículos asociados a ese usuario
        vehicles = Vehicle.objects.filter(users=user)
    else:
        # Si el usuario no es un superusuario ni un miembro del personal, no tiene acceso a ningún vehículo
        vehicles = []

    # Crear el contexto con los vehículos obtenidos
    context = {'vehicles': vehicles}

    # Renderizar el template "vehicle_map.html" con el contexto y devolver la respuesta
    return render(request, 'vehicle_map.html', context)
