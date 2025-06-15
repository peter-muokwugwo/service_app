def upload_to_service(instance, filename):
    return f"services/{instance.category.name}/{filename}/%Y-%m-%d/"