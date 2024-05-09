from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from dcim.models import Site, Location, Device, DeviceType
from virtualization.models import VirtualMachine
from circuits.models import Circuit, Provider
from utilities.forms.fields import TagFilterField, CommentField, DynamicModelChoiceField
from .models import SiteDocument, LocationDocument, DeviceDocument, DeviceTypeDocument, CircuitDocument, CircuitDocTypeChoices, SiteDocTypeChoices, LocationDocTypeChoices, DeviceDocTypeChoices, DeviceTypeDocTypeChoices, VMDocument, VMDocTypeChoices, CircuitProviderDocument, CircuitProviderDocTypeChoices 


#### Site Document Form & Filter Form
class SiteDocumentForm(NetBoxModelForm):
    comments = CommentField()

    site = DynamicModelChoiceField(
        queryset=Site.objects.all()
    )

    class Meta:
        model = SiteDocument
        fields = ('name', 'document', 'external_url', 'document_type', 'site', 'comments', 'tags')

class SiteDocumentFilterForm(NetBoxModelFilterSetForm):
    model = SiteDocument

    name = forms.CharField(
        required=False
    )

    site = forms.ModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False
    )

    document_type = forms.MultipleChoiceField(
        choices=SiteDocTypeChoices,
        required=False
    )

    tag = TagFilterField(model)


#### Location Document Form & Filter Form
class LocationDocumentForm(NetBoxModelForm):
    comments = CommentField()

    site = DynamicModelChoiceField(
        queryset=Site.objects.all()
    )

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        query_params={
            'site_id': '$site'
        }
    )

    class Meta:
        model = LocationDocument
        fields = ('name', 'document', 'external_url', 'document_type', 'site', 'location', 'comments', 'tags')

class LocationDocumentFilterForm(NetBoxModelFilterSetForm):
    model = LocationDocument

    name = forms.CharField(
        required=False
    )

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        query_params={
            'site_id': '$site'
        },
        required=False
    )

    document_type = forms.MultipleChoiceField(
        choices=LocationDocTypeChoices,
        required=False
    )

    tag = TagFilterField(model)


#### Device Document Form & Filter Form
class DeviceDocumentForm(NetBoxModelForm):
    comments = CommentField()

    device = DynamicModelChoiceField(
        queryset=Device.objects.all()
    )

    class Meta:
        model = DeviceDocument
        fields = ('name', 'document', 'external_url', 'document_type', 'device', 'comments', 'tags')

class DeviceDocumentFilterForm(NetBoxModelFilterSetForm):
    model = DeviceDocument

    name = forms.CharField(
        required=False
    )

    device = forms.ModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False
    )

    document_type = forms.MultipleChoiceField(
        choices=DeviceDocTypeChoices,
        required=False
    )

    tag = TagFilterField(model)


#### Device Type Document Form & Filter Form
class DeviceTypeDocumentForm(NetBoxModelForm):
    comments = CommentField()

    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all()
    )

    class Meta:
        model = DeviceTypeDocument
        fields = ('name', 'document', 'external_url', 'document_type', 'device_type', 'comments', 'tags')

class DeviceTypeDocumentFilterForm(NetBoxModelFilterSetForm):
    model = DeviceTypeDocument

    name = forms.CharField(
        required=False
    )

    device = forms.ModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False
    )

    document_type = forms.MultipleChoiceField(
        choices=DeviceTypeDocTypeChoices,
        required=False
    )

    tag = TagFilterField(model)


#### Circuit Document Form & Filter Form
class CircuitDocumentForm(NetBoxModelForm):
    comments = CommentField()

    circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all()
    )

    class Meta:
        model = CircuitDocument
        fields = ('name', 'document', 'external_url', 'document_type', 'circuit', 'comments', 'tags')

class CircuitDocumentFilterForm(NetBoxModelFilterSetForm):
    model = CircuitDocument

    name = forms.CharField(
        required=False
    )

    circuit = forms.ModelMultipleChoiceField(
        queryset=Circuit.objects.all(),
        required=False
    )

    document_type = forms.MultipleChoiceField(
        choices=CircuitDocTypeChoices,
        required=False
    )

    tag = TagFilterField(model)

#### VM Document Form & Filter Form
class VMDocumentForm(NetBoxModelForm):
    comments = CommentField()

    vm = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all()
    )

    class Meta:
        model = VMDocument
        fields = ('name', 'document', 'external_url', 'document_type', 'vm', 'comments', 'tags')

class VMDocumentFilterForm(NetBoxModelFilterSetForm):
    model = VMDocument

    name = forms.CharField(
        required=False
    )

    vm = forms.ModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False
    )

    document_type = forms.MultipleChoiceField(
        choices=VMDocTypeChoices,
        required=False
    )

    tag = TagFilterField(model)

#### Circuit Provider Document Form & Filter Form
class CircuitProviderDocumentForm(NetBoxModelForm):
    comments = CommentField()

    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all()
    )

    class Meta:
        model = CircuitProviderDocument
        fields = ('name', 'document', 'external_url', 'document_type', 'provider', 'comments', 'tags')

class CircuitProviderDocumentFilterForm(NetBoxModelFilterSetForm):
    model = CircuitProviderDocument

    name = forms.CharField(
        required=False
    )

    provider = forms.ModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        required=False
    )

    document_type = forms.MultipleChoiceField(
        choices=CircuitProviderDocTypeChoices,
        required=False
    )

    tag = TagFilterField(model)