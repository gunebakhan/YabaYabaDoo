from django.core import mail
from celery import shared_task
from django.core.mail import send_mail
from .models import ShopOrder


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = ShopOrder.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.user.get_full_name},\n\n' \
        f'You have successfully places and order.' \
        f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.user.email])
    return mail_sent
