from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.filters import CustomFilter
from app.paginations import CustomPagination
from app.user_verification import UserVerification
from user.models import UserManager
from user.serializers import UserSerializers, UserDetailSerializers, GroupSerializers
from secrets import compare_digest

User = get_user_model()
viewName = 'User'


"""
La clase LoginView hereda de APIView y se utiliza para manejar la autenticación de usuarios. Se define el método post 
que se ejecuta cuando se realiza una solicitud POST a la vista de inicio de sesión. En este método, se obtienen las 
credenciales del cuerpo de la solicitud y se autentica al usuario utilizando la función authenticate de Django. 
Si las credenciales son válidas y el usuario está activo, se serializa el objeto de usuario y se devuelve en la 
respuesta con un código de estado 200. Si el usuario está inactivo, se devuelve un error de acceso denegado con un 
código de estado 403. Si las credenciales son inválidas, también se devuelve un error de acceso denegado 
con un código de estado 403. La clase tiene permisos de acceso públicos y no requiere autenticación.
"""


class LoginView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, format=None):
        data = self.request.data
        credentials = {
            'email': data['email'],
            'password': data['password']
        }
        user_session = authenticate(**credentials)

        if user_session is not None and user_session:
            if user_session.alive:
                # Si las credenciales son válidas y el usuario está activo, se serializa el objeto de usuario
                serializer = UserSerializers(user_session)
                return Response(serializer.data, status=200)
            else:
                # Si el usuario está inactivo, se devuelve un error de acceso denegado
                return Response(
                    {'Error': 'ER-LOGIN-002',
                     'Message': 'El usuario está inactivo, contacte al administrador del sistema'},
                    status=403)
        else:
            # Si las credenciales son inválidas, se devuelve un error de acceso denegado
            return Response({'Error': 'ER-LOGIN-001', 'Message': 'Las credenciales son inválidas'}, status=403)


"""
La clase SignupView hereda de UserVerification y APIView y se utiliza para manejar el registro de nuevos usuarios. 
Se define el método post que se ejecuta cuando se realiza una solicitud POST al endpoint de registro. 
En este método, se obtienen los datos proporcionados en la solicitud, como el nombre de usuario, el email, 
la contraseña y la confirmación de contraseña. Se realizan varias validaciones, como verificar si las 
contraseñas coinciden, si el email ya existe en la base de datos y si el nombre de usuario ya existe. 
Si todas las validaciones son exitosas, se crea un nuevo usuario utilizando el UserManager y se 
devuelve una respuesta exitosa con un código de estado 201. Si ocurre algún error durante el registro, 
se devuelve un mensaje de error correspondiente con un código de estado 400. La clase requiere 
la verificación del usuario y tiene permisos de acceso restringidos.
"""


class SignupView(APIView):
    def post(self, request, format=None):
        data = self.request.data
        name = data['name']
        email = data['email']
        password = data['password']
        conf_password = data['confPassword']

        if compare_digest(password, conf_password):
            # Compara si las contraseñas coinciden utilizando la función compare_digest para mayor seguridad
            if User.objects.filter(email=email).exists():
                # Verifica si el email ya existe en la base de datos
                return Response({'Error': 'El email proporcionado ya existe'}, status=400)
            else:
                if User.objects.filter(name=name).exists():
                    # Verifica si el nombre de usuario ya existe en la base de datos
                    return Response({'Error': 'El nombre de usuario ya existe'}, status=400)
                else:
                    if len(password) < 8:
                        # Verifica si la contraseña tiene al menos 8 caracteres
                        return Response({'Error': 'La contraseña debe tener al menos 8 caracteres'}, status=400)
                    else:
                        try:
                            # Intenta crear un nuevo usuario utilizando el UserManager
                            user = User.objects.create(name=name, email=email, password=password, createdBy=None)

                            if user:
                                # Si el usuario se crea correctamente, se devuelve una respuesta exitosa
                                return Response({'Success': 'El usuario "' + user.name + '", se creó exitosamente.'},
                                                status=201)
                            else:
                                # Si ocurre algún error durante la creación del usuario, se devuelve un error
                                return Response({'Error': 'El usuario "' + name + '", no se guardó.'}, status=400)
                        except Exception as e:
                            # Si ocurre una excepción durante la creación del usuario, se devuelve un error
                            return Response({'Error': 'ER-USER', 'Message': str(e)}, status=400)
        else:
            # Si las contraseñas no coinciden, se devuelve un error
            return Response({'Error': 'Las contraseñas no coinciden'}, status=400)


