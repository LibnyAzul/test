"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def custom_page_not_found(request, exception=None):
    # Renderiza el template 404.html con el estilo de admin.sites
    return render(request, '404.html', status=404)

handler404 = custom_page_not_found


urlpatterns = [
 #                 path('', TemplateView.as_view(template_name='index.html')),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/tracking/', include('tracking.urls')),
                  path('api/user/', include('user.urls')),
                  path('api/vehicle/', include('vehicle.urls')),
                  path('admin/', admin.site.urls),
                  re_path(r'^.*$', custom_page_not_found),
              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

# Esta línea de código sirve para capturar todas las URL que no coincidan con las rutas previamente definidas
#  en urlpatterns y las redirige a un archivo index.html.
#urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
