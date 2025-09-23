"""
Defines the aqpplication models.
"""
from django.db import models
from django.utils.timezone import now
from . import constants


"""
Customer model representing customers in the system.
"""
class Customer(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

"""
Inventory model representing items available for sale.
"""
class Inventory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    on_hand = models.IntegerField(default=0)
    warn_limit = models.IntegerField(default=5)
    created_at = models.DateTimeField(default=now)

    def get_status(self):
        """
        Returns the inventory status based on stock availability.
        """
        if self.on_hand == 0:
            return constants.INVENTORY_STATUS["OUT_OF_STOCK"]
        elif self.on_hand <= self.warn_limit:
            return constants.INVENTORY_STATUS["FEW_REMAINING"]
        return constants.INVENTORY_STATUS["AVAILABLE"]

    def __str__(self):
        return f"{self.name} (On Hand: {self.on_hand})"

"""
Order model representing customer orders.
"""
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    state = models.CharField(
        max_length=20,
        choices=[(key, value) for key, value in constants.ORDER_STATES.items()],
        default="DRAFT"
    )
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Order {self.id} - {self.customer.name} ({self.state})"

"""
OrderItem model representing items in an order.
"""
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Item {self.id} (Order {self.order.id})"

"""
Model to log transaction actions like order state updates.
"""
class Transaction(models.Model):
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
