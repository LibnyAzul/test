from django.urls import path
from user.views import UsersView, EnableOrDisable, AddOrEdit, SearchByIdentifier, SignupView, LoginView, GetAllRoles, AssignGroups
# Administra las URL de las Apis de la entidad
urlpatterns = [
    path('', UsersView.as_view()),
    path('alive', EnableOrDisable.as_view()),
    path('add/', AddOrEdit.as_view()),
    path('edit/', AddOrEdit.as_view()),
    path('search/', SearchByIdentifier.as_view()),
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('roles', GetAllRoles.as_view()),
    path('assignGroups', AssignGroups.as_view())
]