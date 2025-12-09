# Source Templates

This directory contains SDCStudio-compatible Markdown templates that define data models. These templates are processed by SDCStudio to generate comprehensive output packages.

## Template Categories

| Directory | Standard | Description |
|-----------|----------|-------------|
| [`NIEM/`](./NIEM/) | NIEM 6.0 | Government and public safety data exchange |
| [`NIH-CDE/`](./NIH-CDE/) | NIH CDE | Healthcare and clinical research |

## Template Format Overview

SDCStudio templates use a structured Markdown format with YAML front matter:

```markdown
---
template_version: "4.0.0"
dataset:
  name: "Data Model Name"
  description: "What this data model represents"
  domain: "Domain Name"
  creator: "Creator/Standard"
  project: "ProjectName"
enrichment:
  enable_llm: true
---

# Dataset Overview

[Description and business context]

## Root Cluster: [Main Cluster Name]

### Column: field_name
**Type**: text | integer | decimal | date | datetime | boolean | identifier | url
**Description**: Description of the field
**Examples**: Example1, Example2
**Constraints**:
  - required: true
  - pattern: ^regex$

## Sub-Cluster: [Child Cluster Name]
**Parent**: [Main Cluster Name]

### Column: child_field
**Type**: text
**Description**: Field in child cluster
```

## Supported Types

| Type | Description | Maps To |
|------|-------------|---------|
| `text` | String values | XdString, XdToken |
| `integer` | Whole numbers | XdCount, XdOrdinal |
| `decimal` | Decimal numbers | XdQuantity, XdFloat |
| `date` | Date only | XdTemporal (date) |
| `datetime` | Date and time | XdTemporal (datetime) |
| `boolean` | True/false | XdBoolean |
| `identifier` | Unique IDs | XdIdentifier |
| `url` | Web links | XdLink |

## Component Reuse

Templates can reference pre-built components using the reuse syntax:

```markdown
### Column: person_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: First name of the individual
```

This enables:
- Consistent field definitions across models
- Automatic semantic linking
- Reduced template duplication

## Creating New Templates

1. **Choose a standard** (NIEM, NIH-CDE) or create custom
2. **Define YAML front matter** with metadata
3. **Document the dataset** in the overview section
4. **Define the root cluster** (required, exactly one)
5. **Add sub-clusters** as needed for hierarchy
6. **Define columns** with types, descriptions, and constraints
7. **Add reuse references** for standard components

## Validation

Templates are validated during upload:
- YAML front matter syntax
- Required fields present
- Valid type references
- Proper cluster hierarchy
- Component reference resolution

## Best Practices

- Use descriptive names for clusters and columns
- Include real-world examples in column definitions
- Document business context in the overview
- Use constraints to define validation rules
- Reference standard components where available
- Keep hierarchies meaningful (2-3 levels typically)

## Generated Outputs

When processed, each template generates:

- XSD Schema (`.xsd`)
- XML Instance (`.xml`)
- JSON Instance (`.json`)
- JSON-LD Schema (`.jsonld`)
- HTML Documentation (`.html`)
- RDF Triples (`.rdf`)
- SHACL Constraints (`.shacl`)
- GQL Statements (`.gql`)

See [`../downloads/`](../downloads/) for generated packages.
