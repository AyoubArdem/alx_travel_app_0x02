from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "listing_id",
            "host",
            "title",
            "description",
            "price_per_night",
            "location",
            "created_at",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "booking_id",
            "listing",
            "user",
            "check_in",
            "check_out",
            "status",
            "created_at",
        ]
