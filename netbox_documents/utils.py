

def file_upload(instance, filename):

    """
    Return a path for uploading image attchments.
    Adapted from netbox/extras/utils.py
    """
    path = 'netbox-documents/'

    if hasattr(instance, 'site'):
        path_prepend = instance.site.id
    if hasattr(instance, 'device'):
        path_prepend = instance.device.id
    if hasattr(instance, 'circuit'):
        path_prepend = instance.circuit.id

    # Rename the file to the provided name, if any. Attempt to preserve the file extension.
    extension = filename.rsplit('.')[-1].lower()
    if instance.name and extension in ['bmp', 'gif', 'jpeg', 'jpg', 'png', 'pdf', 'txt', 'doc', 'docx']:
        filename = '.'.join([instance.name, extension])
    elif instance.name:
        filename = instance.name

    return '{}{}_{}'.format(path, path_prepend, filename)
