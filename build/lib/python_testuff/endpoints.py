def build_endpoint(resource, resource_id=None):
    if resource_id:
        return f"{resource}/{resource_id}"
    return f"{resource}"
