from django.urls import path

from vehicle.views import VehiclesView, EnableOrDisable, AddOrEdit, SearchByIdentifier, vehicle_map

# Administra las URL de las Apis de la entidad
urlpatterns = [
    path('', VehiclesView.as_view()),
    path('alive', EnableOrDisable.as_view()),
    path('add/', AddOrEdit.as_view()),
    path('edit/', AddOrEdit.as_view()),
    path('search/', SearchByIdentifier.as_view()),
    path('map/', vehicle_map, name='vehicle_map'),
]