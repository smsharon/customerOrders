import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch


@pytest.mark.django_db
def test_customer_registration():
    """
    Test that a customer can successfully register.

    Steps:
    - Send POST request to the registration endpoint with valid data.
    - Verify response status is 201 (created).
    - Ensure the response contains the new customer ID and phone number.
    """
    client = APIClient()
    url = reverse("customer-register")
    data = {
        "name": "Test User",
        "phone_number": "0712345678",
        "code": "testuser01",
        "password": "TestPass123!",
        "email": "testuser@example.com"
    }

    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert "id" in response.data
    assert response.data["phone_number"].endswith("5678")


@pytest.mark.django_db
def test_token_authentication(customer_factory, django_user_model):
    """
    Test that a user can obtain JWT tokens via the authentication endpoint.

    Steps:
    - Create a test user.
    - Post username and password to the token endpoint.
    - Verify access and refresh tokens are returned in response.
    """
    user = django_user_model.objects.create_user(
        username="testuser",
        password="testpass123"
    )
    client = APIClient()
    url = reverse("token_obtain_pair")
    response = client.post(url, {"username": "testuser", "password": "testpass123"})
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
@patch("orders.signals.sms.send")
def test_order_creation(mock_sms, customer_factory, inventory_factory, auth_client):
    """
    Test order creation process with valid customer and inventory.

    Steps:
    - Create a test customer and inventory item.
    - Send POST request to order creation endpoint.
    - Verify order is created and items are linked to inventory.
    - Ensure SMS notification function is called.
    """
    customer = customer_factory(user=auth_client.handler._force_user)
    inventory = inventory_factory(on_hand=10, warn_limit=5)

    url = reverse("order-list")
    data = {
        "customer": customer.id,
        "items": [
            {"inventory_id": inventory.id, "quantity": 2}
        ]
    }

    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201

    from orders.models import Order
    order = Order.objects.get(id=response.data["id"])
    assert order.customer == customer
    assert order.items.count() == 1
    assert order.items.first().inventory == inventory
    assert order.items.first().quantity == 2

    assert mock_sms.call_count >= 1
