from django.core.paginator import Paginator

from tracking.serializers import TrackingDetailSerializers
from user.serializers import UsersSerializers
from vehicle.serializers import VehiclesSerializers


class CustomPagination():
    def paginate(self, type, data, object_list):
        # Mapa de tipos para seleccionar el serializador adecuado
        type_map = {
            'User': UsersSerializers,
            'Vehicle': VehiclesSerializers,
            'Tracking': TrackingDetailSerializers
        }
        type_object = type_map.get(type)

        # Obtiene la cantidad de objetos por página
        objects_per_page = data.get('objectsPerPage', 25)
        if objects_per_page < 0:
            objects_per_page = len(object_list)

        # Crea la paginación
        pagination = Paginator(object_list, objects_per_page)

        # Obtiene el número de página solicitado
        page_number = data.get('page', 1)
        if page_number > pagination.num_pages:
            page_number = pagination.num_pages

        # Obtiene la página correspondiente
        get_page = pagination.page(page_number)

        # Manejo de las páginas siguiente y anterior
        if data.get('nextPage', False) and get_page.has_next():
            page_number += 1
            get_page = pagination.page(page_number)
        elif data.get('previousPage', False) and get_page.has_previous():
            page_number -= 1
            get_page = pagination.page(page_number)

        # Construye la respuesta con los datos paginados
        response = {
            'page': page_number,
            'total': pagination.count,
            'maxPage': pagination.num_pages,
            'objectsPerPage': objects_per_page,
            'objectList': type_object(get_page.object_list, many=True).data
        }

        return response
