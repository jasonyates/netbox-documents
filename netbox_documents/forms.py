from django import forms
from django.contrib.contenttypes.models import ContentType
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import TagFilterField, CommentField, ContentTypeChoiceField
from .models import Document, DocTypeChoices, get_allowed_doc_types


class DocumentForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = Document
        fields = (
            'name', 'document', 'external_url', 'document_type',
            'comments', 'tags',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Determine content_type from existing instance (set by view's alter_object)
        content_type_id = None
        if self.instance and self.instance.content_type_id:
            content_type_id = self.instance.content_type_id

        allowed_values = get_allowed_doc_types(content_type_id)

        if allowed_values is not None:
            all_choices = list(DocTypeChoices.choices)
            filtered = [c for c in all_choices if c[0] in allowed_values]

            # Preserve the current value when editing an existing document
            if self.instance and self.instance.pk:
                current = self.instance.document_type
                if current and current not in allowed_values:
                    current_label = dict(all_choices).get(current, current)
                    filtered.append((current, current_label))

            self.fields['document_type'].choices = filtered


class DocumentFilterForm(NetBoxModelFilterSetForm):
    model = Document

    name = forms.CharField(required=False)

    document_type = forms.MultipleChoiceField(
        choices=DocTypeChoices,
        required=False,
    )

    content_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(),
        required=False,
        label='Object Type',
    )

    tag = TagFilterField(model)
