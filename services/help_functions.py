def upload_to_service(instance, filename):
    from datetime import datetime
    import re
    
    date_path = datetime.now().strftime('%Y/%m/%d')
    category = re.sub(r'[^\w\-]', '_', str(instance.category.name))
    return f"services/{category}/{date_path}/{filename}"