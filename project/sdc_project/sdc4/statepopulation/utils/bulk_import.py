
"""
Bulk Import Processor for SDC4 XML Instances.

This module processes bulk XML imports from zip files or directories,
running each file through the standard validation pipeline.
"""
import os
import zipfile
import tempfile
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from lxml import etree
from cuid2 import cuid_wrapper

logger = logging.getLogger(__name__)

# Initialize CUID2 generator
cuid_generator = cuid_wrapper()


@dataclass
class ImportResult:
    """Result of importing a single XML file."""
    filename: str
    success: bool
    instance_id: Optional[str] = None
    error_message: Optional[str] = None
    validation_status: Optional[str] = None
    auto_corrected_fields: List[str] = field(default_factory=list)


@dataclass
class BulkImportResult:
    """Result of a bulk import operation."""
    total_files: int
    successful: int
    failed: int
    results: List[ImportResult] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def duration_seconds(self) -> float:
        """Calculate duration of import."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_files == 0:
            return 0.0
        return (self.successful / self.total_files) * 100

    def get_failures(self) -> List[ImportResult]:
        """Get list of failed imports."""
        return [r for r in self.results if not r.success]


class BulkImportProcessor:
    """
    Processes bulk XML imports for SDC4 data models.

    Supports importing from:
    - Directory path containing XML files
    - Zip file containing XML files

    Each XML file is processed through the same pipeline as form submissions:
    1. Parse XML and assign new instance_id
    2. Validate with sdcvalidator
    3. Auto-apply EVs if validation fails
    4. Extract JSON data
    5. Extract RDF and upload to Fuseki
    6. Save to database
    """

    SDC4_NS = 'https://semanticdatacharter.com/ns/sdc4/'

    def __init__(
        self,
        model_class,
        xsd_path: Union[str, Path],
        dm_ct_id: str,
        dm_label: str,
        field_metadata: Dict[str, Any]
    ):
        """
        Initialize BulkImportProcessor.

        Args:
            model_class: Django model class for the data model
            xsd_path: Path to the XSD schema file
            dm_ct_id: Data Model CT_ID
            dm_label: Data Model label
            field_metadata: FIELD_METADATA from the model
        """
        self.model_class = model_class
        self.xsd_path = Path(xsd_path)
        self.dm_ct_id = dm_ct_id
        self.dm_label = dm_label
        self.field_metadata = field_metadata

    def process_directory(self, directory_path: Union[str, Path]) -> BulkImportResult:
        """
        Process all XML files in a directory.

        Args:
            directory_path: Path to directory containing XML files

        Returns:
            BulkImportResult with success/failure counts and details
        """
        directory = Path(directory_path)
        if not directory.exists():
            return BulkImportResult(
                total_files=0,
                successful=0,
                failed=1,
                results=[ImportResult(
                    filename=str(directory_path),
                    success=False,
                    error_message=f"Directory not found: {directory_path}"
                )]
            )

        # Find all XML files
        xml_files = list(directory.glob('*.xml'))
        return self._process_files(xml_files)

    def process_zipfile(self, zip_path: Union[str, Path]) -> BulkImportResult:
        """
        Process all XML files in a zip archive.

        Args:
            zip_path: Path to zip file containing XML files

        Returns:
            BulkImportResult with success/failure counts and details
        """
        zip_path = Path(zip_path)
        if not zip_path.exists():
            return BulkImportResult(
                total_files=0,
                successful=0,
                failed=1,
                results=[ImportResult(
                    filename=str(zip_path),
                    success=False,
                    error_message=f"Zip file not found: {zip_path}"
                )]
            )

        # Extract to temp directory and process
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    # Extract only XML files
                    xml_names = [n for n in zf.namelist() if n.lower().endswith('.xml')]
                    zf.extractall(temp_dir, members=xml_names)

                # Find extracted XML files
                xml_files = list(Path(temp_dir).rglob('*.xml'))
                return self._process_files(xml_files)

            except zipfile.BadZipFile:
                return BulkImportResult(
                    total_files=0,
                    successful=0,
                    failed=1,
                    results=[ImportResult(
                        filename=str(zip_path),
                        success=False,
                        error_message=f"Invalid zip file: {zip_path}"
                    )]
                )

    def _process_files(self, xml_files: List[Path]) -> BulkImportResult:
        """Process a list of XML files."""
        result = BulkImportResult(
            total_files=len(xml_files),
            successful=0,
            failed=0,
            started_at=datetime.utcnow()
        )

        for xml_file in xml_files:
            file_result = self._process_single_file(xml_file)
            result.results.append(file_result)

            if file_result.success:
                result.successful += 1
            else:
                result.failed += 1

        result.completed_at = datetime.utcnow()
        return result

    def _process_single_file(self, xml_file: Path) -> ImportResult:
        """
        Process a single XML file through the import pipeline.

        Args:
            xml_file: Path to XML file

        Returns:
            ImportResult for this file
        """
        filename = xml_file.name

        try:
            # Read XML content
            with open(xml_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            # Parse and assign new instance_id
            xml_content, instance_id = self._assign_new_instance_id(xml_content)

            # Update creation_timestamp
            xml_content = self._update_creation_timestamp(xml_content)

            # Import the utilities we need
            from .sdc_validator import SDCValidator
            from .json_extractor import JSONExtractor
            from .json_instance_generator import JSONInstanceGenerator
            from .rdf_extractor import RDFExtractor
            from sdc4.utils.triplestore import get_triplestore_client

            # Validate with sdcvalidator
            validator = SDCValidator(str(self.xsd_path))
            validation_result = validator.validate(xml_content)

            validation_status = 'valid'
            validation_errors = {}
            auto_corrected_fields = []

            if not validation_result.is_valid:
                # Auto-correct with Exceptional Values
                xml_content, auto_corrected_fields = validator.auto_correct_with_evs(
                    xml_content,
                    validation_result.errors
                )

                # Update instance_id with EV marker
                base_cuid = instance_id.replace('i-', '').replace('ev-', '')
                new_instance_id = f"i-ev-{base_cuid}"
                xml_content = xml_content.replace(instance_id, new_instance_id)
                instance_id = new_instance_id

                validation_status = 'valid_with_ev'
                validation_errors = validation_result.errors

            # Extract JSON for JSONB queries
            json_extractor = JSONExtractor(field_metadata=self.field_metadata)
            extracted = json_extractor.extract(xml_content)
            json_data = extracted['fields']
            search_text = extracted['search_text']

            # Generate complete JSON instance
            json_instance_generator = JSONInstanceGenerator(field_metadata=self.field_metadata)
            json_instance = json_instance_generator.generate(xml_content)

            # Extract field values for model fields
            field_values = self._extract_field_values(xml_content)

            # Create the model instance
            from django.db import transaction

            with transaction.atomic():
                instance = self.model_class(
                    instance_id=instance_id,
                    xml_content=xml_content,
                    json_data=json_data,
                    json_instance=json_instance,
                    search_text=search_text,
                    validation_status=validation_status,
                    validation_errors=validation_errors,
                    auto_corrected_fields=auto_corrected_fields,
                    **field_values
                )
                instance.save()

            # Upload RDF to triplestore (outside transaction)
            try:
                triplestore = get_triplestore_client()
                if triplestore is None:
                    instance.rdf_sync_status = 'disabled'
                    instance.save(update_fields=['rdf_sync_status'])
                else:
                    rdf_extractor = RDFExtractor(
                        dm_ct_id=self.dm_ct_id,
                        dm_label=self.dm_label,
                        field_metadata=self.field_metadata
                    )
                    rdf_content = rdf_extractor.extract(
                        xml_content=xml_content,
                        instance_id=instance_id,
                        validation_status=validation_status,
                        auto_corrected_fields=auto_corrected_fields
                    )

                    if rdf_content:
                        graph_uri = triplestore.get_graph_uri(instance_id, self.dm_ct_id)

                        if triplestore.upload_graph(rdf_content, None):  # Upload to default graph
                            instance.fuseki_graph_uri = graph_uri
                            instance.rdf_uploaded_at = datetime.utcnow()
                            instance.rdf_sync_status = 'synced'
                        else:
                            instance.rdf_sync_status = 'failed'

                        instance.save(update_fields=['fuseki_graph_uri', 'rdf_uploaded_at', 'rdf_sync_status'])

            except Exception as rdf_error:
                logger.warning(f"RDF upload failed for {filename}: {rdf_error}")
                instance.rdf_sync_status = 'failed'
                instance.save(update_fields=['rdf_sync_status'])

            return ImportResult(
                filename=filename,
                success=True,
                instance_id=instance_id,
                validation_status=validation_status,
                auto_corrected_fields=auto_corrected_fields
            )

        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            return ImportResult(
                filename=filename,
                success=False,
                error_message=str(e)
            )

    def _assign_new_instance_id(self, xml_content: str) -> Tuple[str, str]:
        """
        Assign a new instance_id to the XML content.

        Args:
            xml_content: XML string

        Returns:
            Tuple of (updated_xml_content, new_instance_id)
        """
        # Generate new instance_id
        new_instance_id = f"i-{cuid_generator()}"

        try:
            # Parse XML
            root = etree.fromstring(xml_content.encode('utf-8'))

            # Find instance_id element
            instance_id_elem = root.find('.//instance_id')
            if instance_id_elem is not None:
                instance_id_elem.text = new_instance_id
            else:
                # If not found, try to add it
                logger.warning("instance_id element not found in XML")

            # Serialize back
            xml_content = etree.tostring(
                root,
                pretty_print=True,
                encoding='UTF-8',
                xml_declaration=True
            ).decode('utf-8')

        except etree.XMLSyntaxError as e:
            logger.warning(f"XML parsing error during instance_id assignment: {e}")
            # Try string replacement as fallback
            import re
            pattern = r'<instance_id>[^<]*</instance_id>'
            xml_content = re.sub(pattern, f'<instance_id>{new_instance_id}</instance_id>', xml_content)

        return xml_content, new_instance_id

    def _update_creation_timestamp(self, xml_content: str) -> str:
        """Update the creation_timestamp to now."""
        timestamp = datetime.utcnow().isoformat()

        try:
            root = etree.fromstring(xml_content.encode('utf-8'))

            # Find creation_timestamp element
            ts_elem = root.find('.//creation_timestamp')
            if ts_elem is not None:
                ts_elem.text = timestamp

            xml_content = etree.tostring(
                root,
                pretty_print=True,
                encoding='UTF-8',
                xml_declaration=True
            ).decode('utf-8')

        except etree.XMLSyntaxError as e:
            logger.warning(f"XML parsing error during timestamp update: {e}")
            import re
            pattern = r'<creation_timestamp>[^<]*</creation_timestamp>'
            xml_content = re.sub(pattern, f'<creation_timestamp>{timestamp}</creation_timestamp>', xml_content)

        return xml_content

    def _extract_field_values(self, xml_content: str) -> Dict[str, Any]:
        """
        Extract field values from XML for Django model fields.

        Args:
            xml_content: XML string

        Returns:
            Dict of field_name -> value
        """
        field_values = {}

        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            nsmap = {'sdc4': self.SDC4_NS}

            for field_name, meta in self.field_metadata.items():
                ct_id = meta.get('ct_id', '')
                field_type = meta.get('type', 'XdString')

                if not ct_id:
                    continue

                # Find the component element
                comp_elem = root.find(f".//sdc4:ms-{ct_id}", namespaces=nsmap)
                if comp_elem is None:
                    continue

                # Get value element name
                value_elem_name = self._get_value_element_name(field_type)

                # Handle XdTemporal specially - try all variant element names
                if value_elem_name is None and field_type == 'XdTemporal':
                    raw_value = None
                    for temporal_elem_name in self.TEMPORAL_ELEMENT_NAMES:
                        value_elem = comp_elem.find(f".//{temporal_elem_name}")
                        if value_elem is not None and value_elem.text:
                            raw_value = value_elem.text.strip()
                            break
                    if raw_value is None:
                        continue
                else:
                    # Find value element
                    value_elem = comp_elem.find(f".//{value_elem_name}")
                    if value_elem is None or not value_elem.text:
                        continue

                    # Parse value based on type
                    raw_value = value_elem.text.strip()

                # Skip placeholder values
                if raw_value.startswith('__PLACEHOLDER__') or raw_value.startswith('<!-- '):
                    continue

                field_values[field_name] = self._parse_value(raw_value, field_type)

        except etree.XMLSyntaxError as e:
            logger.warning(f"XML parsing error during field extraction: {e}")

        return field_values

    # XdTemporal variant element names
    TEMPORAL_ELEMENT_NAMES = [
        'xdtemporal-date',
        'xdtemporal-time',
        'xdtemporal-datetime',
        'xdtemporal-duration',
        'xdtemporal-day',
        'xdtemporal-month',
        'xdtemporal-year',
        'xdtemporal-year-month',
        'xdtemporal-month-day',
    ]

    def _get_value_element_name(self, field_type: str) -> str:
        """Get the value element name for a given field type."""
        type_map = {
            'XdString': 'xdstring-value',
            'XdBoolean': 'xdboolean-value',
            'XdCount': 'xdcount-value',
            'XdQuantity': 'xdquantity-value',
            'XdFloat': 'xdfloat-value',
            'XdDouble': 'xddouble-value',
            'XdLink': 'xdlink-value',
            'XdFile': 'xdfile-value',
            'XdOrdinal': 'xdordinal-value',
        }
        # XdTemporal returns None - caller must handle specially
        if field_type == 'XdTemporal':
            return None
        return type_map.get(field_type, 'value')

    def _parse_value(self, value_str: str, field_type: str) -> Any:
        """Parse a string value to the appropriate Python type."""
        if field_type == 'XdBoolean':
            return value_str.lower() == 'true'

        if field_type in ('XdCount', 'XdOrdinal'):
            try:
                return int(value_str)
            except ValueError:
                return None

        if field_type in ('XdQuantity', 'XdFloat', 'XdDouble'):
            try:
                from decimal import Decimal
                return Decimal(value_str)
            except Exception:
                return None

        # XdString, XdTemporal, XdLink, XdFile - return as string
        return value_str

