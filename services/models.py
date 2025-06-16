from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .help_functions import upload_to_service
from uuid import uuid4


class ServiceCategory(models.Model):
    """
    Represents a category for services.
    """
    name = models.CharField(max_length=255, unique=True,
                            verbose_name=_("Category Name"))
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Category Description")
    )
    feature_image = models.ImageField(
        upload_to=upload_to_service,
        blank=True,
        null=True,
        verbose_name=_("Category Image"),
        help_text=_("A representing image for this category."),
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")


class BaseServiceOption(models.Model):
    
    """
    Abstract base class for service options.   
    """
    YES_NO_CHOICES = [
        ('YES', _('Yes')),
        ('NO', _('No')),
    ]
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name="%(class)s_options", verbose_name=_("Service")
    )
    title = models.CharField(max_length=100, blank=True,
                             null=True, verbose_name=_("Service Title"))
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Service Description"))
    related_image = models.ImageField(
        upload_to=upload_to_service, blank=True, null=True,
        help_text=_("Image to the selected service model.")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Service Price"),
        validators=[MinValueValidator(0)],
    )
    quantity = models.PositiveIntegerField(
        default=1, help_text=_("Number of services requested."), verbose_name=_("Quantity"),
        validators=[MinValueValidator(1)],
    )
    needs_moving_help = models.CharField(
        choices=YES_NO_CHOICES, default="NO", help_text=_("Whether moving help is required."), verbose_name=_("Moving Help")
    )
    moving_help_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Additional charge for moving help."),
        verbose_name=_("Moving Help Charge"),
        validators=[MinValueValidator(0)],
    )

    class Meta:
        abstract = True


class TVMountingOption(BaseServiceOption):
    """
    Represents TV mounting options for a service.
    """
    needs = models.CharField(
        max_length=20,
        choices=[
            ('MOUNTING', _('Mounting')),
            ('UNMOUNTING', _('Unmounting')),
            ('BOTH', _('Mounting and Unmounting')),
        ],
        default='MOUNTING',
        verbose_name=_('Needs')
    )
    bracket = models.CharField(
        max_length=20,
        choices=[
            ('OWN', _('I have my own bracket')),
            ('FLAT', _('Flat bracket')),
            ('TILT', _('Tilt bracket')),
            ('FULL_MOTION', _('Full motion bracket')),
        ],
        default='OWN',
        verbose_name=_('Bracket')
    )
    bracket_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Price if bracket is provided."),
        verbose_name=_('Bracket Price')
    )
    wall_type = models.CharField(
        max_length=20,
        choices=[
            ('DRY_WALL', _('Dry Wall')),
            ('CONCRETE', _('Concrete Wall')),
            ('STONE', _('Stone')),
            ('BRICKS', _('Bricks')),
        ],
        default='DRY_WALL',
        verbose_name=_('Wall Type')
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("TV Mounting Option")
        verbose_name_plural = _("TV Mounting Options")


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Location'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')


class ServiceType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Service Type'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service Type')
        verbose_name_plural = _('Service Types')


class AssemblyType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Assembly Type'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Assembly Type')
        verbose_name_plural = _('Assembly Types')


