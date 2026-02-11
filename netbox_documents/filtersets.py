from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models import Document


class DocumentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Document
        fields = ('id', 'name', 'document_type', 'content_type', 'object_id')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(document__icontains=value)
        )
