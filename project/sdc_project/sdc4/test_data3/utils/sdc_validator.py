"""
SDC Validator wrapper with automatic Exceptional Value correction.

This module provides validation for SDC4 XML instances using sdcvalidator,
with automatic correction of invalid components using Exceptional Values.
"""
import xml.etree.ElementTree as ET
from typing import Tuple, Dict, List
from dataclasses import dataclass

try:
    from sdcvalidator import Validator as SDCValidatorCore
except ImportError:
    # Fallback for testing/development
    class SDCValidatorCore:
        def __init__(self, xsd_path):
            self.xsd_path = xsd_path

        def validate(self, xml_content):
            return []


@dataclass
class ValidationResult:
    """Result of XML validation"""
    is_valid: bool
    errors: Dict[str, str]
    invalid_components: List[str]


class SDCValidator:
    """
    Wrapper around sdcvalidator with auto-EV correction capability.

    Validates XML instances against XSD schema and can automatically
    apply Exceptional Values to invalid components.
    """

    # EV choices based on error type
    EV_CHOICES = {
        'NotPerformed': 'The action was not performed',
        'NotApplicable': 'The concept does not apply',
        'NotAsked': 'The question was not asked',
        'Refused': 'The subject refused to answer',
        'Unknown': 'The value is unknown',
        'NoInformation': 'No information is available',
    }

    def __init__(self, xsd_path: str):
        """
        Initialize validator with XSD schema path.

        Args:
            xsd_path: Path to the XSD schema file
        """
        self.xsd_path = xsd_path
        self.validator = SDCValidatorCore(xsd_path)

    def validate(self, xml_content: str) -> ValidationResult:
        """
        Validate XML content against XSD schema.

        Args:
            xml_content: XML string to validate

        Returns:
            ValidationResult with validation status and errors
        """
        errors = self.validator.validate(xml_content)

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=self._format_errors(errors),
            invalid_components=self._extract_component_ids(errors)
        )

    def auto_correct_with_evs(
        self,
        xml_content: str,
        errors: Dict[str, str]
    ) -> Tuple[str, List[str]]:
        """
        Apply Exceptional Values to invalid components.

        Args:
            xml_content: Original XML content with validation errors
            errors: Dictionary of component_ct_id -> error_message

        Returns:
            Tuple of (corrected_xml, list_of_corrected_field_labels)
        """
        try:
            tree = ET.fromstring(xml_content)
        except ET.ParseError as e:
            # If XML is unparseable, return as-is with no corrections
            return xml_content, []

        corrected_fields = []

        for component_ct_id, error_msg in errors.items():
            # Find the invalid component by ct-id
            elem = self._find_element_by_ct_id(tree, component_ct_id)

            if elem is not None:
                # Get field label
                label_elem = elem.find('.//label')
                field_label = label_elem.text if label_elem is not None else component_ct_id

                # Remove invalid value element
                value_elem = elem.find('.//value')
                if value_elem is not None:
                    elem.remove(value_elem)

                # Choose appropriate EV based on error type
                ev_value = self._choose_ev_for_error(error_msg)

                # Add exceptional-value element
                ev_elem = ET.SubElement(elem, 'exceptional-value')
                ev_elem.text = ev_value

                corrected_fields.append(field_label)

        # Rebuild XML with pretty printing
        corrected_xml = ET.tostring(tree, encoding='unicode', method='xml')

        # Re-add XML declaration if it was present
        if xml_content.strip().startswith('<?xml'):
            corrected_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + corrected_xml

        return corrected_xml, corrected_fields

    def _find_element_by_ct_id(self, tree: ET.Element, ct_id: str) -> ET.Element:
        """Find an element by its ct-id attribute"""
        for elem in tree.iter():
            if elem.get('ct-id') == ct_id:
                return elem
        return None

    def _choose_ev_for_error(self, error_msg: str) -> str:
        """
        Choose appropriate Exceptional Value based on validation error type.

        Args:
            error_msg: Error message from validator

        Returns:
            Appropriate EV choice (NotPerformed, Unknown, NoInformation, etc.)
        """
        error_lower = error_msg.lower()

        # Match error patterns to appropriate EVs
        if any(word in error_lower for word in ['required', 'missing', 'mandatory']):
            return 'NotPerformed'
        elif any(word in error_lower for word in ['type', 'format', 'pattern']):
            return 'NoInformation'
        elif any(word in error_lower for word in ['range', 'constraint', 'bounds', 'limit']):
            return 'Unknown'
        elif any(word in error_lower for word in ['refused', 'declined']):
            return 'Refused'
        elif any(word in error_lower for word in ['not applicable', 'n/a']):
            return 'NotApplicable'
        else:
            # Default fallback
            return 'NoInformation'

    def _format_errors(self, errors: list) -> Dict[str, str]:
        """
        Format validator errors into a dictionary.

        Args:
            errors: List of error objects from sdcvalidator

        Returns:
            Dictionary of ct_id -> error_message
        """
        formatted = {}

        for error in errors:
            # Extract CT ID and message from error object
            # Format depends on sdcvalidator implementation
            if hasattr(error, 'ct_id') and hasattr(error, 'message'):
                formatted[error.ct_id] = error.message
            elif isinstance(error, dict):
                formatted[error.get('ct_id', 'unknown')] = error.get('message', str(error))
            else:
                # Fallback: use string representation
                formatted[f'error_{len(formatted)}'] = str(error)

        return formatted

    def _extract_component_ids(self, errors: list) -> List[str]:
        """Extract list of component CT IDs from errors"""
        ct_ids = []

        for error in errors:
            if hasattr(error, 'ct_id'):
                ct_ids.append(error.ct_id)
            elif isinstance(error, dict) and 'ct_id' in error:
                ct_ids.append(error['ct_id'])

        return ct_ids
