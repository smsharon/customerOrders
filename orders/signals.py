"""
Signal handlers for Order-related events.
This module handles automatic creation of transactions,
order state tracking, stock updates, and SMS notifications
via Africa's Talking API.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order, OrderItem, Transaction, Inventory, Customer
import africastalking
from africastalking.SMS import SMSService
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

# Initialize Africa's Talking SDK
AT_USERNAME = getattr(settings, "AFRICASTALKING_USERNAME", "sandbox")
AT_API_KEY = getattr(settings, "AFRICASTALKING_API_KEY", "")

sms = SMSService(AT_USERNAME, AT_API_KEY)


def send_sms(phone_number, message):
    """
    Send an SMS message using Africa's Talking SMS service.

    Args:
        phone_number (str): The recipient's phone number.
        message (str): The message body.

    Returns:
        dict | None: API response if successful, None if sending fails.
    """
    try:
        response = sms.send(message, [phone_number])
        print("SMS Response:", response)  
        return response
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return None


@receiver(pre_save, sender=Order)
def track_order_state(sender, instance, **kwargs):
    """
    Signal handler to track the previous state of an Order
    before it is saved. This allows detection of state transitions.

    Args:
        sender (Model): The model class (`Order`).
        instance (Order): The Order instance being saved.
        kwargs: Additional keyword arguments.
    """
    if instance.pk:  # existing order
        try:
            old = Order.objects.get(pk=instance.pk)
            instance._old_state = old.state
        except Order.DoesNotExist:
            instance._old_state = None
    else:
        instance._old_state = None


@receiver(post_save, sender=Order)
def create_order_transactions(sender, instance, created, **kwargs):
    """
    Signal handler to log transactions and send SMS notifications
    whenever an Order is created or updated.

    Actions:
        - On creation: Creates a CREATE_ORDER transaction and sends SMS.
        - On update: Creates an UPDATE_ORDER transaction.
        - On state change:
            * Logs state transition in Transaction table.
            * Deducts inventory when state changes to FULFILLED.
            * Sends SMS notifications for FULFILLED or CANCELLED states.

    Args:
        sender (Model): The model class (`Order`).
        instance (Order): The Order instance being saved.
        created (bool): True if a new Order was created, False if updated.
        kwargs: Additional keyword arguments.
    """
    if created:
        # New order  create CREATE_ORDER transaction
        Transaction.objects.create(
            order=instance,
            action="CREATE_ORDER",
            description="Order created"
        )
        # Send SMS on order placed
        send_sms(instance.customer.phone_number, f"Your order {instance.id} has been placed.")
    else:
        # Order updated  log UPDATE_ORDER
        Transaction.objects.create(
            order=instance,
            action="UPDATE_ORDER",
            description="Order updated"
        )

        # If state has changed
        old_state = getattr(instance, "_old_state", None)
        if old_state and old_state != instance.state:
            # Log state change
            Transaction.objects.create(
                order=instance,
                action=f"STATE_{instance.state}",
                description=f"Order moved from {old_state} to {instance.state}"
            )

            # Handle specific transitions
            if instance.state == "FULFILLED":
                # Deduct stock
                for item in OrderItem.objects.filter(order=instance):
                    inv = item.inventory
                    inv.on_hand -= item.quantity
                    inv.save()

                # Send SMS
                send_sms(instance.customer.phone_number, f"Your order {instance.id} has been fulfilled.")

            elif instance.state == "CANCELLED":
                send_sms(instance.customer.phone_number, f"Your order {instance.id} has been cancelled.")
