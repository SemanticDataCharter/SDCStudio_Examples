# Contributing to SDCStudio Examples

Thank you for your interest in contributing to the SDCStudio Examples repository! This guide will help you get started.

## Ways to Contribute

### 1. Add New Domain Examples

We welcome examples from new domains:

- **Healthcare**: Patient records, clinical trials, lab results
- **Finance**: Transaction records, compliance reports, risk assessments
- **Logistics**: Shipment tracking, inventory management, supply chain
- **Education**: Student records, course catalogs, credentials
- **Government**: Permits, licenses, regulatory filings
- **And more!**

### 2. Improve Existing Templates

- Add better documentation and examples
- Improve field descriptions
- Add missing constraints
- Fix typos or errors

### 3. Report Issues

- Problems with generated outputs
- Documentation gaps
- Template format questions
- Feature suggestions

## Contribution Process

### For New Templates

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b add-domain-example`
3. **Add your template** to the appropriate directory under `source_templates/`
4. **Test with SDCStudio** to ensure it processes correctly
5. **Add generated outputs** to `downloads/` (optional)
6. **Submit a pull request**

### Template Requirements

All templates must include:

```markdown
---
template_version: "4.0.0"
dataset:
  name: "Descriptive Name"
  description: "Clear description"
  domain: "Domain Name"
  creator: "Your Name/Organization"
  project: "ProjectName"
enrichment:
  enable_llm: true  # or false
---

# Dataset Overview

[Business context and purpose]

## Root Cluster: [Name]

### Column: field_name
**Type**: [valid type]
**Description**: [clear description]
```

### Quality Guidelines

**Good templates include:**

- Clear, descriptive names for clusters and columns
- Meaningful descriptions that explain business context
- Realistic examples for each field
- Appropriate constraints (required, patterns, ranges)
- Reference to applicable standards (if any)
- Documentation of business rules

**Please avoid:**

- Placeholder or generic descriptions
- Missing type definitions
- Undocumented constraints
- Invalid YAML syntax
- Broken component references

## Directory Structure

```
source_templates/
├── NIEM/                # NIEM 6.0 standard examples
├── NIH-CDE/             # Healthcare/clinical examples
└── [new-domain]/        # Your new domain
    ├── README.md        # Domain overview
    └── example-*.md     # Template files
```

## Naming Conventions

- **Directories**: lowercase with hyphens (`new-domain/`)
- **Template files**: `example-descriptive-name.md`
- **Column names**: lowercase with underscores (`field_name`)
- **Cluster names**: Title Case with spaces (`Root Cluster Name`)

## Code of Conduct

- Be respectful and constructive
- Focus on improving the examples
- Help others learn the SDCStudio format
- Acknowledge contributions from others

## Questions?

- Open an issue for questions
- Review existing examples for guidance
- Check SDCStudio documentation

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for helping make SDCStudio Examples better!
