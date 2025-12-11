<p align="center">
  <img src="https://img.shields.io/badge/SDC4-Semantic%20Data%20Charter-blue?style=for-the-badge" alt="SDC4">
  <img src="https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Standards-NIEM%206.0%20|%20NIH--CDE-orange?style=for-the-badge" alt="Standards">
</p>

<h1 align="center">SDCStudio Examples</h1>

<p align="center">
  <strong>Real-world examples demonstrating AI-powered semantic data modeling</strong>
</p>

<p align="center">
  <a href="#overview">Overview</a> |
  <a href="#examples">Examples</a> |
  <a href="#generated-outputs">Generated Outputs</a> |
  <a href="#getting-started">Getting Started</a> |
  <a href="#about-sdcstudio">About SDCStudio</a>
</p>

---

## Overview

This repository showcases **SDCStudio** capabilities through real-world examples across multiple domains. Each example demonstrates the complete workflow from source data templates to fully generated, standards-compliant data model packages.

**What You'll Find Here:**

| Directory | Description |
|-----------|-------------|
| [`source_templates/`](./source_templates/) | Input templates (Markdown format) used to create data models |
| [`downloads/`](./downloads/) | Generated output packages ready for deployment |

### What These Examples Are For

These examples demonstrate SDCStudio's capabilities and can be used to:

- **Learn SDC4 modeling patterns** - See how data models are structured using clusters, components, and relationships
- **Understand the output formats** - Explore the generated XSD, XML, JSON, RDF, SHACL, and other files
- **Test deployment workflows** - Practice deploying and configuring SDC apps before creating your own
- **Start your own projects** - Use these as starting points and modify them for your domain

> **⚠️ Important Disclaimer**: These examples are for **demonstration purposes only**. The data models and their semantics have **not been reviewed or validated by domain experts**. They are not suitable for production use without thorough review by qualified professionals in the relevant domains (law enforcement, immigration, healthcare, etc.).

---

## Examples

### NIEM (National Information Exchange Model)

The [NIEM examples](./source_templates/NIEM/) demonstrate enterprise-grade data modeling aligned with **NIEM 6.0** standards, the premier framework for government and public safety information exchange.

| Example | Domain | Description |
|---------|--------|-------------|
| [Arrest Report](./source_templates/NIEM/example-arrest-report.md) | Justice | Law enforcement arrest documentation with 80+ fields |
| [Incident Report](./source_templates/NIEM/example-incident-report.md) | Justice | Multi-party incident documentation |
| [Visa Application](./source_templates/NIEM/example-visa-application.md) | Immigration | Visa application processing |
| [Vessel Arrival Report](./source_templates/NIEM/example-vessel-arrival-report.md) | Maritime | ANOA compliance reporting |

**Key Features Demonstrated:**
- Component reuse with `@NIEM:component_name` syntax
- Hierarchical clustering with root and sub-clusters
- Standards alignment (NIBRS, UCR, ISO)
- Complex multi-party relationships

### NIH-CDE (Common Data Elements)

The [NIH-CDE examples](./source_templates/NIH-CDE/) demonstrate healthcare and clinical research data modeling using NIH Common Data Elements standards.

> **Note**: NIH-CDE examples are being developed. Check back for updates.

### CSV Examples (Direct Upload)

The [CSV examples](./source_templates/CSV/) demonstrate SDCStudio's ability to automatically generate data models directly from CSV files - no template required.

| Example | Domain | Description |
|---------|--------|-------------|
| [StatePopulation.csv](./source_templates/CSV/StatePopulation.csv) | Demographics | US state population data with adult population percentages |
| [test_data3.csv](./source_templates/CSV/test_data3.csv) | General | Simple person records (name, DOB, city) |

**Key Features Demonstrated:**
- Direct CSV upload without manual template creation
- Automatic column type inference (text, integer, decimal, date)
- AI-powered semantic enrichment of column descriptions
- Constraint detection from data patterns

