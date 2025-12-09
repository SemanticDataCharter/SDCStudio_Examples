# NIEM Foundation Components and Examples

This directory contains SDCStudio-compatible markdown templates for creating NIEM 6.0 compliant data models using a bundling approach.

## Overview

**Strategy**: Foundation components (code lists and core components) are bundled into temporary "wrapper" data models for efficient upload. After processing, the wrapper data models can be deleted while individual components persist and become available for reuse.

**Project Name**: `NIEM` (all components published here)

## Files Included

### Foundation Bundles (Upload First)

1. **`01-niem-code-lists-bundle.md`**
   - Contains 20+ NIEM standard code lists as columns
   - Includes: state codes, country codes, severity levels, status codes, gender codes, contact types, address categories, identification types, incident categories, charge severity, vehicle types, weapon categories, case status, custody status, disposition codes, relationship codes, ethnicity codes, race codes, eye color codes, hair color codes, language codes
   - **Action**: Upload to SDCStudio, wait for processing, then DELETE the "NIEM Code Lists Bundle" data model
   - **Result**: Individual code list components available as `@NIEM:state_code`, `@NIEM:country_code`, etc.

2. **`02-niem-core-components-bundle.md`**
   - Contains 100+ core components organized in sub-clusters
   - Sub-clusters: Person Name, US Address, Contact Information, Organization Information, Location Coordinates, Date and Time, Identification, Vehicle Information, Physical Description, Monetary Amount, Case Information, Arrest Information, Charge Information, Incident Information
   - **Action**: Upload to SDCStudio, wait for processing, then DELETE the "NIEM Core Components Bundle" data model
   - **Result**: Individual components available as `@NIEM:person_given_name`, `@NIEM:location_street_full_text`, `@NIEM:contact_telephone_number`, etc.

### Upload Instructions

3. **`UPLOAD_SEQUENCE.md`**
   - Step-by-step instructions for uploading bundles
   - Post-upload actions and verification steps
   - Troubleshooting guidance
   - Component reference lists

## Domain Template Examples

After uploading and publishing foundation components, use these examples as templates for creating domain-specific data models:

### Justice Domain

4. **`example-arrest-report.md`**
   - Comprehensive arrest report template
   - Captures arrestee information, charges, arrest circumstances, custody, vehicle, narrative
   - Demonstrates reuse of person, location, contact, vehicle, and date/time components

5. **`example-incident-report.md`**
   - Law enforcement incident documentation
   - Includes victim, suspect, witness, property, vehicle, and narrative sections
   - Shows complex multi-party scenario with multiple sub-clusters

### Immigration Domain

6. **`example-visa-application.md`**
   - Visa application form template
   - Covers applicant demographics, passport, travel plans, employment, education, family, security screening
   - Demonstrates extensive use of person, address, contact, and identification components

### Maritime Domain

7. **`example-vessel-arrival-report.md`**
   - Vessel arrival notification (ANOA)
   - Includes vessel details, crew manifest, cargo summary, customs, health/security, environmental compliance
   - Shows integration of organization, location, and regulatory components

## Component Reuse Syntax

All domain examples use the component reuse syntax:

```markdown
### Column: column_name
**ReuseComponent**: @NIEM:component_name
**Description**: Description of how this column is used in this context
```

## Quick Start

### Step 1: Upload Foundation Bundles

1. Log into SDCStudio
2. Create a project named **"NIEM"** if it doesn't exist
   - Project description: "NIEM 6.0 standard components and code lists"
3. Upload `01-niem-code-lists-bundle.md`
   - Wait for status: "Completed"
   - Verify all code list columns created as individual components
   - **Delete** the "NIEM Code Lists Bundle" data model (wrapper)
4. Upload `02-niem-core-components-bundle.md`
   - Wait for status: "Completed"
   - Verify all sub-cluster columns created as individual components
   - **Delete** the "NIEM Core Components Bundle" data model (wrapper)

### Step 2: Publish Components

1. Go to NIEM project in SDCStudio
2. Publish all created components (batch publish if available)
3. Verify components are available for reuse

### Step 3: Create Domain Data Models

1. Use example templates as starting points
2. Customize for your specific use case
3. Reference foundation components using `@NIEM:component_name`
4. Upload and test

## Verification Checklist

After completing uploads:

- [ ] NIEM project contains components only (no wrapper data models)
- [ ] All components are published and available for reuse
- [ ] Approximately 120-140 individual components exist
- [ ] Can create test data model that references `@NIEM:ComponentName`
- [ ] All four example templates demonstrate correct syntax

## Template Format Requirements

All templates follow SDCStudio markdown format:

**Required YAML Front Matter**:
```yaml
---
template_version: "4.0.0"
dataset:
  name: "Dataset Name"
  description: "Description"
  domain: "Domain"
  creator: "NIEM 6.0"
  project: "NIEM"
enrichment:
  enable_llm: true  # or false
---
```

**Required Structure**:
- Dataset Overview section
- Root Cluster (exactly one)
- Sub-Clusters (optional, must specify parent)
- Columns with user-friendly types

**User-Friendly Types**:
- `text` - Maps to XdString or XdToken
- `integer` - Maps to XdCount, XdOrdinal, or XdIdentifier
- `decimal` - Maps to XdQuantity, XdFloat, or XdDouble
- `date` - Maps to XdTemporal (date only)
- `datetime` - Maps to XdTemporal (date with time)
- `boolean` - Maps to XdBoolean
- `identifier` - Maps to XdIdentifier
- `url` - Maps to XdLink

## Available Components

