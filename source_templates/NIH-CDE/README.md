# NIH Common Data Elements (CDE) Templates

This directory contains SDCStudio templates aligned with NIH Common Data Elements standards for healthcare and clinical research data modeling.

## About NIH CDE

The [NIH Common Data Elements (CDE)](https://cde.nlm.nih.gov/) Repository is a resource for researchers and clinical trialists that contains structured, standardized data elements for use in biomedical and clinical research.

### Key Benefits

- **Standardization**: Consistent data collection across studies
- **Interoperability**: Enable data sharing between institutions
- **Quality**: Validated, expert-reviewed elements
- **Compliance**: Support for regulatory requirements

## Available Templates

*Templates coming soon*

| Template | Domain | Description |
|----------|--------|-------------|
| TBD | Clinical Trials | Common trial data elements |
| TBD | Patient Demographics | Standard demographic fields |
| TBD | Adverse Events | Safety reporting elements |

## Component Library

NIH-CDE components will be available for reuse:

```markdown
### Column: patient_age
**ReuseComponent**: @NIH-CDE:patient_age_years
**Description**: Patient age at enrollment
```

## Standards Alignment

Templates in this directory align with:

- NIH Common Data Element Repository standards
- CDISC (Clinical Data Interchange Standards Consortium)
- HL7 FHIR (where applicable)
- HIPAA compliance considerations

## Creating Healthcare Templates

When creating NIH-CDE templates:

1. Reference official CDE definitions from [cde.nlm.nih.gov](https://cde.nlm.nih.gov)
2. Include permissible value sets where defined
3. Document validation requirements
4. Note any regulatory considerations
5. Reference related FHIR resources if applicable

## Related Resources

- [NIH CDE Repository](https://cde.nlm.nih.gov)
- [CDISC Standards](https://www.cdisc.org)
- [HL7 FHIR](https://www.hl7.org/fhir/)
- [Source Templates Overview](../README.md)
