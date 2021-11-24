from .models import *
from rest_framework import serializers


class ReservationSerializer(serializers.ModelSerializer):
    listing_type = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = (
            "property_booked",
            "check_in",
            "check_out",
            "listing_type",
            "title",
            "country",
            "city",
            "price",
        )

    def get_listing_type(self, obj):
        if obj.property_booked.listing:
            return obj.property_booked.listing.get_listing_type_display()
        else:
            return obj.property_booked.hotel_room_type.hotel.get_listing_type_display()

    def get_title(self, obj):
        if obj.property_booked.listing:
            return obj.property_booked.listing.title
        else:
            return obj.property_booked.hotel_room_type.hotel.title

    def get_country(self, obj):
        if obj.property_booked.listing:
            return obj.property_booked.listing.country
        else:
            return obj.property_booked.hotel_room_type.hotel.country

    def get_city(self, obj):
        if obj.property_booked.listing:
            return obj.property_booked.listing.city
        else:
            return obj.property_booked.hotel_room_type.hotel.city

    def get_price(self, obj):
        return obj.property_booked.price


class BookingInfoSerializer(serializers.ModelSerializer):
    listing_type = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = BookingInfo
        fields = (
            "id",
            "listing_type",
            "title",
            "country",
            "city",
            "price",
        )

    def get_listing_type(self, obj):
        if obj.listing:
            return obj.listing.get_listing_type_display()
        else:
            return obj.hotel_room_type.hotel.get_listing_type_display()

    def get_title(self, obj):
        if obj.listing:
            return obj.listing.title
        else:
            return obj.hotel_room_type.hotel.title

    def get_country(self, obj):
        if obj.listing:
            return obj.listing.country
        else:
            return obj.hotel_room_type.hotel.country

    def get_city(self, obj):
        if obj.listing:
            return obj.listing.city
        else:
            return obj.hotel_room_type.hotel.city

    def get_price(self, obj):
        return obj.price