### Code List Components (20+)
- `@NIEM:state_code` - US state codes
- `@NIEM:country_code` - ISO country codes
- `@NIEM:severity_level` - Severity levels
- `@NIEM:status_code` - Status codes
- `@NIEM:gender_code` - Gender classifications
- `@NIEM:contact_method_type` - Contact method types
- `@NIEM:address_category_code` - Address categories
- `@NIEM:identification_category_code` - ID types
- `@NIEM:incident_category_code` - Incident categories
- `@NIEM:charge_severity_level` - Charge severity
- `@NIEM:vehicle_type_code` - Vehicle types
- `@NIEM:weapon_category_code` - Weapon categories
- `@NIEM:case_status_code` - Case status
- `@NIEM:custody_status_code` - Custody status
- `@NIEM:disposition_code` - Disposition codes
- `@NIEM:relationship_code` - Relationship types
- `@NIEM:ethnicity_code` - Ethnicity codes
- `@NIEM:race_code` - Race codes
- `@NIEM:eye_color_code` - Eye color codes
- `@NIEM:hair_color_code` - Hair color codes
- `@NIEM:language_code` - Language codes

### Core Components (100+)

**Person Components**:
- `@NIEM:person_given_name` - First name
- `@NIEM:person_middle_name` - Middle name
- `@NIEM:person_surname` - Last name
- `@NIEM:person_name_suffix` - Name suffix
- `@NIEM:person_full_name` - Full name
- `@NIEM:person_sex` - Gender
- `@NIEM:person_race` - Race
- `@NIEM:person_height` - Height
- `@NIEM:person_weight` - Weight
- `@NIEM:person_eye_color` - Eye color
- `@NIEM:person_hair_color` - Hair color

**Address Components**:
- `@NIEM:location_street_full_text` - Full street address
- `@NIEM:location_street_number` - Street number
- `@NIEM:location_street_name` - Street name
- `@NIEM:address_secondary_unit` - Apt/Suite/Unit
- `@NIEM:location_city_name` - City name
- `@NIEM:location_state_code` - State code
- `@NIEM:location_postal_code` - ZIP code
- `@NIEM:location_country_code` - Country code

**Contact Components**:
- `@NIEM:contact_telephone_number` - Phone number
- `@NIEM:contact_email_id` - Email address
- `@NIEM:contact_fax_number` - Fax number
- `@NIEM:contact_mailing_address` - Mailing address
- `@NIEM:contact_website_uri` - Website URL

**Organization Components**:
- `@NIEM:organization_name` - Organization name
- `@NIEM:organization_abbreviation` - Organization abbreviation
- `@NIEM:organization_tax_id` - Tax ID (EIN)

**Location Components**:
- `@NIEM:location_latitude_degree` - Latitude
- `@NIEM:location_longitude_degree` - Longitude
- `@NIEM:location_altitude` - Altitude

**Date/Time Components**:
- `@NIEM:date_representation` - Date
- `@NIEM:datetime_representation` - Date and time
- `@NIEM:time_representation` - Time
- `@NIEM:date_range_start` - Start date
- `@NIEM:date_range_end` - End date

**Identification Components**:
- `@NIEM:identification_id` - ID value
- `@NIEM:identification_category` - ID type
- `@NIEM:identification_expiration_date` - Expiration date
- `@NIEM:identification_issuer` - Issuing organization

**Vehicle Components**:
- `@NIEM:vehicle_identification_number` - VIN
- `@NIEM:vehicle_make_name` - Make
- `@NIEM:vehicle_model_name` - Model
- `@NIEM:vehicle_year` - Year
- `@NIEM:vehicle_color_primary` - Color
- `@NIEM:vehicle_license_plate_number` - License plate

**Monetary Components**:
- `@NIEM:amount_value` - Amount
- `@NIEM:currency_code` - Currency

**Case/Legal Components**:
- `@NIEM:case_tracking_id` - Case ID
- `@NIEM:case_title` - Case title
- `@NIEM:case_file_date` - Filing date
- `@NIEM:case_status` - Case status
- `@NIEM:arrest_date` - Arrest date
- `@NIEM:arrest_location` - Arrest location
- `@NIEM:arrest_agency` - Arresting agency
- `@NIEM:charge_statute` - Statute/code
- `@NIEM:charge_description` - Charge description
- `@NIEM:charge_severity` - Charge severity
- `@NIEM:charge_filing_date` - Charge filing date

**Incident Components**:
- `@NIEM:incident_date` - Incident date/time
- `@NIEM:incident_location` - Incident location
- `@NIEM:incident_category` - Incident category
- `@NIEM:incident_report_number` - Report number

## Support and Documentation

**Related Files**:
- `../NIEM_TEMPLATE_IMPLEMENTATION_PLAN.md` - Complete implementation plan
- `../LESSONS_LEARNED.md` - What we learned from initial approach
- `UPLOAD_SEQUENCE.md` - Detailed upload instructions

**Key Principles**:
1. Foundation components must be uploaded and published FIRST
2. Delete wrapper data models after processing completes
3. Components persist even after data model deletion
4. Use `@NIEM:component_name` syntax for reuse
5. Project name must be "NIEM" for all components

## Timeline Estimate

- **Step 1 upload**: ~2-3 minutes processing time
- **Step 2 upload**: ~3-5 minutes processing time
- **Cleanup**: ~5 minutes to delete wrappers and verify
- **Total**: ~15 minutes for complete foundation

After foundation is ready, each domain template takes ~2-3 minutes to upload and process.

## Next Steps

1. Upload foundation bundles (Step 1)
2. Publish all components (Step 2)
3. Test component reuse by uploading one example template
4. Create your own domain-specific templates
5. Share feedback on template format and usability
