from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import (CartItemSerializer, CartSerializer, FurnitureAssemblyOptionSerializer,
                          GazeboServiceOptionSerializer,
                          InstallationServiceOptionSerializer,
                          ServiceCategorySerializer,
                          TVMountingOptionSerializer)
from .models import (Cart, CartItem, FurnitureAssemblyOption,
                     GazeboServiceOption,
                     InstallationServiceOption,
                     ServiceCategory,
                     TVMountingOption)

# Create your views here.


def service_list(request):
    categories = ServiceCategory.objects.prefetch_related('services').all()
    return render(request, 'services/list.html', {'categories': categories})


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and retrieving Service Categories.
    """
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class TVMountingOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving TV Mounting Options.
    """
    queryset = TVMountingOption.objects.all()
    serializer_class = TVMountingOptionSerializer


class FurnitureAssemblyOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving Furniture Assembly Options.
    """
    queryset = FurnitureAssemblyOption.objects.all()
    serializer_class = FurnitureAssemblyOptionSerializer


class InstallationServiceOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving Installation Service Options.
    """
    queryset = InstallationServiceOption.objects.all()
    serializer_class = InstallationServiceOptionSerializer


class GazeboServiceOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving Gazebo Service Options.
    """
    queryset = GazeboServiceOption.objects.all()
    serializer_class = GazeboServiceOptionSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing the Cart.
    """
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects \
            .prefetch_related('items__service_option').all()

    serializer_class = CartSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Cart Items.
    """
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('service_option')

    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['cart_pk']
        }
    serializer_class = CartItemSerializer
