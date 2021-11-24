from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("reservation", views.ReservationViewSet, basename="reservation")
router.register("rooms", views.BookingInfoViewSet, basename="rooms")

urlpatterns = []
urlpatterns += router.urls