This is the fastest way to get started - just upload a CSV and SDCStudio generates a complete SDC4-compliant data model.

---

## Generated Outputs

SDCStudio generates comprehensive output packages for each data model:

### Output Types

| Output | Format | Description |
|--------|--------|-------------|
| **XSD Schema** | `.xsd` | XML Schema Definition for validation |
| **XML Instance** | `.xml` | Example data instances |
| **JSON Instance** | `.json` | Complete JSON data examples |
| **JSON-LD Schema** | `.jsonld` | Linked data semantic descriptions |
| **HTML Documentation** | `.html` | Human-readable documentation |
| **RDF Triples** | `.rdf` | Semantic web integration |
| **SHACL Constraints** | `.shacl` | Schema constraint validation |
| **GQL Statements** | `.gql` | Graph database CREATE statements |

### Download Packages

| Package Type | Location | Description |
|--------------|----------|-------------|
| **Model Packages** | [`downloads/model_pkgs/`](./downloads/model_pkgs/) | Data model definitions only |
| **Enterprise Apps** | [`downloads/Enterprise/`](./downloads/Enterprise/) | Full enterprise application packages |
| **Open Source Apps** | [`downloads/OS/`](./downloads/OS/) | Lightweight application packages |

---

## Getting Started

### Explore the Examples

1. **Browse Source Templates**: Start with the [NIEM Arrest Report](./source_templates/NIEM/example-arrest-report.md) to see a complete example
2. **Examine the Structure**: Note the YAML front matter, cluster hierarchy, and component reuse patterns
3. **Download Generated Outputs**: Get the corresponding [generated package](./downloads/model_pkgs/Arrest-Report.zip) to see all outputs

### Option 1: Deploy Generated Apps (Fastest)

The easiest way to use these examples is with the pre-generated Enterprise apps:

1. Download an Enterprise package from [`downloads/Enterprise/`](./downloads/Enterprise/)
2. Extract and follow the README inside the package
3. Run `docker compose up -d --build`
4. Add more data models using the built-in app installer

See [`downloads/README.md`](./downloads/README.md) for detailed deployment instructions.

### Option 2: Build Your Own Implementation (Full Control)

If you prefer to build a custom application using AI coding assistants (Claude, ChatGPT, Cursor, etc.):

1. Download a **Model Package** from [`downloads/model_pkgs/`](./downloads/model_pkgs/)
2. Extract the ZIP - it contains all schema files plus a `README-AI-PROMPT.md`
3. Open `README-AI-PROMPT.md` for ready-to-use prompts and guidance
4. Share the schema files with your AI assistant and describe your requirements

The `README-AI-PROMPT.md` includes:
- **Prompt templates** for different frameworks (Django, React, FastAPI, Reflex, etc.)
- **Database schema mapping** options (normalized vs JSON embedding)
- **sdcvalidator** integration for full SDC4 compliance
- **Tips for iterating** with AI assistants

This approach gives you complete control over your tech stack and architecture.

### Option 3: Use with SDCStudio

Create your own data models from scratch:

