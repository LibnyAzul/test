from django.urls import path

from tracking.views import TrackingsView, GetLatestTracking, CreateTracking

urlpatterns = [
    path('', TrackingsView.as_view()),
    path('add/', CreateTracking.as_view()),
    path('getLatestTracking/', GetLatestTracking.as_view(), name='get_latest_tracking')
]