from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, InventoryViewSet, OrderViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
