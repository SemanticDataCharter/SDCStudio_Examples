---
template_version: "4.0.0"
dataset:
  name: "Incident Report"
  description: "Law enforcement incident documentation including event details, location, involved parties, and property"
  domain: "Justice"
  creator: "NIEM 6.0"
  project: "NIEM"
enrichment:
  enable_llm: true
---

# Dataset Overview

Comprehensive incident report for law enforcement documentation of events, following NIEM Justice domain (j:) standards. Captures incident details, location, involved persons, witnesses, property, and narrative.

**Purpose**: Document law enforcement incidents for records management systems, CAD integration, UCR/NIBRS reporting, and information sharing.

**Business Context**: Used by police departments, sheriff's offices, state law enforcement for incident documentation. Feeds into RMS (Records Management Systems), CAD systems, and crime analysis databases.

**Standards Alignment**:
- NIEM Justice Domain (j:) v6.0
- NIEM Core (nc:) v6.0
- FBI UCR (Uniform Crime Reporting)
- NIBRS (National Incident-Based Reporting System)

## Root Cluster: Incident Report

### Column: incident_report_number
**Type**: identifier
**Description**: Unique identifier for this incident report
**Examples**: IR-2024-001234, 2024-INC-567890, INC-2024-9876
**Constraints**:
  - required: true
  - pattern: ^[A-Z]{2,4}-\d{4}-\d{6}$

### Column: incident_date_time
**ReuseComponent**: @NIEM:incident_date
**Description**: Date and time when incident occurred

### Column: report_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time when this report was filed

### Column: incident_category
**ReuseComponent**: @NIEM:incident_category_code
**Description**: Type or category of incident

### Column: incident_location_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: Street address where incident occurred

### Column: incident_location_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: City where incident occurred

### Column: incident_location_state
**ReuseComponent**: @NIEM:location_state_code
**Description**: State where incident occurred

### Column: incident_location_zip
**ReuseComponent**: @NIEM:location_postal_code
**Description**: ZIP code of incident location

### Column: incident_location_latitude
**ReuseComponent**: @NIEM:location_latitude_degree
**Description**: Latitude coordinate of incident location

### Column: incident_location_longitude
**ReuseComponent**: @NIEM:location_longitude_degree
**Description**: Longitude coordinate of incident location

### Column: reporting_agency_name
**ReuseComponent**: @NIEM:organization_name
**Description**: Law enforcement agency filing the report

### Column: reporting_agency_ori
**Type**: identifier
**Description**: Originating Agency Identifier (ORI) - 9-character NCIC agency code
**Examples**: CA0012300, NY0034500, TX1234567
**Constraints**:
  - pattern: ^[A-Z]{2}\d{7}$

## Sub-Cluster: Reporting Officer
**Parent**: Incident Report

### Column: officer_badge_number
**Type**: identifier
**Description**: Badge number of reporting officer
**Examples**: 1234, B-5678, S-9012

### Column: officer_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Officer's first name

### Column: officer_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Officer's last name

### Column: officer_rank
**Type**: text
**Description**: Officer's rank or title
**Examples**: Officer, Sergeant, Lieutenant, Detective

### Column: officer_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Officer's contact phone number

### Column: officer_email
**ReuseComponent**: @NIEM:contact_email_id
**Description**: Officer's email address

## Sub-Cluster: Victim Information
**Parent**: Incident Report

### Column: victim_type
**Type**: text
**Description**: Type of victim (person, business, etc.)
**Enumeration**:
  - person: Individual Person
  - business: Business/Organization
  - government: Government Entity
  - other: Other

### Column: victim_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Victim's first name (if person)

### Column: victim_middle_name
**ReuseComponent**: @NIEM:person_middle_name
**Description**: Victim's middle name

### Column: victim_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Victim's last name

### Column: victim_dob
**ReuseComponent**: @NIEM:date_representation
**Description**: Victim's date of birth

### Column: victim_sex
**ReuseComponent**: @NIEM:person_sex
**Description**: Victim's gender

### Column: victim_race
**ReuseComponent**: @NIEM:person_race
**Description**: Victim's race

### Column: victim_home_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: Victim's home street address

### Column: victim_home_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: Victim's home city

### Column: victim_home_state
**ReuseComponent**: @NIEM:location_state_code
**Description**: Victim's home state

### Column: victim_home_zip
**ReuseComponent**: @NIEM:location_postal_code
**Description**: Victim's home ZIP code

### Column: victim_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Victim's contact phone

### Column: victim_email
**ReuseComponent**: @NIEM:contact_email_id
**Description**: Victim's email address

### Column: victim_organization_name
**ReuseComponent**: @NIEM:organization_name
**Description**: Organization name (if victim is business/government)

## Sub-Cluster: Suspect Information
**Parent**: Incident Report

### Column: suspect_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Suspect's first name

### Column: suspect_middle_name
**ReuseComponent**: @NIEM:person_middle_name
**Description**: Suspect's middle name

### Column: suspect_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Suspect's last name

### Column: suspect_dob
**ReuseComponent**: @NIEM:date_representation
**Description**: Suspect's date of birth

