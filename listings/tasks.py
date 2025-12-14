from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_email(booking_reference):
  send_mail(
       subject="Payment Successful",
        message=f"Your payment for booking {booking_reference} was successful.",
        from_email="noreply@travelapp.com",
        recipient_list=["user@example.com"],
        fail_silently=True
  )
