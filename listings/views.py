from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ListingSerializer , BookingSerializer
from rest_framework import IsAuthenticated , AllowAny
# Create your views here.

class ListingView(viewsets.ModelViewset):
       queryset = Listing.objects.all()
       serializer_class = ListingSerializer 
       permission_class = [AllowAny]
      


class BookingView(viewsets.ModelViewset):
       queryset = Booking.objects.all()
       serializer_class = BookingSerializer
       permission_class = [IsAuthenticated] 

       def get_queryset(self):
           user = self.request.user
           return Booking.objects.filter(user=user)

      