"""
La clase UsersView hereda de UserVerification y ListAPIView y define un método post para manejar la solicitud POST. 
Dentro de este método, se obtienen los datos de la solicitud y se realiza un filtrado de los objetos User utilizando 
la función custom_filter de CustomFilter. Luego, se paginan los resultados utilizando la función paginate de 
CustomPagination, pasando el nombre de la vista (viewName), los datos de paginación y el conjunto de resultados filtrados. 
Finalmente, se devuelve la respuesta paginada utilizando Response.
"""


class UsersView(UserVerification, ListAPIView):
    def post(self, request, format=None):
        data = self.request.data
        # Filtrar los datos de acuerdo a los parámetros proporcionados
        queryset = CustomFilter.custom_filter(self, data, User.objects.all())
        # Paginar los resultados
        response = CustomPagination.paginate(self, viewName, data, queryset)
        # Devolver la respuesta paginada
        return Response(response, status=200)


"""
La clase SearchByIdentifier hereda de UserVerification y APIView y se utiliza para buscar un usuario por su identificador. 
Se define el método get que se ejecuta cuando se realiza una solicitud GET al endpoint de búsqueda de usuarios. 
En este método, se obtiene el identificador del usuario de los parámetros de la solicitud y se intenta buscar el 
objeto de usuario correspondiente en la base de datos. Si se encuentra, se serializa el objeto de usuario utilizando 
UserDetailSerializers y se devuelve una respuesta con los datos serializados. Si el usuario no existe, se maneja la 
excepción y se devuelve una respuesta apropiada. Si no se proporciona un identificador en la solicitud, se devuelve 
una respuesta de error indicando que los parámetros requeridos no se cumplen. La clase requiere la verificación del 
usuario y tiene permisos de acceso restringidos.
"""


class SearchByIdentifier(UserVerification, APIView):
    def get(self, request, format=None):
        id = self.request.query_params.get('id', None)
        if id is not None:
            try:
                # Buscar el objeto de usuario por su identificador
                queryset = User.objects.get(pk=id)
                # Serializar el objeto de usuario
                serializer = UserDetailSerializers(queryset)
                return Response(serializer.data, status=200)
            except User.DoesNotExist:
                # Manejar el caso en el que el usuario no existe
                return self.handle_does_not_exist(id)
        else:
            return Response(
                {'Error': 'ER-USER-001', 'Message': 'The request does not meet the required parameters'},
                status=400)


"""
La clase EnableOrDisable hereda de UserVerification y APIView y se utiliza para habilitar o deshabilitar un usuario. 
Se define el método put que se ejecuta cuando se realiza una solicitud PUT al endpoint de habilitación/deshabilitación de usuarios. 
En este método, se obtiene el identificador y el estado de alive del usuario de los datos de la solicitud. 
Se verifica que los parámetros requeridos estén presentes y luego se intenta buscar el 
objeto de usuario correspondiente en la base de datos. 
Si se encuentra, se actualiza el estado de alive del usuario y se guarda el objeto de usuario. 
Se devuelve una respuesta con un mensaje de éxito indicando el estado de la operación.
Si el usuario no existe, se maneja la excepción y se devuelve una respuesta apropiada. 
La clase requiere la verificación del usuario y tiene permisos de acceso restringidos.
"""


