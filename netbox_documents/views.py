from netbox.views import generic
from . import forms, models, tables, filtersets


### SiteDocument
class SiteDocumentView(generic.ObjectView):
    queryset = models.SiteDocument.objects.all()

class SiteDocumentListView(generic.ObjectListView):
    queryset = models.SiteDocument.objects.all()
    table = tables.SiteDocumentTable
    filterset = filtersets.SiteDocumentFilterSet
    filterset_form = forms.SiteDocumentFilterForm

class SiteDocumentEditView(generic.ObjectEditView):
    queryset = models.SiteDocument.objects.all()
    form = forms.SiteDocumentForm

class SiteDocumentDeleteView(generic.ObjectDeleteView):
    queryset = models.SiteDocument.objects.all()

### DeviceDocument
class DeviceDocumentView(generic.ObjectView):
    queryset = models.DeviceDocument.objects.all()

class DeviceDocumentListView(generic.ObjectListView):
    queryset = models.DeviceDocument.objects.all()
    table = tables.DeviceDocumentTable
    filterset = filtersets.DeviceDocumentFilterSet
    filterset_form = forms.DeviceDocumentFilterForm

class DeviceDocumentEditView(generic.ObjectEditView):
    queryset = models.DeviceDocument.objects.all()
    form = forms.DeviceDocumentForm

class DeviceDocumentDeleteView(generic.ObjectDeleteView):
    queryset = models.DeviceDocument.objects.all()

### CircuitDocument
class CircuitDocumentView(generic.ObjectView):
    queryset = models.CircuitDocument.objects.all()

class CircuitDocumentListView(generic.ObjectListView):
    queryset = models.CircuitDocument.objects.all()
    table = tables.CircuitDocumentTable
    filterset = filtersets.CircuitDocumentFilterSet
    filterset_form = forms.CircuitDocumentFilterForm

class CircuitDocumentEditView(generic.ObjectEditView):
    queryset = models.CircuitDocument.objects.all()
    form = forms.CircuitDocumentForm

class CircuitDocumentDeleteView(generic.ObjectDeleteView):
    queryset = models.CircuitDocument.objects.all()