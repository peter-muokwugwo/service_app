from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import (CartItemSerializer, CartSerializer, FurnitureAssemblyOptionSerializer,
                          GazeboServiceOptionSerializer,
                          InstallationServiceOptionSerializer,
                          ServiceCategorySerializer,
                          TVMountingOptionSerializer, OrderSerializer, OrderItemSerializer)
from .models import (Cart, CartItem, FurnitureAssemblyOption,
                     GazeboServiceOption,
                     InstallationServiceOption,
                     ServiceCategory,
                     TVMountingOption, Order, OrderItem)

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


class TVMountingOptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing TV Mounting Options.
    """
    queryset = TVMountingOption.objects.all()
    serializer_class = TVMountingOptionSerializer


class FurnitureAssemblyOptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Furniture Assembly Options.
    """
    queryset = FurnitureAssemblyOption.objects.all()
    serializer_class = FurnitureAssemblyOptionSerializer


class InstallationServiceOptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Installation Service Options.
    """
    queryset = InstallationServiceOption.objects.all()
    serializer_class = InstallationServiceOptionSerializer


class GazeboServiceOptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Gazebo Service Options.
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
        cart_pk = self.kwargs.get('cart_pk', None)
        qs = CartItem.objects.all()
        if cart_pk:
            qs = qs.filter(cart_id=cart_pk)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        cart_pk = self.kwargs.get('cart_pk', None)
        if cart_pk:
            context['cart_id'] = cart_pk
        return context
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Orders.
    """
    queryset = Order.objects.prefetch_related('items').select_related('user', 'cart')
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Optionally set user from request if using authentication
        # serializer.save(user=self.request.user)
        serializer.save()


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Order Items.
    """
    queryset = OrderItem.objects.select_related('order', 'content_type')
    serializer_class = OrderItemSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_pk = self.kwargs.get('order_pk', None)
        qs = OrderItem.objects.all().select_related('order', 'content_type')
        if order_pk:
            qs = qs.filter(order_id=order_pk)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        order_pk = self.kwargs.get('order_pk', None)
        if order_pk:
            context['order_id'] = order_pk
        return context
