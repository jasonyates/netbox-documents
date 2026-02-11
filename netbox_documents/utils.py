def file_upload(instance, filename):
    """
    Return a path for uploading file attachments.
    Uses the content_type and object_id from the GenericFK.
    """
    path = 'netbox-documents/'

    # Use object_id as the path prefix (works for any related model)
    path_prepend = instance.object_id

    # Rename the file to the provided name, if any. Attempt to preserve the file extension.
    extension = filename.rsplit('.')[-1].lower()
    if instance.name and extension in [
        'bmp', 'gif', 'jpeg', 'jpg', 'png', 'pdf', 'txt', 'doc', 'docx',
        'xls', 'xlsx', 'xlsm', 'tif', 'tiff', 'drawio', 'svg', 'webp',
        'html', 'pptx'
    ]:
        filename = '.'.join([instance.name, extension])
    elif instance.name:
        filename = instance.name

    return '{}{}_{}'.format(path, path_prepend, filename)
