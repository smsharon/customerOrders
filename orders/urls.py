"""
URL configuration for the application.
This module registers API endpoints for Customers, Inventory,
Orders, and Transactions using Django REST Framework routers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, InventoryViewSet, OrderViewSet, TransactionViewSet

# Create a default router and register API viewsets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'transactions', TransactionViewSet)

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
