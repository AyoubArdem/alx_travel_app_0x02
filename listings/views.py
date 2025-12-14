from django.shortcuts import render
from rest_framework import viewsets,status
from .models import Payment,Listing,Booking
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
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
'''
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def payment_view(request):
    booking_ref = request.data.get("booking_reference")
    transaction_id = request.data.get("transaction_id")
    amount = request.data.get("amount")

    
    if Booking.objects.filter(id=booking_ref).exists():
        payment = Payment.objects.create(
            booking_reference=booking_ref,
            transaction_id=transaction_id,
            amount=amount,
        )
        return Response(
            {"message": "Payment created successfully", "id": payment.id},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"error": "The booking_reference is not available"},
            status=status.HTTP_404_NOT_FOUND
        )
'''
CHAPA_API_URL = "https://api.chapa.co/v1/transaction/initialize"
secret_key = settings.CHAPA_SECRET_KEY
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
       amount=request.data.get("amount")
       ref_tx=str(uuid.uuid4())
       email = request.data.get("email")
       first_name = request.data.get("first_name")
       last_name = request.data.get("last_name")
       
       headers={
              "Authorization":f"Bearer {secret_key}",
              "content-type":"Application/json"
       }
       payload = {
        "amount": str(amount),
        "currency": "ETB",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "tx_ref": ref_tx,
        "callback_url": "http://localhost:8000/api/payment/verify/",
        "return_url": "http://localhost:8000/payment-success/",
        "customization": {
            "title": "Travel Booking Payment",
            "description": "Booking payment via Chapa"
        }
       response=requests.post(CHAPA_API_URL,data=payload,headers=headers)
       
       data = response.json()
       if response.status_code == 200 and data.get("status") == "success":
          Payment.objects.create(
            booking_reference=ref_tx,
            transaction_id=data["data"]["tx_ref"],
            amount=amount,
            status="PENDING"
          )

          return Response({
                "payment_url": data["data"]["checkout_url"],
                "reference": ref_tx
        })

      return Response(
          {"error": "Payment initiation failed"},
          status=status.HTTP_400_BAD_REQUEST
      )

       
  
@api_view(["GET"])
def verify_payment(request):
    tx_ref = request.GET.get("tx_ref")

    payment = Payment.objects.filter(transaction_id=tx_ref).first()
    if not payment:
        return Response({"error": "Invalid transaction"}, status=404)

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.get(
        f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}",
        headers=headers
    )

    data = response.json()

    if data.get("status") == "success":
        payment.status = "COMPLETED"
        payment.save()

        send_payment_email.delay(payment.booking_reference)

        return Response({"message": "Payment verified successfully"})

    payment.status = "FAILED"
    payment.save()

    return Response({"message": "Payment failed"}, status=400)

  
