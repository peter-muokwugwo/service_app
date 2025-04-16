import base64
from rest_framework import serializers
from .models import (Cart, CartItem, FurnitureAssemblyOption,
                     GazeboServiceOption,
                     InstallationServiceOption, 
                     ServiceCategory,
                     TVMountingOption)


class ServiceCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ServiceCategory model.
    """

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'feature_image', 'created_at']
        read_only_fields = ['id', 'created_at']


class TVMountingOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the TVMountingOption model.
    """

    class Meta:
        model = TVMountingOption
        fields = [
            'id', 'category', 'title', 'description', 'needs', 'bracket',
            'bracket_price', 'wall_type', 'quantity', 'price'
        ]
        read_only_fields = ['id']


class FurnitureAssemblyOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the FurnitureAssemblyOption model.
    """

    class Meta:
        model = FurnitureAssemblyOption
        fields = [
            'id', 'category', 'title', 'description', 'location', 'service_type',
            'assembly_type', 'needs_moving_help', 'moving_help_charge', 'quantity', 'price'
        ]
        read_only_fields = ['id']


class InstallationServiceOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the InstallationServiceOption model.
    """

    class Meta:
        model = InstallationServiceOption
        fields = [
            'id', 'category', 'title', 'description', 'installation_type',
            'location', 'power_nearby', 'quantity', 'price'
        ]
        read_only_fields = ['id']


class GazeboServiceOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the GazeboServiceOption model.
    """

    class Meta:
        model = GazeboServiceOption
        fields = [
            'id', 'category', 'title', 'description', 'action', 'gazebo_model',
            'size', 'anchoring', 'related_image', 'price'
        ]
        read_only_fields = ['id']


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model.
    """
    service_option_title = serializers.CharField(source='service_option.title', read_only=True)
    service_option_price = serializers.DecimalField(
        source='service_option.price', max_digits=10, decimal_places=2, read_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'service_option', 'service_option_title', 'service_option_price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        """
        Calculates the total price for this cart item.
        """
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model.
    """
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_total_price(self, obj):
        """
        Calculates the total price of all items in the cart.
        """
        return obj.get_total_price()
