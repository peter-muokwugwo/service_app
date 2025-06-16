from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models

# Register your models here.
admin.sites.site.site_header = "Fixitek Services"


@admin.register(models.ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name', 'description')


@admin.register(models.TVMountingOption)
class TVMountingOptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'needs',
                    'bracket', 'wall_type', 'quantity', 'price', 'needs_moving_help', 'moving_help_charge']
    list_filter = ['needs', 'bracket', 'wall_type', 'price']
    search_fields = ['title']


@admin.register(models.FurnitureAssemblyOption)
class FurnitureAssemblyOptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'location',
                    'needs_moving_help', 'quantity', 'price']
    list_filter = ['location', 'service_type', 'needs_moving_help']
    search_fields = ['title', 'service_type']


@admin.register(models.InstallationServiceOption)
class InstallationServiceOptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'installation_type',
                    'location', 'power_nearby', 'quantity', 'price']
    list_filter = ['installation_type', 'location', 'power_nearby']
    search_fields = ['title', 'installation_type']


@admin.register(models.GazeboServiceOption)
class GazeboServiceOptionAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'gazebo_model', 'size', 'quantity', 'price', 'needs_moving_help', 'anchoring',
                    'related_image', 'moving_help_charge']
    list_filter = ['gazebo_model', 'size']
    search_fields = ['title', 'gazebo_model']


@admin.register(models.GazeboModel)
class GazeboModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'description')
    search_fields = ('name', 'description')


@admin.register(models.InstallationType)
class InstallationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'description')
    search_fields = ('name', 'description')


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(models.ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(models.AssemblyType)
class AssemblyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
