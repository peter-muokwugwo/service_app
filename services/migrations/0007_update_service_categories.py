from django.db import migrations

def create_and_assign_service_categories(apps, schema_editor):
    ServiceCategory = apps.get_model('services', 'ServiceCategory')
    FurnitureAssemblyOption = apps.get_model('services', 'FurnitureAssemblyOption')
    GazeboServiceOption = apps.get_model('services', 'GazeboServiceOption')
    InstallationServiceOption = apps.get_model('services', 'InstallationServiceOption')
    TVMountingOption = apps.get_model('services', 'TVMountingOption')
    # Add other service option models as needed

    # Define the 7 categories
    categories = [
        'Indoor Furniture Assembly',
        'Outdoor & Patio Assembly',
        'Gazebos & Pergolas',
        'Fitness & Recreation Equipment',
        'Home Installations & Security',
        'Appliances, Plumbing & Maintenance',
        'Child & Baby Safety',
    ]
    category_objs = {}
    for name in categories:
        obj, _ = ServiceCategory.objects.get_or_create(name=name)
        category_objs[name] = obj

    # Example assignments (customize as needed for your data)
    FurnitureAssemblyOption.objects.update(category=category_objs['Indoor Furniture Assembly'])
    GazeboServiceOption.objects.update(category=category_objs['Gazebos & Pergolas'])
    # Add more assignments for other models as needed

class Migration(migrations.Migration):
    dependencies = [
        ('services', '0006_installationtype_and_more'),
    ]
    operations = [
        migrations.RunPython(create_and_assign_service_categories),
    ]
