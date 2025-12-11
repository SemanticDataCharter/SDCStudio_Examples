
"""
XML Template Generator for SDC4 Data Models.

Generates a clean XML template file that users can use for bulk import.
The template contains the complete XML structure with placeholder comments
indicating where user data should be inserted.
"""
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TemplateGenerator:
    """
    Generates downloadable XML templates for bulk import.

    The template:
    - Has the complete XML structure matching the XSD schema
    - Contains helpful comments showing field names and types
    - Uses example placeholders that users replace with actual data
    - Includes all optional metadata fields (VTB, VTE, location, etc.)
    """

    PLACEHOLDER_PREFIX = '__PLACEHOLDER__'
    EV_PLACEHOLDER_PREFIX = '__EV_PLACEHOLDER__'

    # Human-readable type descriptions
    TYPE_HINTS = {
        'xdstring-value': 'string value (text)',
        'xdboolean-value': 'boolean value (true or false)',
        'xdcount-value': 'integer value (whole number)',
        'xdquantity-value': 'decimal value (number with decimals)',
        'xdfloat-value': 'float value (decimal number)',
        'xddouble-value': 'double value (high precision decimal)',
        'xdtemporal-value': 'datetime value (ISO 8601: YYYY-MM-DDTHH:MM:SS)',
        'xdlink-value': 'URI value (URL or URN)',
        'xdfile-value': 'base64 encoded file content',
        'xdordinal-value': 'ordinal value (integer for ranked items)',
    }

    # Metadata field descriptions
    METADATA_HINTS = {
        'vtb': 'Valid Time Begin - when this value became valid (ISO 8601 datetime)',
        'vte': 'Valid Time End - when this value expires (ISO 8601 datetime)',
        'tr': 'Time Recorded - when this value was recorded (ISO 8601 datetime)',
        'modified': 'Time Modified - when this value was last modified (ISO 8601 datetime)',
        'latitude': 'Location latitude (decimal degrees, -90 to 90)',
        'longitude': 'Location longitude (decimal degrees, -180 to 180)',
        'act': 'Access Control Tag - security classification',
        'normal-status': 'Normal status indicator',
        'magnitude-status': 'Magnitude status indicator',
        'accuracy_margin': 'Accuracy margin for measurements',
        'precision_digits': 'Number of precision digits',
    }

    # Exceptional Value codes with descriptions
    EV_HINTS = {
        'NI': 'No Information - No information available',
        'MSK': 'Masked - Value is masked for privacy',
        'INV': 'Invalid - Value is invalid',
        'DER': 'Derived - Value was derived/calculated',
        'UNC': 'Unencoded - Value could not be encoded',
        'OTH': 'Other - Other exceptional condition',
        'NINF': 'Negative Infinity',
        'PINF': 'Positive Infinity',
        'ASKR': 'Asked and Refused - Subject refused to provide',
        'NASK': 'Not Asked - Question was not asked',
        'NAV': 'Not Available - Value not available',
        'NA': 'Not Applicable - Does not apply',
        'TRC': 'Trace - Trace amount detected',
        'ASKU': 'Asked but Unknown - Asked but subject does not know',
        'UNK': 'Unknown - Value is unknown',
        'QS': 'Sufficient Quantity',
    }

    def __init__(
        self,
        dm_ct_id: str,
        dm_label: str,
        field_metadata: Optional[Dict] = None
    ):
        """
        Initialize TemplateGenerator.

        Args:
            dm_ct_id: Data Model CT_ID
            dm_label: Data Model label
            field_metadata: Field metadata dictionary with field info
        """
        self.dm_ct_id = dm_ct_id
        self.dm_label = dm_label
        self.field_metadata = field_metadata or {}

        # Build ct_id to field info mapping
        self._ct_id_to_meta = {}
        for field_name, meta in self.field_metadata.items():
            ct_id = meta.get('ct_id')
            if ct_id:
                self._ct_id_to_meta[ct_id] = {
                    'field_name': field_name,
                    **meta
                }

    def generate_template(self) -> str:
        """
        Generate a clean XML template from the skeleton.

        Returns:
            str: XML template with placeholder comments for user data
        """
        # Load the skeleton XML
        skeleton_path = Path(__file__).parent / 'xml_skeleton.xml'
        if not skeleton_path.exists():
            logger.error(f"XML skeleton not found at {skeleton_path}")
            return self._generate_minimal_template()

        with open(skeleton_path, 'r', encoding='utf-8') as f:
            skeleton = f.read()

        # Transform skeleton into a user-friendly template
        template = self._transform_skeleton(skeleton)

        # Add header comment after XML declaration
        header = self._generate_header_comment()

        # Find the position after the XML declaration (<?xml ...?>)
        if template.startswith('<?xml'):
            # Find the end of the XML declaration
            decl_end = template.find('?>') + 2
            template = template[:decl_end] + '\n' + header + template[decl_end:]
        else:
            # No XML declaration, add one with header
            template = '<?xml version="1.0" encoding="UTF-8"?>\n' + header + template

        return template

    def _transform_skeleton(self, skeleton: str) -> str:
        """
        Transform the skeleton XML into a user-friendly template.

        - Replace __PLACEHOLDER__ values with <!-- ENTER: description -->
        - Remove ev-placeholder elements (replace with comment)
        - Keep structure intact
        """
        template = skeleton

        # Replace metadata placeholders
        template = self._replace_metadata_placeholders(template)

        # Replace field value placeholders
        template = self._replace_field_placeholders(template)

        # Remove ev-placeholder elements and add EV comment
        template = self._replace_ev_placeholders(template)

        # Clean up any remaining placeholders
        template = self._cleanup_remaining_placeholders(template)

        return template

    def _replace_metadata_placeholders(self, template: str) -> str:
        """Replace standard metadata placeholders with examples."""
        # creation_timestamp - example ISO datetime
        template = template.replace(
            f'{self.PLACEHOLDER_PREFIX}creation_timestamp',
            '<!-- ENTER: creation timestamp (ISO 8601) - Example: 2024-01-15T10:30:00 -->'
        )

        # instance_id - will be replaced on import
        template = template.replace(
            f'{self.PLACEHOLDER_PREFIX}instance_id',
            '<!-- AUTO-GENERATED: instance_id will be assigned on import -->'
        )

        # instance_version
        template = template.replace(
            f'{self.PLACEHOLDER_PREFIX}instance_version',
            '1.0'
        )

        # current-state
        template = template.replace(
            f'{self.PLACEHOLDER_PREFIX}current-state',
            ''
        )

        return template

    def _replace_field_placeholders(self, template: str) -> str:
        """Replace field value and metadata placeholders with helpful comments."""
        # Process each field
        for ct_id, meta in self._ct_id_to_meta.items():
            field_name = meta.get('field_name', ct_id)
            field_type = meta.get('type', 'XdString')
            field_label = meta.get('label', field_name)

            # Get value element name for this type
            value_elem_name = self._get_value_element_name(field_type)

            # Replace value placeholder
            value_placeholder = f'{self.PLACEHOLDER_PREFIX}{value_elem_name}_{ct_id}'
            type_hint = self.TYPE_HINTS.get(value_elem_name, 'value')
            template = template.replace(
                value_placeholder,
                f'<!-- ENTER: {field_label} ({type_hint}) -->'
            )

            # Replace optional metadata placeholders
            for meta_name, hint in self.METADATA_HINTS.items():
                meta_placeholder = f'{self.PLACEHOLDER_PREFIX}{meta_name}_{ct_id}'
                if meta_placeholder in template:
                    # Check if this metadata is allowed for this field
                    allow_key = f'allow_{meta_name.replace("-", "_")}'
                    if meta.get(allow_key, False) or meta_name in ('normal-status', 'magnitude-status', 'accuracy_margin', 'precision_digits'):
                        template = template.replace(
                            meta_placeholder,
                            f'<!-- OPTIONAL: {hint} -->'
                        )
                    else:
                        # Remove elements not allowed for this field
                        template = self._remove_element_line(template, meta_name, ct_id)

            # Handle units placeholders
            units_info = meta.get('units', {})
            if units_info:
                units_ct_id = units_info.get('ct_id', '')
                units_label = units_info.get('label', f'{field_label}_units')
                symbols = units_info.get('symbols', [])

                if units_ct_id:
                    # Replace units label placeholder
                    label_placeholder = f'{self.PLACEHOLDER_PREFIX}label_{units_ct_id}'
                    template = template.replace(label_placeholder, units_label)

                    # Replace units value placeholder
                    units_value_placeholder = f'{self.PLACEHOLDER_PREFIX}xdstring-value_{units_ct_id}'
                    if symbols:
                        symbols_str = ', '.join(symbols)
                        template = template.replace(
                            units_value_placeholder,
                            f'<!-- ENTER: units - valid values: {symbols_str} -->'
                        )
                    else:
                        template = template.replace(
                            units_value_placeholder,
                            f'<!-- ENTER: units -->'
                        )

        return template

    def _replace_ev_placeholders(self, template: str) -> str:
        """Remove ev-placeholder elements and add helpful EV comment."""
        # Pattern to match ev-placeholder elements
        ev_pattern = r'<ev-placeholder[^>]*>.*?</ev-placeholder>'

        # Build EV options comment
        ev_comment = self._build_ev_comment()

        # Replace ev-placeholder with comment about EV options
        template = re.sub(
            ev_pattern,
            f'<!-- OPTIONAL: Exceptional Value - See template header for valid EV codes -->',
            template
        )

        return template

    def _build_ev_comment(self) -> str:
        """Build a comment block describing EV options."""
        lines = ['Available Exceptional Value codes:']
        for code, description in self.EV_HINTS.items():
            lines.append(f'    {code}: {description}')
        return '\n'.join(lines)

    def _cleanup_remaining_placeholders(self, template: str) -> str:
        """Clean up any remaining __PLACEHOLDER__ strings."""
        # Replace any remaining placeholders with generic comment
        pattern = r'__PLACEHOLDER__[a-zA-Z0-9_-]+'
        template = re.sub(
            pattern,
            '<!-- ENTER: value -->',
            template
        )

        # Clean up EV placeholders
        ev_pattern = r'__EV_PLACEHOLDER__[a-zA-Z0-9_-]+'
        template = re.sub(ev_pattern, '', template)

        return template

    def _remove_element_line(self, template: str, element_name: str, ct_id: str) -> str:
        """Remove an element line containing a placeholder."""
        # Pattern to match the entire element line
        pattern = rf'^\s*<{element_name}>[^<]*{self.PLACEHOLDER_PREFIX}[^<]*</{element_name}>\s*\n?'
        template = re.sub(pattern, '', template, flags=re.MULTILINE)
        return template

    def _generate_header_comment(self) -> str:
        """Generate a header comment with instructions."""
        header = f"""<!--
================================================================================
XML TEMPLATE FOR BULK IMPORT
================================================================================

Data Model: {self.dm_label}
DM CT_ID: {self.dm_ct_id}
Generated: {datetime.utcnow().isoformat()}

INSTRUCTIONS:
1. Copy this template for each record you want to import
2. Replace <!-- ENTER: ... --> comments with your actual data
3. Optional fields (marked <!-- OPTIONAL: ... -->) can be deleted if not needed
4. The instance_id will be auto-generated on import - leave as is
5. Save all XML files in a directory or zip file for bulk import

EXCEPTIONAL VALUES (EV):
If a field has no value but needs an explanation, use one of these EV codes
by replacing the ev-placeholder comment with the appropriate element:

Example: <NASK><ev-name>Not Asked</ev-name></NASK>

"""
        # Add EV codes
        for code, description in self.EV_HINTS.items():
            header += f"  {code}: {description}\n"

        header += """
================================================================================
-->
"""
        return header

    def _generate_minimal_template(self) -> str:
        """Generate a minimal template if skeleton is not available."""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!--
XML Template for {self.dm_label}
Skeleton file not found - please regenerate the app.
-->
<sdc4:dm-{self.dm_ct_id}
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:sdc4="https://semanticdatacharter.com/ns/sdc4/"
  xsi:schemaLocation="https://semanticdatacharter.com/ns/sdc4/ https://semanticdatacharter.com/dmlib/dm-{self.dm_ct_id}.xsd">
  <dm-label>{self.dm_label}</dm-label>
  <!-- Template generation failed - skeleton not found -->
</sdc4:dm-{self.dm_ct_id}>
"""

    def _get_value_element_name(self, field_type: str) -> str:
        """Get the value element name for a given field type."""
        type_map = {
            'XdString': 'xdstring-value',
            'XdBoolean': 'xdboolean-value',
            'XdCount': 'xdcount-value',
            'XdQuantity': 'xdquantity-value',
            'XdFloat': 'xdfloat-value',
            'XdDouble': 'xddouble-value',
            'XdTemporal': 'xdtemporal-value',
            'XdLink': 'xdlink-value',
            'XdFile': 'xdfile-value',
            'XdOrdinal': 'xdordinal-value',
        }
        return type_map.get(field_type, 'value')

