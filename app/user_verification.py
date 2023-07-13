from rest_framework import permissions
from rest_framework.response import Response

from user.serializers import UserSerializers


class ActiveUserRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_data = UserSerializers(user).data
        return user.is_authenticated and user_data['alive']


class UserVerification:
    permission_classes = [ActiveUserRequired]

    def handle_inactive_user(self):
        return Response(
            {'Error': 'ER-LOGIN-002', 'Message': 'The user is inactive, contact the system administrator'},
            status=403
        )

    def handle_invalid_credentials(self):
        return Response(
            {'Error': 'ER-COLLABORATOR-001', 'Message': 'Credentials are invalid'},
            status=403)

    def handle_does_not_exist(self, id):
        return Response(
            {'Error': 'ER-USER-000',
             'Message': 'There is no object with identifier: ' + str(id)},
            status=404)

# Este es un código en Django que maneja la verificación de usuarios y sus permisos.
#     1. ActiveUserRequired es una clase de permiso personalizada que hereda de permissions.BasePermission.
#        Define una única función has_permission() que toma una solicitud y una vista, y retorna True
#         si el usuario está autenticado y está activo (es decir, su atributo alive es True).
#        En caso contrario, retorna False. Los permisos en Django son una forma de asegurar que solo ciertos
#         usuarios puedan acceder a ciertas vistas o realizar ciertas operaciones.
#     2. UserVerification es una clase que define los permisos necesarios para una vista y provee dos métodos para
#        manejar errores comunes de autenticación de usuarios.
#         1. permission_classes = [ActiveUserRequired] especifica que todas las vistas que utilicen
#             esta clase requerirán que el usuario esté activo.
#         2. handle_inactive_user() y handle_invalid_credentials() son dos métodos que retornan una respuesta HTTP
#             con un mensaje de error y un código de estado.
#            Estos métodos pueden ser llamados en una vista para manejar casos en los que el usuario está inactivo o
#             las credenciales son inválidas.
#   Este tipo de clases son útiles para abstraer la lógica común de manejo de permisos y errores de autenticación,
#     para así mantener el código de las vistas más limpio y fácil de leer.