1. Visit [SDCStudio](https://sdcstudio.axiussdc.com) (or your deployment)
2. Create a new project
3. Upload your own `.md` template (see below for how to create one)
4. Watch SDCStudio process and generate outputs
5. Download your customized packages

**Creating Your Own Templates:**

| Resource | Description |
|----------|-------------|
| [`source_templates/`](./source_templates/) | Use these examples as a starting point - copy and modify for your domain |
| [Form2SDCTemplate](https://github.com/SemanticDataCharter/Form2SDCTemplate) | Generate templates from existing forms (PDF, images, etc.) |
| [SDCObsidianTemplate](https://github.com/SemanticDataCharter/SDCObsidianTemplate) | Build templates in Obsidian with live preview and validation |

### Template Format Quick Reference

```markdown
---
template_version: "4.0.0"
dataset:
  name: "Your Data Model Name"
  description: "Description of your data model"
  domain: "Domain"
  project: "ProjectName"
enrichment:
  enable_llm: true
---

# Dataset Overview

Description of your dataset...

## Root Cluster: Main Cluster Name

### Column: column_name
**Type**: text | integer | decimal | date | datetime | boolean | identifier | url
**Description**: What this field represents
**Examples**: Example1, Example2
**Constraints**:
  - required: true
  - pattern: ^[A-Z]{2}-\d{4}$

### Column: reused_column
**ReuseComponent**: @NIEM:component_name
**Description**: How this reused component applies here

## Sub-Cluster: Child Cluster Name
**Parent**: Main Cluster Name

### Column: child_field
**Type**: text
**Description**: Field in the child cluster
```

---

## About SDCStudio

**SDCStudio** is an AI-powered semantic data modeling platform that transforms the way organizations create, manage, and share data models.

### Key Capabilities

- **AI-Assisted Modeling**: Intelligent suggestions based on your data and domain
- **Standards Compliance**: Built-in support for NIEM, NIH-CDE, and custom ontologies
- **Multi-Format Output**: Generate 8+ output formats from a single model definition
- **Component Reuse**: Library of reusable components for rapid development
- **Semantic Enrichment**: Automatic ontology linking and RDF triple generation

### The SDC4 Specification

SDCStudio implements the **Semantic Data Charter (SDC4)** specification, providing:

- **Semantic Clarity**: Every data element has clear, unambiguous meaning
- **Interoperability**: Standards-based outputs work across systems
- **Traceability**: Full lineage from source to generated artifacts
- **Flexibility**: Support for diverse domains and use cases

---

## Repository Structure

```
SDCStudio_Examples/
├── README.md                    # This file
├── LICENSE                      # Apache 2.0 License
├── source_templates/            # Input templates for SDCStudio
│   ├── NIEM/                    # NIEM 6.0 compliant examples (Markdown templates)
│   │   ├── README.md
│   │   ├── 01-niem-code-lists-bundle.md
│   │   ├── 02-niem-core-components-bundle.md
│   │   ├── example-arrest-report.md
│   │   ├── example-incident-report.md
│   │   ├── example-visa-application.md
│   │   └── example-vessel-arrival-report.md
│   ├── CSV/                     # CSV direct upload examples
│   │   ├── StatePopulation.csv  # US state demographics
│   │   └── test_data3.csv       # Simple person records
│   └── NIH-CDE/                 # NIH Common Data Elements (coming soon)
│       └── README.md
└── downloads/                   # Generated output packages
    ├── README.md                # Downloads documentation
    ├── model_pkgs/              # Schema-only packages (XSD, XML, JSON, RDF, etc.)
    ├── Enterprise/              # Full enterprise application packages
    └── OS/                      # Lightweight/open source packages
```

---

## Contributing

We welcome contributions! Whether you're:

- **Adding new domain examples** (healthcare, finance, logistics, etc.)
- **Improving existing templates** with better documentation
- **Reporting issues** with generated outputs
- **Suggesting enhancements** to the example structure

Please see our contributing guidelines for more information.

---

## License

This repository is licensed under the [Apache License 2.0](./LICENSE).

---

## Links

- **SDCStudio**: [https://sdcstudio.axiussdc.com](https://sdcstudio.axiussdc.com)
- **Axius SDC, Inc.**: [https://axius-sdc.com](https://axius-sdc.com)
- **SDC4 Specification**: [https://semanticdatacharter.com](https://semanticdatacharter.com)
- **NIEM**: [https://niem.gov](https://niem.gov)
- **NIH-CDE**: [https://cde.nlm.nih.gov](https://cde.nlm.nih.gov)

---

<p align="center">
  <strong>Built with SDCStudio by <a href="https://axius-sdc.com">Axius SDC, Inc.</a></strong>
</p>
