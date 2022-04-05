from django.contrib.postgres.fields import ArrayField
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
        ('wirelessmodel', 'Wireless Model (Ekahau)', 'yellow'),
        ('quote', 'Quote', 'brown'),
        ('purchaseorder', 'Purchase Order', 'orange'),
    ]

class DeviceDocTypeChoices(ChoiceSet):

    key = 'DocTypeChoices.device'

    CHOICES = [
        ('diagram', 'Network Diagram', 'green'),
        ('supportcontract', 'Support Contract', 'blue'),
        ('quote', 'Quote', 'brown'),
        ('purchaseorder', 'Purchase Order', 'orange'),
    ]

class CircuitDocTypeChoices(ChoiceSet):
    
    key = 'DocTypeChoices.circuit'

    CHOICES = [
        ('diagram', 'Network Diagram', 'green'),
        ('quote', 'Quote', 'brown'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('circuitcontract', 'Circuit Contract', 'red'),
    ]

class SiteDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename will be used.'
    )
    document = models.FileField(
        upload_to=file_upload
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
        except tuple(expected_exceptions):
            return None

    @property
    def filename(self):
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:sitedocument', args=[self.pk])

class DeviceDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename will be used.'
    )

    document = models.FileField(
        upload_to=file_upload
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
        except tuple(expected_exceptions):
            return None

    @property
    def filename(self):
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]


    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:devicedocument', args=[self.pk])

class CircuitDocument(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename will be used.'
    )
    document = models.FileField(
        upload_to=file_upload
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
        except tuple(expected_exceptions):
            return None

    @property
    def filename(self):
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name
        filename = self.document.name.rsplit('/', 1)[-1]
        return filename.split('_', 1)[1]

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:circuitdocument', args=[self.pk])
