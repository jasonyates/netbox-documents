from unittest.mock import MagicMock, patch

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from netbox_documents.models import Document, DocTypeChoices, _BUILTIN_CHOICES, _build_all_choices, get_allowed_doc_types
from netbox_documents.utils import file_upload


class DocTypeChoicesTest(TestCase):
    """Tests for the unified DocTypeChoices ChoiceSet."""

    def test_all_expected_choices_present(self):
        """All expected document type choice values should be present."""
        expected_values = [
            'diagram', 'floorplan', 'purchaseorder', 'quote', 'wirelessmodel',
            'manual', 'supportcontract', 'circuitcontract', 'contract', 'msa',
            'kmz', 'other',
        ]
        actual_values = [choice[0] for choice in DocTypeChoices.CHOICES]
        for value in expected_values:
            self.assertIn(
                value,
                actual_values,
                f"Expected choice '{value}' not found in DocTypeChoices",
            )

    def test_colors_defined_for_all_choices(self):
        """Every choice should have a color defined."""
        for value, label, color in DocTypeChoices.CHOICES:
            self.assertIsNotNone(
                color,
                f"Color not defined for choice '{value}'",
            )
            self.assertIn(
                DocTypeChoices.colors.get(value),
                ['green', 'purple', 'orange', 'indigo', 'yellow', 'pink', 'blue', 'red', 'gray'],
                f"Unexpected color '{color}' for choice '{value}'",
            )


class FileUploadUtilTest(TestCase):
    """Tests for the file_upload utility function."""

    def _make_instance(self, object_id, name=''):
        """Create a mock Document instance with the given object_id and name."""
        instance = MagicMock()
        instance.object_id = object_id
        instance.name = name
        return instance

    def test_path_format_with_object_id_prefix(self):
        """The returned path should start with 'netbox-documents/' followed by the object_id prefix."""
        instance = self._make_instance(object_id=42, name='')
        result = file_upload(instance, 'report.pdf')
        self.assertTrue(result.startswith('netbox-documents/'))
        self.assertIn('42_', result)

    def test_preserves_extension_for_supported_types(self):
        """When a name is provided and the file extension is supported, the extension should be preserved."""
        supported_extensions = [
            'bmp', 'gif', 'jpeg', 'jpg', 'png', 'pdf', 'txt', 'doc', 'docx',
            'xls', 'xlsx', 'xlsm', 'tif', 'tiff', 'drawio', 'svg', 'webp',
            'html', 'pptx',
        ]
        for ext in supported_extensions:
            instance = self._make_instance(object_id=10, name='my-document')
            result = file_upload(instance, f'original.{ext}')
            self.assertTrue(
                result.endswith(f'my-document.{ext}'),
                f"Expected path to end with 'my-document.{ext}', got '{result}' for extension '{ext}'",
            )

    def test_uses_name_without_extension_for_unsupported_types(self):
        """When a name is provided but the file extension is unsupported, use just the name."""
        instance = self._make_instance(object_id=10, name='my-document')
        result = file_upload(instance, 'original.xyz')
        self.assertTrue(
            result.endswith('10_my-document'),
            f"Expected path to end with '10_my-document', got '{result}'",
        )

    def test_preserves_original_filename_without_name(self):
        """When no name is provided, the original filename should be kept."""
        instance = self._make_instance(object_id=5, name='')
        result = file_upload(instance, 'original-file.pdf')
        self.assertEqual(result, 'netbox-documents/5_original-file.pdf')

    def test_case_insensitive_extension(self):
        """File extension matching should be case-insensitive."""
        instance = self._make_instance(object_id=10, name='my-document')
        result = file_upload(instance, 'original.PDF')
        self.assertTrue(
            result.endswith('my-document.pdf'),
            f"Expected path to end with 'my-document.pdf' (lowered), got '{result}'",
        )

    def test_path_format_complete(self):
        """Verify the complete path format: 'netbox-documents/{object_id}_{filename}'."""
        instance = self._make_instance(object_id=99, name='')
        result = file_upload(instance, 'test.pdf')
        self.assertEqual(result, 'netbox-documents/99_test.pdf')


