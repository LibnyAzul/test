from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.filters import CustomFilter
from app.paginations import CustomPagination
from app.user_verification import UserVerification
from tracking.models import Tracking
from tracking.serializers import TrackingDetailSerializers, TrackingSerializer
from vehicle.models import Vehicle

viewName = 'Tracking'

"""
La clase TrackingsView hereda de UserVerification y ListAPIView y define un método post para manejar la solicitud POST. 
Dentro de este método, se obtienen los datos de la solicitud y se realiza un filtrado de los objetos Tracking utilizando 
la función custom_filter de CustomFilter. Luego, se paginan los resultados utilizando la función paginate de 
CustomPagination, pasando el nombre de la vista (viewName), los datos de paginación y el conjunto de resultados filtrados. 
Finalmente, se devuelve la respuesta paginada utilizando Response.
"""


class TrackingsView(UserVerification, ListAPIView):
    def post(self, request, format=None):
        data = self.request.data
        # Filtrar los datos de acuerdo a los parámetros proporcionados
        queryset = CustomFilter.custom_filter(self, data, Tracking.objects.all())
        # Paginar los resultados
        response = CustomPagination.paginate(self, viewName, data, queryset)
        # Devolver la respuesta paginada
        return Response(response, status=200)


"""
La clase CreateTracking hereda de APIView y define un método post para manejar la solicitud POST. 
Dentro de este método, se obtienen los datos de la solicitud y se verifica si todos los campos requeridos 
(vehicle_plates, latitude y longitude) están presentes y no están vacíos. Si algún campo requerido falta o está vacío, 
se devuelve una respuesta de error con el código de error y un mensaje correspondiente. Luego, se crea una instancia 
del serializador TrackingSerializer con los datos recibidos. Si los datos son válidos, se guardan y se devuelve una 
respuesta exitosa. Si los datos no son válidos, se devuelven los errores de validación en la respuesta.
"""


class CreateTracking(APIView):
    def post(self, request, format=None):
        data = self.request.data
        required_fields = ['vehicle_plates', 'latitude', 'longitude']

        # Verificar si todos los campos requeridos están presentes y no están vacíos
        for field in required_fields:
            if field not in data or not data[field]:
                error_code = f'ER-TRACKING-00{required_fields.index(field) + 2}'
                error_message = f'{field.capitalize()} is required'
                return Response({'Error': error_code, 'Message': error_message}, status=400)

        # Serializar los datos de seguimiento
        tracking_serializer = TrackingSerializer(data=data)
        if tracking_serializer.is_valid():
            # Guardar los datos de seguimiento
            tracking_serializer.save()
            return Response({'OK': 'Save'}, status=201)
        else:
            # Devolver errores de validación si los datos no son válidos
            return Response({'Error': 'ER-TRACKING', 'Message': str(tracking_serializer.errors)}, status=400)


"""
La clase GetLatestTracking hereda de UserVerification y APIView. Define un método get_object para obtener el objeto de 
seguimiento correspondiente a un identificador de vehículo. Dentro de este método, se busca el vehículo en base al 
identificador proporcionado y se obtiene el último registro de seguimiento asociado a ese vehículo, ordenado por 
la fecha de creación descendente. Si no se encuentra ningún registro de seguimiento, se devuelve una respuesta de error. 
En el método get, se obtiene el identificador de vehículo de los parámetros de consulta y se llama al método get_object 
para obtener el objeto de seguimiento correspondiente. Luego, se serializa el objeto de seguimiento y se devuelve en la
respuesta. Si no se proporciona el identificador en los parámetros de la solicitud, se devuelve un error en la respuesta.
"""


class GetLatestTracking(UserVerification, APIView):

    def get(self, request, format=None):
        id = self.request.query_params.get('id', None)
        if id is not None:
            try:
                vehicle = Vehicle.objects.get(pk=id)
                tracking = Tracking.objects.filter(vehicle=vehicle).order_by('-createdDate').first()
                if tracking is None:
                    return Response({'Error': 'ER-TRACKING-000',
                                     'Message': 'No hay registro de seguimiento para el vehículo especificado'}, status=200)

                # Serializar el objeto de seguimiento
                serializer = TrackingDetailSerializers(tracking)
                return Response(serializer.data, status=200)
            except Vehicle.DoesNotExist:
                return Response({'Error': 'ER-VEHICLE-000',
                                 'Message': 'No existe un objeto con el identificador: ' + str(id)}, status=404)
        else:
            # Devolver un error si no se proporciona el identificador en los parámetros de la solicitud
            return Response({'Error': 'ER-TRACKING-001',
                             'Message': 'La solicitud no cumple con los parámetros requeridos'}, status=400)
