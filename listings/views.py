from django.db.models import Min, Sum
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status, filters, serializers
from rest_framework.decorators import action
from .models import *
from .serializers import *
from datetime import datetime

# Create your views here.


class ReservationViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, IsAll,)
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.all()
        queryset = queryset.order_by("id")
        return queryset

    def list(self, request, *args, **kwargs):
        response_data = {}
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        response_data["status_code"] = "200"
        response_data["status"] = True
        response_data["message"] = "Reservation details"
        response_data["data"] = data
        resp_status = status.HTTP_200_OK
        return Response(response_data, status=resp_status)

    def create(self, request, *args, **kwargs):
        response_data = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            response = super().create(request)
        except Exception as e:
            response_data["status_code"] = "400"
            response_data["status"] = False
            response_data["message"] = "Booking unsuccessful - " + str(e)
        else:
            response_data["status_code"] = "201"
            response_data["status"] = True
            response_data["message"] = "Booking successful"
            response_data["data"] = response.data

        if response_data["status_code"] == "400":
            resp_status = status.HTTP_400_BAD_REQUEST
        elif response_data["status_code"] == "201":
            resp_status = status.HTTP_201_CREATED

        return Response(response_data, status=resp_status)


class BookingInfoViewSet(viewsets.ModelViewSet):
    serializer_class = BookingInfoSerializer

    def get_queryset(self):
        queryset = BookingInfo.objects.all()
        queryset = queryset.order_by("id")

        max_price = self.request.query_params.get("max_price", None)
        check_in = self.request.query_params.get("check_in", None)
        check_out = self.request.query_params.get("check_out", None)

        exclude_list = []
        reservation_list = Reservation.objects.all()
        if max_price:
            queryset = queryset.filter(price__lte=int(max_price))
        if check_in and check_out:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

            for reserved in reservation_list:
                if (check_in_date <= reserved.check_in <= check_out_date) or (
                    check_in_date <= reserved.check_out <= check_out_date
                ):
                    exclude_list.append(reserved.property_booked.id)
            queryset = queryset.exclude(id__in=exclude_list)
        return queryset.order_by("price")

    def list(self, request, *args, **kwargs):
        response_data = {}
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        response_data["status_code"] = "200"
        response_data["status"] = True
        response_data["message"] = "Property details"
        response_data["data"] = data
        resp_status = status.HTTP_200_OK
        return Response(response_data, status=resp_status)

    @action(methods=["get"], detail=False, name="check_availability")
    def check_availability(self, request, *args, **kwargs):
        response_data = {}
        queryset = self.filter_queryset(self.get_queryset())

        apartments = queryset.filter(hotel_room_type__isnull=True)
        hotels = queryset.filter(listing__isnull=True)

        min_price_rooms = (
            hotels.values("hotel_room_type__hotel__id")
            .annotate(price=Min("price"))
            .order_by("price")
        )
        unique_hotel_booking_ids = BookingInfo.objects.none()
        for entry in min_price_rooms:
            obj = hotels.filter(
                hotel_room_type__hotel__id=entry["hotel_room_type__hotel__id"],
                price=entry["price"],
            )
            unique_hotel_booking_ids = unique_hotel_booking_ids | obj
        queryset = apartments | unique_hotel_booking_ids

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        response_data["status_code"] = "200"
        response_data["status"] = True
        response_data["message"] = "Available properties"
        response_data["data"] = data

        resp_status = status.HTTP_200_OK
        return Response(response_data, status=resp_status)
