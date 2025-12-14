from django.urls import path  
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
from .views import initiate_payment, verify_payment

urlpatterns = [
    path("payment/initiate/", initiate_payment),
    path("payment/verify/", verify_payment),
]


router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listings')
router.register(r'bookings', BookingViewSet, basename='bookings')

urlpatterns += router.urls