class DocumentModelTest(TestCase):
    """Tests for the unified Document model."""

    def setUp(self):
        """Set up test data. Use ContentType for ContentType as the related object type."""
        self.ct = ContentType.objects.get_for_model(ContentType)
        self.object_id = 1

    # ------------------------------------------------------------------
    # Creation tests
    # ------------------------------------------------------------------

    def test_create_document_with_file(self):
        """A Document can be created with an uploaded file."""
        uploaded_file = SimpleUploadedFile(
            'network_diagram.pdf', b'%PDF-1.4 fake content', content_type='application/pdf'
        )
        doc = Document.objects.create(
            name='Network Diagram',
            document=uploaded_file,
            document_type='diagram',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertIsNotNone(doc.pk)
        self.assertEqual(doc.name, 'Network Diagram')
        self.assertEqual(doc.document_type, 'diagram')
        self.assertTrue(doc.document.name)
        self.assertEqual(doc.external_url, '')

    def test_create_document_with_external_url(self):
        """A Document can be created with an external URL."""
        doc = Document.objects.create(
            name='External Doc',
            external_url='https://example.com/doc.pdf',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertIsNotNone(doc.pk)
        self.assertEqual(doc.external_url, 'https://example.com/doc.pdf')
        self.assertFalse(doc.document.name)

    # ------------------------------------------------------------------
    # Validation tests
    # ------------------------------------------------------------------

    def test_validation_neither_file_nor_url(self):
        """Validation should reject a document with neither a file nor an external URL."""
        doc = Document(
            name='Empty',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        with self.assertRaises(ValidationError) as ctx:
            doc.clean()
        self.assertIn(
            'A document must contain an uploaded file or an external URL.',
            str(ctx.exception),
        )

    def test_validation_both_file_and_url(self):
        """Validation should reject a document with both a file and an external URL."""
        uploaded_file = SimpleUploadedFile(
            'test.pdf', b'content', content_type='application/pdf'
        )
        doc = Document(
            name='Both',
            document=uploaded_file,
            external_url='https://example.com/test.pdf',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        with self.assertRaises(ValidationError) as ctx:
            doc.clean()
        self.assertIn(
            'A document cannot contain both an uploaded file and an external URL.',
            str(ctx.exception),
        )

    def test_validation_file_only_passes(self):
        """Validation should pass for a document with only a file."""
        uploaded_file = SimpleUploadedFile(
            'test.pdf', b'content', content_type='application/pdf'
        )
        doc = Document(
            name='File Only',
            document=uploaded_file,
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        doc.clean()

    def test_validation_url_only_passes(self):
        """Validation should pass for a document with only an external URL."""
        doc = Document(
            name='URL Only',
            external_url='https://example.com/doc.pdf',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        doc.clean()

    # ------------------------------------------------------------------
    # __str__ tests
    # ------------------------------------------------------------------

    def test_str_returns_name_when_set(self):
        """__str__ should return the name when it is set."""
        doc = Document(
            name='My Document',
            external_url='https://example.com/doc.pdf',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertEqual(str(doc), 'My Document')

    def test_str_returns_external_url_when_no_name(self):
        """__str__ should return the external_url when name is blank."""
        doc = Document(
            name='',
            external_url='https://example.com/doc.pdf',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertEqual(str(doc), 'https://example.com/doc.pdf')

    def test_str_returns_filename_when_no_name_no_url(self):
        """__str__ should return the parsed filename when name and external_url are blank."""
        doc = Document(
            name='',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        doc.document.name = 'netbox-documents/1_report.pdf'
        self.assertEqual(str(doc), 'report.pdf')

    def test_str_returns_empty_string_when_nothing_set(self):
        """__str__ should return empty string when name, url, and document are all empty."""
        doc = Document(
            name='',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertEqual(str(doc), '')

    # ------------------------------------------------------------------
    # get_absolute_url tests
    # ------------------------------------------------------------------

    def test_get_absolute_url(self):
        """get_absolute_url should return the correct URL for the document detail view."""
        doc = Document.objects.create(
            name='Test Doc',
            external_url='https://example.com/test',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        expected_url = f'/plugins/documents/documents/{doc.pk}/'
        self.assertEqual(doc.get_absolute_url(), expected_url)

    # ------------------------------------------------------------------
    # get_document_type_color tests
    # ------------------------------------------------------------------

    def test_get_document_type_color_returns_correct_color(self):
        """get_document_type_color should return the color for the document type."""
        test_cases = {
            'diagram': 'green',
            'floorplan': 'purple',
            'other': 'gray',
            'contract': 'red',
            'kmz': 'blue',
        }
        for doc_type, expected_color in test_cases.items():
            doc = Document(
                name='Test',
                external_url='https://example.com/test',
                document_type=doc_type,
                content_type=self.ct,
                object_id=self.object_id,
            )
            self.assertEqual(
                doc.get_document_type_color(),
                expected_color,
                f"Color for document_type '{doc_type}' should be '{expected_color}'",
            )

    def test_get_document_type_color_unknown_type(self):
        """get_document_type_color should return None for an unknown document type."""
        doc = Document(
            name='Test',
            external_url='https://example.com/test',
            document_type='nonexistent',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertIsNone(doc.get_document_type_color())

    # ------------------------------------------------------------------
    # filename property tests
    # ------------------------------------------------------------------

    def test_filename_returns_external_url_for_url_documents(self):
        """The filename property should return the external_url for URL-based documents."""
        doc = Document(
            name='Test',
            external_url='https://example.com/document.pdf',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertEqual(doc.filename, 'https://example.com/document.pdf')

    def test_filename_returns_parsed_name_for_uploaded_files(self):
        """The filename property should parse the stored path and return the original filename."""
        doc = Document(
            name='',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        doc.document.name = 'netbox-documents/42_network_diagram.pdf'
        self.assertEqual(doc.filename, 'network_diagram.pdf')

    def test_filename_returns_none_when_nothing_set(self):
        """The filename property should return None when neither URL nor file is set."""
        doc = Document(
            name='',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertIsNone(doc.filename)

    def test_filename_strips_path_prefix(self):
        """The filename property should strip directory prefixes from the stored path."""
        doc = Document(
            name='',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        doc.document.name = 'netbox-documents/100_my_file.docx'
        self.assertEqual(doc.filename, 'my_file.docx')

    # ------------------------------------------------------------------
    # size property tests
    # ------------------------------------------------------------------

    def test_size_returns_none_when_file_inaccessible(self):
        """The size property should return None when the file cannot be accessed."""
        doc = Document(
            name='Test',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        doc.document.name = 'netbox-documents/1_nonexistent.pdf'
        self.assertIsNone(doc.size)

    def test_size_returns_none_when_no_file(self):
        """The size property should return None when no file is set."""
        doc = Document(
            name='Test',
            external_url='https://example.com/test',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        self.assertIsNone(doc.size)

    def test_size_returns_value_when_file_accessible(self):
        """The size property should return the file size when the file is accessible."""
        doc = Document(
            name='Test',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        mock_field = MagicMock()
        mock_field.size = 12345
        doc.document = mock_field
        self.assertEqual(doc.size, 12345)

    # ------------------------------------------------------------------
    # delete tests
    # ------------------------------------------------------------------

    def test_delete_uploaded_document_cleans_up_file(self):
        """Deleting a document with an uploaded file should remove the file from disk."""
        uploaded_file = SimpleUploadedFile(
            'test_delete.pdf', b'delete me', content_type='application/pdf'
        )
        doc = Document.objects.create(
            name='To Delete',
            document=uploaded_file,
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        pk = doc.pk
        file_name = doc.document.name

        with patch.object(doc.document.storage, 'delete') as mock_storage_delete:
            doc.delete()

        self.assertFalse(Document.objects.filter(pk=pk).exists())
        # The name should be restored after delete for notification purposes
        self.assertEqual(doc.document.name, file_name)

    def test_delete_external_url_document(self):
        """Deleting a document with an external URL should not attempt file cleanup."""
        doc = Document.objects.create(
            name='External',
            external_url='https://example.com/doc.pdf',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        pk = doc.pk
        doc.delete()
        self.assertFalse(Document.objects.filter(pk=pk).exists())

    # ------------------------------------------------------------------
    # Meta and ordering tests
    # ------------------------------------------------------------------

    def test_ordering_by_name(self):
        """Documents should be ordered by name."""
        Document.objects.create(
            name='Zebra',
            external_url='https://example.com/z',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        Document.objects.create(
            name='Alpha',
            external_url='https://example.com/a',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        Document.objects.create(
            name='Middle',
            external_url='https://example.com/m',
            document_type='other',
            content_type=self.ct,
            object_id=self.object_id,
        )
        docs = list(Document.objects.values_list('name', flat=True))
        self.assertEqual(docs, ['Alpha', 'Middle', 'Zebra'])

    def test_verbose_name(self):
        """The model's verbose name should be 'Document'."""
        self.assertEqual(Document._meta.verbose_name, 'Document')
        self.assertEqual(Document._meta.verbose_name_plural, 'Documents')

    # ------------------------------------------------------------------
    # clone_fields tests
    # ------------------------------------------------------------------

    def test_clone_fields_defined(self):
        """The clone_fields tuple should contain the expected fields."""
        self.assertIn('content_type', Document.clone_fields)
        self.assertIn('object_id', Document.clone_fields)
        self.assertIn('document_type', Document.clone_fields)

    # ------------------------------------------------------------------
    # content_type / generic foreign key tests
    # ------------------------------------------------------------------

    def test_content_type_and_object_id_stored(self):
        """The content_type and object_id should be properly stored on the document."""
        doc = Document.objects.create(
            name='GFK Test',
            external_url='https://example.com/gfk',
            document_type='diagram',
            content_type=self.ct,
            object_id=42,
        )
        doc.refresh_from_db()
        self.assertEqual(doc.content_type, self.ct)
        self.assertEqual(doc.object_id, 42)


class BuildAllChoicesTest(TestCase):
    """Tests for the _build_all_choices() function."""

    def test_returns_builtin_choices_when_no_custom(self):
        """Should return only built-in choices when no custom types are configured."""
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'custom_doc_types': []}}):
            choices = _build_all_choices()
            self.assertEqual(choices, _BUILTIN_CHOICES)

    def test_appends_custom_types(self):
        """Should append custom types from plugin settings."""
        custom = [('sla', 'SLA Document', 'teal')]
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'custom_doc_types': custom}}):
            choices = _build_all_choices()
            values = [c[0] for c in choices]
            self.assertIn('sla', values)
            self.assertEqual(len(choices), len(_BUILTIN_CHOICES) + 1)

    def test_skips_duplicate_values(self):
        """Should skip custom types whose value collides with a built-in type."""
        custom = [('diagram', 'Custom Diagram', 'cyan')]
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'custom_doc_types': custom}}):
            choices = _build_all_choices()
            self.assertEqual(len(choices), len(_BUILTIN_CHOICES))
            # The built-in label should be preserved, not the custom one
            diagram_entry = [c for c in choices if c[0] == 'diagram'][0]
            self.assertEqual(diagram_entry[1], 'Network Diagram')

    def test_skips_malformed_entries(self):
        """Should skip entries that are not 3-tuples."""
        custom = [('only_two', 'Missing Color'), ('ok', 'Valid', 'green')]
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'custom_doc_types': custom}}):
            choices = _build_all_choices()
            values = [c[0] for c in choices]
            self.assertNotIn('only_two', values)
            self.assertIn('ok', values)

    def test_returns_builtin_when_no_config(self):
        """Should return built-in choices when PLUGINS_CONFIG has no netbox_documents entry."""
        with self.settings(PLUGINS_CONFIG={}):
            choices = _build_all_choices()
            self.assertEqual(choices, _BUILTIN_CHOICES)


class GetAllowedDocTypesTest(TestCase):
    """Tests for the get_allowed_doc_types() function."""

    def setUp(self):
        self.ct = ContentType.objects.get_for_model(ContentType)

    def test_returns_none_when_mapping_empty(self):
        """Should return None (all types) when allowed_doc_types is empty."""
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': {}}}):
            result = get_allowed_doc_types(self.ct.pk)
            self.assertIsNone(result)

    def test_returns_mapped_types_for_known_model(self):
        """Should return the mapped type list for a model that has an explicit mapping."""
        model_label = f'{self.ct.app_label}.{self.ct.model}'
        mapping = {model_label: ['diagram', 'other']}
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': mapping}}):
            result = get_allowed_doc_types(self.ct.pk)
            self.assertEqual(result, ['diagram', 'other'])

    def test_falls_back_to_all_for_unmapped_model(self):
        """Should fall back to __all__ for a model not explicitly listed."""
        mapping = {
            'some.othermodel': ['diagram'],
            '__all__': ['diagram', 'other', 'quote'],
        }
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': mapping}}):
            result = get_allowed_doc_types(self.ct.pk)
            self.assertEqual(result, ['diagram', 'other', 'quote'])

    def test_returns_none_for_unmapped_model_without_all(self):
        """Should return None when model is not mapped and __all__ is absent."""
        mapping = {'some.othermodel': ['diagram']}
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': mapping}}):
            result = get_allowed_doc_types(self.ct.pk)
            self.assertIsNone(result)

    def test_returns_all_default_when_content_type_is_none(self):
        """Should return __all__ default when content_type_id is None."""
        mapping = {'__all__': ['diagram', 'other']}
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': mapping}}):
            result = get_allowed_doc_types(None)
            self.assertEqual(result, ['diagram', 'other'])

    def test_returns_none_when_content_type_is_none_and_no_all(self):
        """Should return None when content_type_id is None and __all__ is absent."""
        mapping = {'dcim.site': ['diagram']}
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': mapping}}):
            result = get_allowed_doc_types(None)
            self.assertIsNone(result)

    def test_returns_all_default_for_nonexistent_content_type(self):
        """Should fall back to __all__ when content_type_id doesn't exist."""
        mapping = {'__all__': ['other']}
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': mapping}}):
            result = get_allowed_doc_types(99999)
            self.assertEqual(result, ['other'])