### Column: suspect_sex
**ReuseComponent**: @NIEM:person_sex
**Description**: Suspect's gender

### Column: suspect_race
**ReuseComponent**: @NIEM:person_race
**Description**: Suspect's race

### Column: suspect_height
**ReuseComponent**: @NIEM:person_height
**Description**: Suspect's height in centimeters

### Column: suspect_weight
**ReuseComponent**: @NIEM:person_weight
**Description**: Suspect's weight in kilograms

### Column: suspect_eye_color
**ReuseComponent**: @NIEM:person_eye_color
**Description**: Suspect's eye color

### Column: suspect_hair_color
**ReuseComponent**: @NIEM:person_hair_color
**Description**: Suspect's hair color

### Column: suspect_last_known_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: Suspect's last known street address

### Column: suspect_last_known_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: Suspect's last known city

### Column: suspect_last_known_state
**ReuseComponent**: @NIEM:location_state_code
**Description**: Suspect's last known state

## Sub-Cluster: Property Involved
**Parent**: Incident Report

### Column: property_category
**Type**: text
**Description**: Category of property involved
**Enumeration**:
  - stolen: Stolen Property
  - recovered: Recovered Property
  - evidence: Evidence
  - damaged: Damaged Property
  - seized: Seized Property

### Column: property_description
**Type**: text
**Description**: Description of property
**Examples**: Black leather wallet, 2020 Honda Civic, iPhone 13 Pro

### Column: property_value
**ReuseComponent**: @NIEM:amount_value
**Description**: Estimated value in US dollars

### Column: property_currency
**ReuseComponent**: @NIEM:currency_code
**Description**: Currency code (typically USD)

### Column: serial_number
**Type**: text
**Description**: Serial number or other unique identifier
**Examples**: ABC123456789, VIN:1HGBH41JXMN109186

## Sub-Cluster: Vehicle Involved
**Parent**: Incident Report

### Column: vehicle_vin
**ReuseComponent**: @NIEM:vehicle_identification_number
**Description**: Vehicle Identification Number

### Column: vehicle_make
**ReuseComponent**: @NIEM:vehicle_make_name
**Description**: Vehicle manufacturer

### Column: vehicle_model
**ReuseComponent**: @NIEM:vehicle_model_name
**Description**: Vehicle model

### Column: vehicle_year
**ReuseComponent**: @NIEM:vehicle_year
**Description**: Vehicle year

### Column: vehicle_color
**ReuseComponent**: @NIEM:vehicle_color_primary
**Description**: Vehicle primary color

### Column: vehicle_license_plate
**ReuseComponent**: @NIEM:vehicle_license_plate_number
**Description**: Vehicle license plate number

### Column: vehicle_license_state
**ReuseComponent**: @NIEM:location_state_code
**Description**: State that issued vehicle license plate

### Column: vehicle_role
**Type**: text
**Description**: Role of vehicle in incident
**Enumeration**:
  - suspect: Suspect Vehicle
  - victim: Victim Vehicle
  - witness: Witness Vehicle
  - evidence: Evidence Vehicle

## Sub-Cluster: Witness Information
**Parent**: Incident Report

### Column: witness_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Witness's first name

### Column: witness_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Witness's last name

### Column: witness_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Witness's contact phone

### Column: witness_statement
**Type**: text
**Description**: Summary of witness statement

## Sub-Cluster: Incident Narrative
**Parent**: Incident Report

### Column: incident_summary
**Type**: text
**Description**: Brief summary of incident (one paragraph)

### Column: incident_narrative
**Type**: text
**Description**: Detailed narrative of incident, investigation, and officer actions
**Business Rules**: Should include: what happened, when, where, who was involved, witness statements, evidence collected, actions taken

### Column: officer_actions_taken
**Type**: text
**Description**: Description of actions taken by officer
**Examples**: Secured scene, interviewed witnesses, collected evidence, photographed damage

### Column: evidence_collected
**Type**: boolean
**Description**: Whether evidence was collected

### Column: evidence_description
**Type**: text
**Description**: Description of evidence collected

### Column: photos_taken
**Type**: boolean
**Description**: Whether photographs were taken

### Column: number_of_photos
**Type**: integer
**Description**: Number of photographs taken
**Constraints**:
  - range: [0, 999]

## Sub-Cluster: Report Status
**Parent**: Incident Report

### Column: report_status
**ReuseComponent**: @NIEM:status_code
**Description**: Current status of incident report

### Column: case_status
**ReuseComponent**: @NIEM:case_status_code
**Description**: Status of investigation

### Column: disposition
**Type**: text
**Description**: Disposition of incident
**Enumeration**:
  - cleared_arrest: Cleared by Arrest
  - cleared_exceptional: Cleared Exceptionally
  - unfounded: Unfounded
  - investigation_continuing: Investigation Continuing
  - suspended: Suspended

### Column: supervisor_reviewed_by
**Type**: text
**Description**: Name of supervisor who reviewed report

### Column: supervisor_review_date
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time supervisor reviewed report

### Column: approved_by
**Type**: text
**Description**: Name of person who approved report

### Column: approval_date
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date report was approved
