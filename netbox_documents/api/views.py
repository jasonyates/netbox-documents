from netbox.api.viewsets import NetBoxModelViewSet
from .. import models, filtersets
from .serializers import DocumentSerializer


class DocumentViewSet(NetBoxModelViewSet):
    queryset = models.Document.objects.select_related('content_type').prefetch_related('tags')
    serializer_class = DocumentSerializer
    filterset_class = filtersets.DocumentFilterSet
