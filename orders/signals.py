from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order, OrderItem, Transaction, Inventory, Customer

# --- Configure Africa's Talking (SMS only) ---
from africastalking.SMS import SMSService

import uuid

from django.contrib.auth import get_user_model

User = get_user_model()

#@receiver(post_save, sender=User)
#def create_customer_for_new_user(sender, instance, created, **kwargs):
    #if created:
        #customer_code = str(uuid.uuid4())[:8].upper()
        #Customer.objects.create(
           # user=instance,  # <-- FIX: Link to user!
            #name=instance.username or "Unknown",
            #code=customer_code,
            #phone_number="0000000000"  # placeholder, update later
        #)

AT_USERNAME = getattr(settings, "AFRICASTALKING_USERNAME", "sandbox")
AT_API_KEY = getattr(settings, "AFRICASTALKING_API_KEY", "")

sms = SMSService(AT_USERNAME, AT_API_KEY)

def send_sms(phone_number, message):
    """Send SMS via Africa's Talking, wrapped in try/except."""
    try:
        sms.send(message, [phone_number])
    except Exception as e:
        print(f"SMS sending failed: {e}")

# --- Track state before saving for comparison ---
@receiver(pre_save, sender=Order)
def track_order_state(sender, instance, **kwargs):
    """Store old state before saving for transition detection."""
    if instance.pk:  # existing order
        try:
            old = Order.objects.get(pk=instance.pk)
            instance._old_state = old.state
        except Order.DoesNotExist:
            instance._old_state = None
    else:
        instance._old_state = None

# --- Create transaction and SMS after save ---
@receiver(post_save, sender=Order)
def create_order_transactions(sender, instance, created, **kwargs):
    if created:
        # New order → create CREATE_ORDER transaction
        Transaction.objects.create(
            order=instance,
            action="CREATE_ORDER",
            description="Order created"
        )
        # Send SMS on order placed
        send_sms(instance.customer.phone_number, f"Your order {instance.id} has been placed.")
    else:
        # Order updated → log UPDATE_ORDER
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