class EnableOrDisable(UserVerification, APIView):
    def put(self, request, format=None):
        data = self.request.data
        user_id = data.get('id')
        is_alive = data.get('alive')

        if not user_id or is_alive is None:
            return Response(
                {'Error': 'ER-USER-001', 'Message': 'The request does not meet the required parameters'},
                status=400
            )

        try:
            # Buscar el objeto de usuario por su identificador
            user = User.objects.get(pk=user_id)
            # Actualizar el estado de alive del usuario
            user.alive = is_alive
            # Establecer el último usuario modificado
            user.lastModifiedBy = self.request.user.name

            try:
                # Guardar los cambios en el objeto de usuario
                user.save()
                # Preparar el mensaje de estado según el estado de alive
                status_msg = 'Registration was activated successfully' if is_alive else 'Registration was successfully deactivated'
                return Response(
                    {'OK': 'Activated' if is_alive else 'Deactivated', 'Message': status_msg},
                    status=200
                )
            except Exception as e:
                return Response({'Error': 'ER-USER', 'Message': str(e)}, status=400)
        except User.DoesNotExist:
            # Manejar el caso en el que el usuario no existe
            return self.handle_does_not_exist(user_id)


"""
La clase AddOrEdit hereda de UserVerification y APIView y se utiliza para agregar o editar un usuario. 
Se define el método post que se ejecuta cuando se realiza una solicitud POST al endpoint de agregar usuario y 
solicitud PUT al editar usuario. 
En el método edit_user, se busca el objeto de usuario correspondiente y se actualizan los campos especificados en los datos de la solicitud. 
    ° Si se proporciona una nueva contraseña, se establece para el usuario. 
    ° Se guarda el objeto de usuario actualizado y se devuelve una respuesta de éxito. 
    ° Si el usuario no existe, se maneja la excepción y se devuelve una respuesta apropiada. 
En el método create_user, se crean nuevos usuarios, ya sea un superusuario o un usuario normal, 
según los datos proporcionados en la solicitud. 
    ° Se asignan los campos adicionales si están presentes y se guardan los cambios en la base de datos. 
    ° Se devuelve una respuesta de éxito con el ID del usuario creado. Si ocurre alguna excepción durante el proceso, 
    ° se maneja y se devuelve una respuesta de error. La clase requiere la verificación del usuario y tiene permisos de acceso restringidos.
"""


class AddOrEdit(UserVerification, APIView):
    def post(self, request, format=None):
        user_session = UserSerializers(self.request.user)
        return self.create_user(self.request.data, user_session)

    def put(self, request, format=None):
        user_session = UserSerializers(self.request.user)
        return self.edit_user(self.request.data, user_session)

    def edit_user(self, data, user_session):
        try:
            # Obtener el objeto de usuario por su identificador
            user = User.objects.get(pk=data['id'])
            update_fields = ['alive', 'cellphone', 'birthdate', 'email', 'fullName', 'is_superuser', 'is_staff', 'name']

            for field in update_fields:
                if field in data:
                    setattr(user, field, data[field])

            if 'password' in data and data['password']:
                # Establecer una nueva contraseña para el usuario
                user.set_password(data['password'])

            user.lastModifiedBy = user_session.data['name']
            user.save()
            return Response({'OK': 'Update', 'Message': 'The registry was updated successfully', 'entity': user.id},
                            status=200)

        except User.DoesNotExist:
            # Manejar el caso en el que el usuario no existe
            return Response(
                {'Error': 'ER-USER-000', 'Message': 'There is no object with identifier: ' + str(data['id'])},
                status=404)

        except Exception as e:
            # Manejar otras excepciones que puedan ocurrir
            return Response({'Error': 'ER-USER', 'Message': str(e)}, status=400)

    def create_user(self, data, user_session):
        required_fields = ['name', 'email', 'password']

        for field in required_fields:
            if field not in data or not data[field]:
                # Manejar el caso en el que falten campos requeridos
                return Response({'Error': f'ER-USER-00{required_fields.index(field) + 3}',
                                 'Message': f'{field.capitalize()} is required'}, status=400)

        is_superuser = data.get('is_superuser', False)
        user = None
        if is_superuser:
            # Crear un nuevo superusuario
            user = User.objects.create_superuser(data['name'], data['email'], data['password'],
                                                 user_session.data['name'])
        else:
            # Crear un nuevo usuario normal
            user = User.objects.create(data['name'], data['email'], data['password'], user_session.data['name'])

        additional_fields = ['cellphone', 'birthdate', 'fullName']

        for field in additional_fields:
            if field in data:
                setattr(user, field, data[field])

        user.createdBy = user_session.data['name']
        user.lastModifiedBy = user_session.data['name']

        try:
            # Guardar el objeto de usuario en la base de datos
            user.save()
            return Response({'OK': 'Save', 'Message': 'The User: ' + str(data['name']) + ' was saved successfully',
                             'entity': user.id}, status=201)
        except Exception as e:
            # Manejar excepciones al guardar el usuario
            return Response({'Error': 'ER-USER', 'Message': str(e)}, status=400)


