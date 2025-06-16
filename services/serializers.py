import base64
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import (Cart, CartItem, FurnitureAssemblyOption, Location, ServiceType, AssemblyType,
                     GazeboServiceOption, GazeboModel,
                     InstallationServiceOption, InstallationType,
                     ServiceCategory,
                     TVMountingOption,
                     Order,
                     OrderItem)


def serialize_service_option(obj):
    if obj is None:
        return None
    if isinstance(obj, TVMountingOption):
        return TVMountingOptionSerializer(obj).data
    elif isinstance(obj, FurnitureAssemblyOption):
        return FurnitureAssemblyOptionSerializer(obj).data
    elif isinstance(obj, InstallationServiceOption):
        return InstallationServiceOptionSerializer(obj).data
    elif isinstance(obj, GazeboServiceOption):
        return GazeboServiceOptionSerializer(obj).data
    return None

class UserInfoMixin:
    def get_user_info(self, obj):
        user = getattr(obj, 'user', None)
        if user:
            return {'id': user.id, 'username': user.username, 'email': user.email}
        return None

class BaseServiceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ['id']

class TVMountingOptionSerializer(BaseServiceOptionSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())

    class Meta(BaseServiceOptionSerializer.Meta):
        model = TVMountingOption

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']
        read_only_fields = ['id']

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name']
        read_only_fields = ['id']

class AssemblyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyType
        fields = ['id', 'name']
        read_only_fields = ['id']

class FurnitureAssemblyOptionSerializer(BaseServiceOptionSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source='location', write_only=True, required=False, allow_null=True)
    service_type = ServiceTypeSerializer(read_only=True)
    service_type_id = serializers.PrimaryKeyRelatedField(queryset=ServiceType.objects.all(), source='service_type', write_only=True, required=False, allow_null=True)
    assembly_type = AssemblyTypeSerializer(read_only=True)
    assembly_type_id = serializers.PrimaryKeyRelatedField(queryset=AssemblyType.objects.all(), source='assembly_type', write_only=True, required=False, allow_null=True)

    class Meta(BaseServiceOptionSerializer.Meta):
        model = FurnitureAssemblyOption
        fields = ['id', 'category', 'title', 'description', 'related_image', 'price', 'quantity', 'location', 'location_id', 'service_type', 'service_type_id', 'assembly_type', 'assembly_type_id', 'created_at']
        read_only_fields = BaseServiceOptionSerializer.Meta.read_only_fields

class InstallationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationType
        fields = ['id', 'name', 'photo', 'description']
        read_only_fields = ['id']

class InstallationServiceOptionSerializer(BaseServiceOptionSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())
    installation_type = InstallationTypeSerializer(read_only=True)
    installation_type_id = serializers.PrimaryKeyRelatedField(queryset=InstallationType.objects.all(), source='installation_type', write_only=True, required=False, allow_null=True)

    class Meta(BaseServiceOptionSerializer.Meta):
        model = InstallationServiceOption
        fields = ['id', 'category', 'title', 'description', 'related_image', 'price', 'quantity', 'installation_type', 'installation_type_id', 'location', 'power_nearby', 'created_at']
        read_only_fields = BaseServiceOptionSerializer.Meta.read_only_fields

class GazeboModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GazeboModel
        fields = ['id', 'name', 'photo', 'description']
        read_only_fields = ['id']

class GazeboServiceOptionSerializer(BaseServiceOptionSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())
    gazebo_model = GazeboModelSerializer(read_only=True)
    gazebo_model_id = serializers.PrimaryKeyRelatedField(queryset=GazeboModel.objects.all(), source='gazebo_model', write_only=True, required=False, allow_null=True)

    class Meta(BaseServiceOptionSerializer.Meta):
        model = GazeboServiceOption
        fields = ['id', 'category', 'title', 'description', 'related_image', 'price', 'quantity', 'action', 'gazebo_model', 'gazebo_model_id', 'size', 'anchoring', 'created_at'
        ]
        read_only_fields = BaseServiceOptionSerializer.Meta.read_only_fields


class ServiceCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ServiceCategory model.
    """

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'feature_image', 'created_at']
        read_only_fields = ['id', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    """
    Improved serializer for CartItem model, handling generic relations and providing detailed service option data.
    """
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    object_id = serializers.IntegerField()
    service_option = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'content_type', 'object_id', 'service_option', 'quantity', 'total_price']

    def get_service_option(self, obj):
        return serialize_service_option(obj.service_option)

    def get_total_price(self, obj):
        if obj.service_option and hasattr(obj.service_option, 'price'):
            return obj.quantity * float(obj.service_option.price)
        return 0


class CartSerializer(serializers.ModelSerializer):
    """
    Improved serializer for Cart model, providing user info, item count, and robust total price calculation.
    """
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'item_count', 'total_price', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = validated_data.pop('user')
        cart = Cart.objects.create(user=user, **validated_data)
        return cart

    def get_total_price(self, obj):
        """
        Calculates the total price of all items in the cart, safely handling missing prices.
        """
        total = 0
        for item in obj.items.all():
            price = getattr(item.service_option, 'price', 0) or 0
            try:
                total += item.quantity * float(price)
            except Exception:
                continue
        return total

    def get_item_count(self, obj):
        return obj.items.count()

    def get_user(self, obj):
        user = getattr(obj, 'user', None)
        if user:
            return {'id': user.id, 'username': user.username, 'email': user.email}
        return None


class OrderItemSerializer(serializers.ModelSerializer):
    service_option = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'content_type', 'object_id', 'service_option', 'quantity', 'price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'service_option']

    def get_service_option(self, obj):
        return serialize_service_option(obj.service_option)


class OrderSerializer(UserInfoMixin, serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=False, allow_null=True)
    user_info = serializers.SerializerMethodField(read_only=True)
    guest_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    guest_email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    guest_phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_info', 'guest_name', 'guest_email', 'guest_phone', 'cart', 'items', 'total_price', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'items', 'user_info']

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        order = Order.objects.create(user=user, **validated_data)
        return order

    def validate(self, data):
        user = data.get('user')
        guest_email = data.get('guest_email')
        guest_phone = data.get('guest_phone')
        if not user and not (guest_email or guest_phone):
            raise serializers.ValidationError('Guest orders must include at least an email or phone.')
        return data
