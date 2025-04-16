from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    ServiceCategoryViewSet,
    TVMountingOptionViewSet,
    FurnitureAssemblyOptionViewSet,
    InstallationServiceOptionViewSet,
    GazeboServiceOptionViewSet,
    CartViewSet,
    CartItemViewSet,
)

# Create a router and register the viewsets
router = routers.DefaultRouter()
router.register(r'service-categories', ServiceCategoryViewSet, basename='service-category')
router.register(r'tv-mounting-options', TVMountingOptionViewSet, basename='tv-mounting-option')
router.register(r'furniture-assembly-options', FurnitureAssemblyOptionViewSet, basename='furniture-assembly-option')
router.register(r'installation-service-options', InstallationServiceOptionViewSet, basename='installation-service-option')
router.register(r'gazebo-service-options', GazeboServiceOptionViewSet, basename='gazebo-service-option')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')

# Nested routers for cart items
cart_router = routers.NestedDefaultRouter(router, r'cart', lookup='cart')
cart_router.register(r'items', CartItemViewSet, basename='cart-items')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
]