"""
La clase GetAllRoles hereda de UserVerification y APIView y se utiliza para obtener todos los roles disponibles en el sistema. 
Se define el método post que se ejecuta cuando se realiza una solicitud POST al endpoint correspondiente. 
En el método, se obtienen todos los objetos de roles de la base de datos utilizando Group.objects.all().
Luego, los objetos de roles se serializan utilizando GroupSerializers para convertirlos en un formato adecuado para la respuesta. 
Finalmente, se devuelve una respuesta con los datos de los roles serializados. 
Esta clase requiere la verificación del usuario y tiene permisos de acceso restringidos.
"""


class GetAllRoles(UserVerification, APIView):
    def post(self, request, format=None):
        # Obtener todos los objetos de roles
        queryset = Group.objects.all()

        # Serializar los objetos de roles
        serializer = GroupSerializers(queryset, many=True)

        # Devolver la respuesta con los datos de los roles serializados
        return Response({'OK': serializer.data}, status=200)


"""
La clase AssignGroups hereda de UserVerification y APIView y se utiliza para asignar grupos a un usuario específico. 
Se define el método post que se ejecuta cuando se realiza una solicitud POST al endpoint correspondiente. 
En el método, se obtienen los datos de la solicitud, incluyendo el ID del usuario y los IDs de los grupos a asignar. 
Se validan los parámetros de la solicitud y se realizan las siguientes acciones:
    1. Se obtiene el objeto de usuario correspondiente al ID proporcionado.
    2. Se obtienen los objetos de grupos correspondientes a los IDs proporcionados.
    3. Se eliminan todos los grupos existentes del usuario.
    4. Se asignan los nuevos grupos al usuario.
    5. Se devuelve una respuesta de éxito indicando que los grupos se han asignado correctamente.
Si el usuario o los grupos no se encuentran, se devuelve una respuesta de error correspondiente.
"""


class AssignGroups(UserVerification, APIView):
    def post(self, request, format=None):
        # Obtener los datos de la solicitud
        data = self.request.data

        # Obtener el ID del usuario y los IDs de los grupos
        user_id = data['userId']
        groups_ids = data.get('groupsId', [])

        # Validar los parámetros de la solicitud
        if user_id is None or not isinstance(groups_ids, list):
            return Response({'error': 'Invalid parameters'})

        try:
            # Obtener el objeto de usuario
            user = User.objects.get(id=user_id)

            # Obtener los objetos de grupos
            groups = Group.objects.filter(id__in=groups_ids)

            # Limpiar los grupos existentes del usuario
            user.groups.clear()

            # Asignar los nuevos grupos al usuario
            for group in groups:
                user.groups.add(group)

            # Devolver la respuesta de éxito
            return Response({'success': 'Groups assigned successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'})
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'})

