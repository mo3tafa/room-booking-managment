from django.urls import path,include
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from room_reserve.viewsets import *

# Create a router and register our viewsets with it.
router = DefaultRouter()


router.register(r'',DefaultViewSet)
# router.register(r'user',UserViewSet)
router.register(r'room',RoomViewSet)
router.register(r'reservation',ReservationViewSet)
# router.register(r'state',StateViewSet)
# router.register(r'role',RoleViewSet)


urlpatterns = [
    path('',include(router.urls)),
]