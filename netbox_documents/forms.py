from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from dcim.models import Site, Device, DeviceType 
from circuits.models import Circuit
from utilities.forms import TagFilterField, CommentField, DynamicModelChoiceField
from .models import SiteDocument, DeviceDocument, DeviceTypeDocument, CircuitDocument, CircuitDocTypeChoices, SiteDocTypeChoices, DeviceDocTypeChoices, DeviceTypeDocTypeChoices 


#### Site Document Form & Filter Form
class SiteDocumentForm(NetBoxModelForm):
    comments = CommentField()

    site = DynamicModelChoiceField(
        queryset=Site.objects.all()
    )

    class Meta:
        model = SiteDocument
        fields = ('name', 'document', 'document_type', 'site', 'comments', 'tags')

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


#### Device Document Form & Filter Form
class DeviceDocumentForm(NetBoxModelForm):
    comments = CommentField()

    device = DynamicModelChoiceField(
        queryset=Device.objects.all()
    )

    class Meta:
        model = DeviceDocument
        fields = ('name', 'document', 'document_type', 'device', 'comments', 'tags')

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
        fields = ('name', 'document', 'document_type', 'device_type', 'comments', 'tags')

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
        fields = ('name', 'document', 'document_type', 'circuit', 'comments', 'tags')

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
