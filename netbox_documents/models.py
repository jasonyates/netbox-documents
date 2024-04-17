from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from .utils import file_upload

class SiteDocTypeChoices(ChoiceSet):

    key = 'DocTypeChoices.site'

    CHOICES = [
        ('diagram', 'Network Diagram', 'green'),
        ('floorplan', 'Floor Plan', 'purple'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('quote', 'Quote', 'indigo'),
        ('wirelessmodel', 'Wireless Model (Ekahau)', 'yellow'),
        ('other', 'Other', 'gray'),
    ]

class LocationDocTypeChoices(ChoiceSet):

    key = 'DocTypeChoices.location'

    CHOICES = [
        ('diagram', 'Network Diagram', 'green'),
        ('floorplan', 'Floor Plan', 'purple'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('quote', 'Quote', 'indigo'),
        ('wirelessmodel', 'Wireless Model (Ekahau)', 'yellow'),
        ('other', 'Other', 'gray'),
    ]

class DeviceDocTypeChoices(ChoiceSet):

    key = 'DocTypeChoices.device'

    CHOICES = [
        ('diagram', 'Network Diagram', 'green'),
        ('manual', 'Manual', 'pink'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('quote', 'Quote', 'indigo'),
        ('supportcontract', 'Support Contract', 'blue'),
        ('other', 'Other', 'gray'),
    ]


class DeviceTypeDocTypeChoices(ChoiceSet):

    key = 'DocTypeChoices.devicetype'

    CHOICES = [
        ('diagram', 'Network Diagram', 'green'),
        ('manual', 'Manual', 'pink'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('quote', 'Quote', 'indigo'),
        ('supportcontract', 'Support Contract', 'blue'),
        ('other', 'Other', 'gray'),
    ]

class CircuitDocTypeChoices(ChoiceSet):
    
    key = 'DocTypeChoices.circuit'

    CHOICES = [
        ('circuitcontract', 'Circuit Contract', 'red'),
        ('diagram', 'Network Diagram', 'green'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('quote', 'Quote', 'indigo'),
        ('kmz', 'KMZ', 'blue'),
        ('other', 'Other', 'gray'),
    ]

class CircuitProviderDocTypeChoices(ChoiceSet):
    
    key = 'DocTypeChoices.circuitprovider'

    CHOICES = [
        ('contract', 'Contract', 'red'),
        ('msa', 'MSA', 'green'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('quote', 'Quote', 'indigo'),
        ('other', 'Other', 'gray'),
    ]


class VMDocTypeChoices(ChoiceSet):

    key = 'DocTypeChoices.virtualmachine'

    CHOICES = [
        ('diagram', 'Network Diagram', 'green'),
        ('manual', 'Manual', 'pink'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('quote', 'Quote', 'indigo'),
        ('supportcontract', 'Support Contract', 'blue'),
        ('other', 'Other', 'gray'),
    ]

class SiteDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename or url will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )

    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=SiteDocTypeChoices
    )

    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('-created', 'name')
        verbose_name_plural = "Site Documents"
        verbose_name = "Site Document"

    def get_document_type_color(self):
        return SiteDocTypeChoices.colors.get(self.document_type)

    @property
    def size(self):
        """
        Wrapper around `document.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
        catch other exceptions that we know other storage back-ends to throw.
        """
        expected_exceptions = [OSError]

        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass

        try:
            return self.document.size
        except:
            return None

    @property
    def filename(self):
        if self.external_url:
            return self.external_url
        elif self.document:
            filename = self.document.name.rsplit('/', 1)[-1]
            return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name

        elif self.external_url:
            return self.external_url

        elif self.document:
            filename = self.document.name.rsplit('/', 1)[-1]
            return filename.split('_', 1)[1]

        else:
            return ""

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:sitedocument', args=[self.pk])

    def clean(self):
        super().clean()

        # Must have an uploaded document or an external URL. cannot have both
        if not self.document and self.external_url == '':
            raise ValidationError("A document must contain an uploaded file or an external URL.")
        if self.document and self.external_url:
            raise ValidationError("A document cannot contain both an uploaded file and an external URL.")

    def delete(self, *args, **kwargs):

        # Check if its a document or a URL
        if self.external_url == '':

            _name = self.document.name

            # Delete file from disk
            super().delete(*args, **kwargs)
            self.document.delete(save=False)

            # Restore the name of the document as it's re-used in the notifications later
            self.document.name = _name
        else:
            # Straight delete of external URL
            super().delete(*args, **kwargs)


class LocationDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename or url will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )

    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=LocationDocTypeChoices
    )

    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.CASCADE,
        related_name='document'
    )

    location = models.ForeignKey(
        to='dcim.Location',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('-created', 'name')
        verbose_name_plural = "Location Documents"
        verbose_name = "Location Document"

    def get_document_type_color(self):
        return LocationDocTypeChoices.colors.get(self.document_type)

    @property
    def size(self):
        """
        Wrapper around `document.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
        catch other exceptions that we know other storage back-ends to throw.
        """
        expected_exceptions = [OSError]

        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass

        try:
            return self.document.size
        except:
            return None

    @property
    def filename(self):
        if self.external_url:
            return self.external_url
        elif self.document:
            filename = self.document.name.rsplit('/', 1)[-1]
            return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name

        elif self.external_url:
            return self.external_url

        elif self.document:
            filename = self.document.name.rsplit('/', 1)[-1]
            return filename.split('_', 1)[1]

        else:
            return ""

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:locationdocument', args=[self.pk])

    def clean(self):
        super().clean()

        # Must have an uploaded document or an external URL. cannot have both
        if not self.document and self.external_url == '':
            raise ValidationError("A document must contain an uploaded file or an external URL.")
        if self.document and self.external_url:
            raise ValidationError("A document cannot contain both an uploaded file and an external URL.")
        if self.location.site != self.site:
            raise ValidationError("Location must belong to Site.")

    def delete(self, *args, **kwargs):

        # Check if its a document or a URL
        if self.external_url == '':

            _name = self.document.name

            # Delete file from disk
            super().delete(*args, **kwargs)
            self.document.delete(save=False)

            # Restore the name of the document as it's re-used in the notifications later
            self.document.name = _name
        else:
            # Straight delete of external URL
            super().delete(*args, **kwargs)


class DeviceDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )

    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=DeviceDocTypeChoices
    )

    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Device Documents"
        verbose_name = "Device Document"

    def get_document_type_color(self):
        return DeviceDocTypeChoices.colors.get(self.document_type)

    @property
    def size(self):
        """
        Wrapper around `document.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
        catch other exceptions that we know other storage back-ends to throw.
        """
        expected_exceptions = [OSError]

        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass

        try:
            return self.document.size
        except:
            return None

    @property
    def filename(self):
        if self.external_url:
            return self.external_url
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name

        if self.external_url:
            return self.external_url

        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:devicedocument', args=[self.pk])

    def clean(self):
        super().clean()

        # Must have an uploaded document or an external URL. cannot have both
        if not self.document and self.external_url == '':
            raise ValidationError("A document must contain an uploaded file or an external URL.")
        if self.document and self.external_url:
            raise ValidationError("A document cannot contain both an uploaded file and an external URL.")

    def delete(self, *args, **kwargs):

        # Check if its a document or a URL
        if self.external_url == '':

            _name = self.document.name

            # Delete file from disk
            super().delete(*args, **kwargs)
            self.document.delete(save=False)

            # Restore the name of the document as it's re-used in the notifications later
            self.document.name = _name
        else:
            # Straight delete of external URL
            super().delete(*args, **kwargs)



class DeviceTypeDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )
    
    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=DeviceTypeDocTypeChoices
    )

    device_type = models.ForeignKey(
        to='dcim.DeviceType',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Device Type Documents"
        verbose_name = "Device Type Document"

    def get_document_type_color(self):
        return DeviceTypeDocTypeChoices.colors.get(self.document_type)

    @property
    def size(self):
        """
        Wrapper around `document.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
        catch other exceptions that we know other storage back-ends to throw.
        """
        expected_exceptions = [OSError]

        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass

        try:
            return self.document.size
        except:
            return None

    @property
    def filename(self):
        if self.external_url:
            return self.external_url
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name

        if self.external_url:
            return self.external_url

        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:devicetypedocument', args=[self.pk])

    def clean(self):
        super().clean()

        # Must have an uploaded document or an external URL. cannot have both
        if not self.document and self.external_url == '':
            raise ValidationError("A document must contain an uploaded file or an external URL.")
        if self.document and self.external_url:
            raise ValidationError("A document cannot contain both an uploaded file and an external URL.")

    def delete(self, *args, **kwargs):

        # Check if its a document or a URL
        if self.external_url == '':

            _name = self.document.name

            # Delete file from disk
            super().delete(*args, **kwargs)
            self.document.delete(save=False)

            # Restore the name of the document as it's re-used in the notifications later
            self.document.name = _name
        else:
            # Straight delete of external URL
            super().delete(*args, **kwargs)


class CircuitDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )

    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=CircuitDocTypeChoices
    )

    circuit = models.ForeignKey(
        to='circuits.Circuit',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    comments = models.TextField(
        blank=True
    )

    def get_document_type_color(self):
        return CircuitDocTypeChoices.colors.get(self.document_type)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Circuit Documents"
        verbose_name = "Circuit Document"

    @property
    def size(self):
        """
        Wrapper around `document.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
        catch other exceptions that we know other storage back-ends to throw.
        """
        expected_exceptions = [OSError]

        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass

        try:
            return self.document.size
        except:
            return None

    @property
    def filename(self):
        if self.external_url:
            return self.external_url
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name

        if self.external_url:
            return self.external_url

        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:circuitdocument', args=[self.pk])

    def clean(self):
        super().clean()

        # Must have an uploaded document or an external URL. cannot have both
        if not self.document and self.external_url == '':
            raise ValidationError("A document must contain an uploaded file or an external URL.")
        if self.document and self.external_url:
            raise ValidationError("A document cannot contain both an uploaded file and an external URL.")

    def delete(self, *args, **kwargs):

        # Check if its a document or a URL
        if self.external_url == '':

            _name = self.document.name

            # Delete file from disk
            super().delete(*args, **kwargs)
            self.document.delete(save=False)

            # Restore the name of the document as it's re-used in the notifications later
            self.document.name = _name
        else:
            # Straight delete of external URL
            super().delete(*args, **kwargs)


class VMDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )

    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=VMDocTypeChoices
    )

    vm = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Virtual Machine Documents"
        verbose_name = "Virtual Machine Document"

    def get_document_type_color(self):
        return VMDocTypeChoices.colors.get(self.document_type)

    @property
    def size(self):
        """
        Wrapper around `document.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
        catch other exceptions that we know other storage back-ends to throw.
        """
        expected_exceptions = [OSError]

        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass

        try:
            return self.document.size
        except:
            return None

    @property
    def filename(self):
        if self.external_url:
            return self.external_url
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name

        if self.external_url:
            return self.external_url

        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:vmdocument', args=[self.pk])

    def clean(self):
        super().clean()

        # Must have an uploaded document or an external URL. cannot have both
        if not self.document and self.external_url == '':
            raise ValidationError("A document must contain an uploaded file or an external URL.")
        if self.document and self.external_url:
            raise ValidationError("A document cannot contain both an uploaded file and an external URL.")

    def delete(self, *args, **kwargs):

        # Check if its a document or a URL
        if self.external_url == '':

            _name = self.document.name

            # Delete file from disk
            super().delete(*args, **kwargs)
            self.document.delete(save=False)

            # Restore the name of the document as it's re-used in the notifications later
            self.document.name = _name
        else:
            # Straight delete of external URL
            super().delete(*args, **kwargs)

class CircuitProviderDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )

    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=CircuitProviderDocTypeChoices
    )

    provider = models.ForeignKey(
        to='circuits.Provider',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    comments = models.TextField(
        blank=True
    )

    def get_document_type_color(self):
        return CircuitProviderDocTypeChoices.colors.get(self.document_type)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Circuit Provider Documents"
        verbose_name = "Circuit Provider Document"

    @property
    def size(self):
        """
        Wrapper around `document.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
        catch other exceptions that we know other storage back-ends to throw.
        """
        expected_exceptions = [OSError]

        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass

        try:
            return self.document.size
        except:
            return None

    @property
    def filename(self):
        if self.external_url:
            return self.external_url
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name

        if self.external_url:
            return self.external_url

        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:circuitproviderdocument', args=[self.pk])

    def clean(self):
        super().clean()

        # Must have an uploaded document or an external URL. cannot have both
        if not self.document and self.external_url == '':
            raise ValidationError("A document must contain an uploaded file or an external URL.")
        if self.document and self.external_url:
            raise ValidationError("A document cannot contain both an uploaded file and an external URL.")

    def delete(self, *args, **kwargs):

        # Check if its a document or a URL
        if self.external_url == '':

            _name = self.document.name

            # Delete file from disk
            super().delete(*args, **kwargs)
            self.document.delete(save=False)

            # Restore the name of the document as it's re-used in the notifications later
            self.document.name = _name
        else:
            # Straight delete of external URL
            super().delete(*args, **kwargs)