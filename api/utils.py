import os
from django.core.mail import send_mail
from django.conf import settings
import africastalking


AFRICASTALKING_USERNAME = os.environ.get("AFRICASTALKING_USERNAME")
AFRICASTALKING_API_KEY = os.environ.get("AFRICASTALKING_API_KEY")


def send_order_notification(order):
    """
    Sends notification for a new order.
    """

    subject = f"New Order #{order.uuid}"
    message = f"Customer: {order.customer.first_name}\nItems: {[str(item) for item in order.items.all()]}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
    )

    # Send SMS
    africastalking.initialize(AFRICASTALKING_USERNAME, AFRICASTALKING_API_KEY)
    sms = africastalking.SMS
    if order.customer.phone:
        sms.send(f"Order #{order.uuid} placed successfully.", [order.customer.phone])
