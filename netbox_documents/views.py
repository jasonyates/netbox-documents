from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from . import forms, models, tables, filtersets


class DocumentView(generic.ObjectView):
    queryset = models.Document.objects.select_related('content_type').all()


class DocumentListView(generic.ObjectListView):
    queryset = models.Document.objects.select_related('content_type').all()
    table = tables.DocumentTable
    filterset = filtersets.DocumentFilterSet
    filterset_form = forms.DocumentFilterForm
    actions = {
        'export': {'view'},
        'bulk_delete': {'delete'},
    }


class DocumentEditView(generic.ObjectEditView):
    queryset = models.Document.objects.all()
    form = forms.DocumentForm
    template_name = 'netbox_documents/document_edit.html'

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            content_type = request.GET.get('content_type')
            object_id = request.GET.get('object_id')
            if content_type and object_id:
                instance.content_type = get_object_or_404(ContentType, pk=content_type)
                instance.object_id = int(object_id)
        return instance


class DocumentDeleteView(generic.ObjectDeleteView):
    queryset = models.Document.objects.all()


class DocumentBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Document.objects.all()
    table = tables.DocumentTable
