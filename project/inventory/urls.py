from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import *


router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'inventories', InventoryViewSet, basename='inventory')
router.register(r'movements', MovementViewSet, basename='movement')

urlpatterns = [
    path('', include(router.urls)),
]