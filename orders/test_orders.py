import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch

@pytest.mark.django_db
def test_customer_registration():
    client = APIClient()
    url = reverse("customer-register")  # adjust if your URL name is different
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
    user = django_user_model.objects.create_user(
        username="testuser",
        password="testpass123"
    )
    client = APIClient()
    url = reverse("token_obtain_pair")  # SimpleJWT endpoint
    response = client.post(url, {"username": "testuser", "password": "testpass123"})
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
@patch("orders.signals.sms.send")
def test_order_creation(mock_sms, customer_factory, inventory_factory, auth_client):
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

    # Check that SMS was sent (allow multiple calls)
    assert mock_sms.call_count >= 1
