from netbox.search import SearchIndex
from .models import Document


class DocumentIndex(SearchIndex):
    model = Document
    fields = (
        ("name", 100),
        ("document", 500),
        ("comments", 5000),
    )


indexes = [DocumentIndex]