class FurnitureAssemblyOption(BaseServiceOption):
    """
    Represents furniture assembly options for a service.
    """
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Location'))
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Service Type'))
    assembly_type = models.ForeignKey(AssemblyType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Assembly Type'))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Furniture Assembly Option")
        verbose_name_plural = _("Furniture Assembly Options")


class InstallationType(models.Model):
    """
    Represents a type of installation with name, photo, and description.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Installation Type Name'))
    photo = models.ImageField(upload_to=upload_to_service, blank=True, null=True, verbose_name=_('Installation Type Photo'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Installation Type Description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Installation Type')
        verbose_name_plural = _('Installation Types')


class InstallationServiceOption(BaseServiceOption):
    """
    Represents installation service options.
    """
    installation_type = models.ForeignKey(
        'InstallationType', on_delete=models.SET_NULL, blank=True, null=True, related_name='service_options', verbose_name=_('Installation Type'))
    location = models.CharField(
        max_length=20,
        choices=[
            ('INDOOR', _('Indoor')),
            ('OUTDOOR', _('Outdoor')),
            ('BOTH', _('Both')),
        ],
        verbose_name=_('Location')
    )
    power_nearby = models.CharField(
        max_length=20,
        choices=[
            ('NO', _('No')),
            ('YES', _('Yes')),
            ('NOT_SURE', _('Not Sure')),
        ],
        default='NOT_SURE',
        verbose_name=_('Power Nearby')
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Installation Service Option")
        verbose_name_plural = _("Installation Service Options")


class GazeboModel(models.Model):
    """
    Represents a specific gazebo model with name, photo, and description.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Model Name'))
    photo = models.ImageField(upload_to=upload_to_service, blank=True, null=True, verbose_name=_('Model Photo'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Model Description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Gazebo Model')
        verbose_name_plural = _('Gazebo Models')


class GazeboServiceOption(BaseServiceOption):
    ACTION_CHOICES = [
        ('INSTALLATION', 'Installation'),
        ('UNINSTALLATION', 'Uninstallation'),
        ('REPLACEMENT', 'Replacement'),
        ('COMPLETION', 'Completion'),
    ]
    SIZE_CHOICES = [
        ('10X10', '10x10 ft'),
        ('12X12', '12x12 ft'),
        ('12X16', '12x16 ft'),
        ('12X20', '12x20 ft'),
        ('CUSTOM', 'Custom'),
    ]
    YES_NO_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]
    action = models.CharField(
        max_length=20, choices=ACTION_CHOICES, default='INSTALLATION')
    gazebo_model = models.ForeignKey(
        'GazeboModel', on_delete=models.SET_NULL, blank=True, null=True, related_name='service_options', verbose_name=_('Gazebo Model'))
    size = models.CharField(
        max_length=20, choices=SIZE_CHOICES, blank=True, null=True)
    anchoring = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, default='NO')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Gazebo Assembly Option")
        verbose_name_plural = _("Gazebo Assembly Options")


class Cart(models.Model):
    """
    Represents a shopping cart for a user.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, verbose_name=_("Cart ID")
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart", verbose_name=_("User")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"Cart for {self.user.username}"

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")


class CartItem(models.Model):
    """
    Represents an item in a shopping cart.
    """
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", verbose_name=_("Cart")
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"),
        help_text=_('The type of the related service option.')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("Object ID"), help_text=_('The ID of the related service option object.')
    )
    service_option = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_("Quantity"), help_text=_("Number of this service option in the cart."),
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        service_title = getattr(self.service_option, 'title', str(self.service_option))
        username = getattr(getattr(self.cart, 'user', None), 'username', 'unknown')
        return f"{self.quantity} x {service_title} in {username}'s cart"

    class Meta:
        unique_together = [('cart', 'content_type', 'object_id')]
        ordering = ['cart']
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        indexes = [
            models.Index(fields=['cart']),
        ]


class Order(models.Model):
    """
    Represents a finalized order created from a cart.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('Order ID'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name=_('User'), null=True, blank=True)
    # Guest contact fields
    guest_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Guest Name'))
    guest_email = models.EmailField(blank=True, null=True, verbose_name=_('Guest Email'))
    guest_phone = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('Guest Phone'))
    cart = models.OneToOneField('Cart', on_delete=models.SET_NULL, null=True, blank=True, related_name='order', verbose_name=_('Cart'))
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Total Price'))
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', _('Pending')),
            ('PAID', _('Paid')),
            ('CANCELLED', _('Cancelled')),
            ('COMPLETED', _('Completed')),
        ],
        default='PENDING',
        verbose_name=_('Status')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        if self.user:
            return f"Order {self.id} for {self.user.username} - {self.status}"
        return f"Order {self.id} (Guest: {self.guest_name or 'N/A'}) - {self.status}"

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def clean(self):
        # Ensure guest contact info is present if user is not set
        if not self.user and not (self.guest_email or self.guest_phone):
            from django.core.exceptions import ValidationError
            raise ValidationError(_('Guest orders must include at least an email or phone.'))


class OrderItem(models.Model):
    """
    Represents an item within an order, referencing the same service options as CartItem.
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_('Content Type'),
        help_text=_('The type of the related service option.')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('Object ID'), help_text=_('The ID of the related service option object.')
    )
    service_option = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_('Quantity'), help_text=_('Number of this service option in the order.'),
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('Price'),
        help_text=_('Price of the service option at the time of order.')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        service_title = getattr(self.service_option, 'title', str(self.service_option))
        return f"{self.quantity} x {service_title} in Order {self.order_id}"

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ['order']
        indexes = [
            models.Index(fields=['order']),
        ]
