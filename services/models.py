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
        upload_to="service_categories/",
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
    moving_help_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Additional charge for moving help."),
        verbose_name=_("Moving Help Charge"),
        validators=[MinValueValidator(0)],
    )
    needs_moving_help = models.BooleanField(
        default=False, help_text=_("Whether moving help is required."), verbose_name=_("Moving Help")
    )

    def get_total_price(self):
        base_price = self.price or 0
        moving_charge = self.moving_help_charge or 0 if self.needs_moving_help else 0
        return (base_price + moving_charge) * self.quantity

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

    def get_total_price(self):
        """
        Calculates the total price for this TV mounting option.
        """
        base_price = self.price or 0
        bracket_price = self.bracket_price or 0 if self.bracket != 'OWN' else 0
        moving_charge = self.moving_help_charge or 0 if self.needs_moving_help else 0
        unit_price = base_price + bracket_price + moving_charge
        return unit_price * self.quantity

    class Meta:
        verbose_name = _("TV Mounting Option")
        verbose_name_plural = _("TV Mounting Options")


class FurnitureAssemblyOption(BaseServiceOption):
    """
    Represents furniture assembly options for a service.
    """
    location = models.CharField(
        max_length=20,
        choices=[
            ('INDOOR', _('Indoor')),
            ('OUTDOOR', _('Outdoor')),
        ],
        default='INDOOR',
        verbose_name=_('Location')
    )
    service_type = models.CharField(
        max_length=20,
        choices=[
            ('ASSEMBLY', _('Assembly')),
            ('DISASSEMBLY', _('Disassembly')),
            ('BOTH', _('Assembly and Disassembly')),
        ],
        default='ASSEMBLY',
        verbose_name=_('Service Type')
    )
    assembly_type = models.CharField(
        max_length=20,
        choices=[
            ('FLAT_PACK', _('Flat Pack')),
            ('PRE_ASSEMBLED', _('Pre-Assembled')),
        ],
        default='FLAT_PACK',
        verbose_name=_('Assembly Type')
    )

    def __str__(self):
        moving = " with Moving Help" if self.needs_moving_help else ""
        return f"{self.title}"

    class Meta:
        verbose_name = _("Furniture Assembly Option")
        verbose_name_plural = _("Furniture Assembly Options")


class InstallationServiceOption(BaseServiceOption):
    """
    Represents installation service options.
    """
    installation_type = models.CharField(
        max_length=20,
        choices=[
            ('PLUMBING', _('Plumbing')),
            ('FITNESS', _('Fitness Equipment')),
            ('HOME_SECURITY', _('Home Security')),
            ('WALL_HANGING', _('Wall Hanging')),
            ('BABY_PROOF', _('Baby Proofing')),
            ('APPLIANCE', _('Appliance')),
            ('PLAYGROUND', _('Playground Equipment')),
            ('LIGHT_FIXTURE', _('Light Fixture')),
        ],
        verbose_name=_('Installation Type')
    )
    location = models.CharField(
        max_length=20,
        choices=[
            ('INDOOR', _('Indoor')),
            ('OUTDOOR', _('Outdoor')),
            ('BOTH', _('Indoor and Outdoor')),
        ],
        default='INDOOR',
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


class GazeboServiceOption(BaseServiceOption):
    ACTION_CHOICES = [
        ('INSTALLATION', 'Installation'),
        ('UNINSTALLATION', 'Uninstallation'),
        ('REPLACEMENT', 'Replacement'),
    ]
    GAZEBO_MODEL_CHOICES = [
        ('CEDAR', 'Cedar'),
        ('ALUMINIUM_DOUBLE_ROOF', 'Aluminium with Double Roof'),
        ('PATIO_DOUBLE_ROOF', 'Patio with Double Roof'),
        ('WOOD_PAVILION', 'Wood Pavilion'),
        ('GRAND', 'Grand'),
        ('MESSINA', 'Messina'),
        ('CAROLINA_PAVILION', 'Carolina Pavilion'),
        ('ALEXANDER_HARDTOP', 'Alexander Hardtop'),
        ('SANTA_MONICA', 'Santa Monica'),
        ('ARCHWOOD', 'Archwood'),
        ('CARDOVA', 'Cardova'),
        ('DOUBLE_ROOF_HARDTOP', 'Double Roof Hardtop'),
        ('SIENA_SCREEN_ROOM', 'Siena Screen Room'),
        ('APOLLO_ALUMINIUM', 'Apollo Aluminium'),
        ('ARLINGTON', 'Arlington'),
        ('CANOPY', 'Canopy'),
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
    gazebo_model = models.CharField(
        max_length=50, choices=GAZEBO_MODEL_CHOICES, blank=True, null=True)
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

    def get_total_price(self):
        """
        Calculates the total price of all items in the cart.
        """
        return sum(item.get_total_price() for item in self.items.all())

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
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type")
    )
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    service_option = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_("Quantity"), help_text=_("Number of this service option in the cart.")
    )

    def __str__(self):
        return f"{self.quantity} x {self.service_option.title} in {self.cart.user.username}'s cart"

    def get_total_price(self):
        """
        Calculates the total price for this cart item.
        """
        return self.service_option.get_total_price() * self.quantity

    class Meta:
        unique_together = [['cart', 'content_type', 'object_id']]
        ordering = ['cart']
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
