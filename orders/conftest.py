import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from orders.models import Customer, Inventory

User = get_user_model()


@pytest.fixture
def customer_factory():
    """Factory fixture to create Customer instances with an associated User."""
    def create_customer(**kwargs):
        user = kwargs.pop("user", None) or User.objects.create_user(
            username="testuser",
            password="pass1234"
        )
        defaults = {
            "user": user,
            "name": "Customer A",
            "phone_number": "0712345678",
            "code": "CUST001",
        }
        defaults.update(kwargs)
        return Customer.objects.create(**defaults)
    return create_customer


@pytest.fixture
def inventory_factory():
    """Factory fixture to create Inventory items with sensible defaults."""
    def create_inventory(**kwargs):
        defaults = {
            "name": "Item A",
            "on_hand": 10,
            "warn_limit": 5,
        }
        defaults.update(kwargs)
        return Inventory.objects.create(**defaults)
    return create_inventory


@pytest.fixture
def auth_client():
    """Fixture that returns an authenticated APIClient instance."""
    user = User.objects.create_user(username="authuser", password="pass1234")
    client = APIClient()
    client.force_authenticate(user=user)
    return client
