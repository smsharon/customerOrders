"""
Defines the application models.
"""
from django.db import models
from django.utils.timezone import now
from . import constants
from django.conf import settings


class Customer(models.Model):
    """
    Customer model representing customers in the system.

    Attributes:
        user (OneToOneField): Link to the Django User model.
        name (CharField): Full name of the customer.
        code (CharField): Unique customer code identifier.
        phone_number (CharField): Unique phone number, normalized to +254 format.

    Methods:
        save(): Overrides save to normalize phone number format.
        __str__(): Returns a human-readable representation of the customer.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        """
        Normalize the phone number before saving:
        - Converts numbers starting with '0' into +254 format.
        - Ensures all numbers start with '+'.
        """
        if self.phone_number.startswith("0"):
            self.phone_number = "+254" + self.phone_number[1:]
        elif not self.phone_number.startswith("+"):
            self.phone_number = "+" + self.phone_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Inventory(models.Model):
    """
    Inventory model representing items available for sale.

    Attributes:
        name (CharField): Unique name of the inventory item.
        on_hand (IntegerField): Quantity of the item currently in stock.
        warn_limit (IntegerField): Threshold to warn when stock is low.
        created_at (DateTimeField): Timestamp of creation.

    Methods:
        get_status(): Returns the availability status based on stock level.
        __str__(): Returns a human-readable representation of the inventory.
    """
    name = models.CharField(max_length=120, unique=True)
    on_hand = models.IntegerField(default=0)
    warn_limit = models.IntegerField(default=5)
    created_at = models.DateTimeField(default=now)

    def get_status(self):
        """
        Returns the stock status:
        - OUT_OF_STOCK if no items are left.
        - FEW_REMAINING if stock is at or below the warning limit.
        - AVAILABLE otherwise.
        """
        if self.on_hand == 0:
            return constants.INVENTORY_STATUS["OUT_OF_STOCK"]
        elif self.on_hand <= self.warn_limit:
            return constants.INVENTORY_STATUS["FEW_REMAINING"]
        return constants.INVENTORY_STATUS["AVAILABLE"]

    def __str__(self):
        return f"{self.name} (On Hand: {self.on_hand})"


class Order(models.Model):
    """
    Order model representing customer orders.

    Attributes:
        customer (ForeignKey): The customer placing the order.
        state (CharField): Current state of the order (Draft, Submitted, etc.).
        created_at (DateTimeField): Timestamp of order creation.

    Methods:
        __str__(): Returns a human-readable representation of the order.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    state = models.CharField(
        max_length=20,
        choices=[(key, value) for key, value in constants.ORDER_STATES.items()],
        default="DRAFT"
    )
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Order {self.id} - {self.customer.name} ({self.state})"


class OrderItem(models.Model):
    """
    OrderItem model representing individual items in an order.

    Attributes:
        order (ForeignKey): The order this item belongs to.
        inventory (ForeignKey): The inventory item being ordered.
        quantity (IntegerField): Quantity of the item ordered.
        price_at_order (DecimalField): Price at the time of ordering.

    Methods:
        __str__(): Returns a human-readable representation of the order item.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Item {self.id} (Order {self.order.id})"


class Transaction(models.Model):
    """
    Transaction model for logging order-related actions.

    Attributes:
        order (ForeignKey): The order associated with the transaction.
        customer (ForeignKey): The customer responsible (nullable).
        action (CharField): The action performed (e.g., CREATE_ORDER, APPROVE_ORDER).
        description (TextField): Additional details about the action.
        timestamp (DateTimeField): Timestamp when the transaction occurred.

    Methods:
        __str__(): Returns a human-readable representation of the transaction.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transactions")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(
        max_length=50,
        choices=[(key, val) for key, val in constants.TRANSACTION_ACTIONS.items()]
    )
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} on Order #{self.order.id} by {self.customer}"
