from django.urls import path  
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet

urlpatterns=[
]

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listings')
router.register(r'bookings', BookingViewSet, basename='bookings')

urlpatterns += router.urls
