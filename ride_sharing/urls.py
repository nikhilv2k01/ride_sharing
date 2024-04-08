from django.urls import path
from .views import *

urlpatterns = [
    path('rides/create/', RideCreateAPIView.as_view(), name='ride-create'),
    path('rides/<int:ride_id>/update-status/', RideCreateAPIView.as_view(), name='ride-status-update'),
    path('rides/<int:ride_id>/', RideDetailAPIView.as_view(), name='ride-detail'),
    path('rides/', RideListAPIView.as_view(), name='ride-list'),
    path('rides/<int:ride_id>/location/', RideLocationAPIView.as_view(), name='ride-location'),
] 