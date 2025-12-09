---
template_version: "4.0.0"
dataset:
  name: "Arrest Report"
  description: "Law enforcement arrest documentation with arrestee, charges, location, and officer information"
  domain: "Justice"
  creator: "NIEM 6.0"
  project: "NIEM"
enrichment:
  enable_llm: true
---

# Dataset Overview

Comprehensive arrest report capturing the apprehension of a subject by law enforcement, following NIEM Justice domain (j:) standards. Documents arrestee information, charges, arrest circumstances, location, and arresting officers.

**Purpose**: Capture complete arrest event information for law enforcement records management systems, court case management, jail booking systems, and criminal justice information sharing.

**Business Context**: Used by police departments, sheriff's offices, state law enforcement agencies, and federal law enforcement to document arrests. Integrates with CAD (Computer-Aided Dispatch), RMS (Records Management Systems), jail management systems, and state/federal criminal justice databases (NCIC, state repositories).

**Standards Alignment**:
- NIEM Justice Domain (j:) v6.0
- NIEM Core (nc:) v6.0
- FBI UCR (Uniform Crime Reporting)
- NIBRS (National Incident-Based Reporting System)

## Root Cluster: Arrest Report

### Column: arrest_report_number
**Type**: identifier
**Description**: Unique identifier for this arrest report
**Examples**: AR-2024-001234, 2024-123456-A, ARREST-2024-567890
**Constraints**:
  - required: true
  - pattern: ^[A-Z]{2,4}-\d{4}-\d{6}(-[A-Z])?$

### Column: arrest_date_time
**ReuseComponent**: @NIEM:arrest_date
**Description**: Date and time when arrest occurred

### Column: report_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time when this report was filed

### Column: arrest_location_description
**ReuseComponent**: @NIEM:arrest_location
**Description**: Narrative description of arrest location

### Column: arrest_location_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: Street address where arrest occurred

### Column: arrest_location_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: City where arrest occurred

### Column: arrest_location_state
**ReuseComponent**: @NIEM:location_state_code
**Description**: State where arrest occurred (two-letter code)

### Column: arrest_location_zip
**ReuseComponent**: @NIEM:location_postal_code
**Description**: ZIP code of arrest location

### Column: arrest_location_latitude
**ReuseComponent**: @NIEM:location_latitude_degree
**Description**: Latitude coordinate of arrest location

### Column: arrest_location_longitude
**ReuseComponent**: @NIEM:location_longitude_degree
**Description**: Longitude coordinate of arrest location

### Column: arresting_agency_name
**ReuseComponent**: @NIEM:arrest_agency
**Description**: Law enforcement agency that made the arrest
**Examples**: Springfield Police Department, State Highway Patrol, FBI

### Column: arresting_agency_ori
**Type**: identifier
**Description**: Originating Agency Identifier (ORI) - 9-character NCIC agency code
**Examples**: CA0012300, NY0034500, TX1234567
**Constraints**:
  - pattern: ^[A-Z]{2}\d{7}$

## Sub-Cluster: Arrestee Information
**Parent**: Arrest Report

### Column: arrestee_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Arrestee's first name

### Column: arrestee_middle_name
**ReuseComponent**: @NIEM:person_middle_name
**Description**: Arrestee's middle name

### Column: arrestee_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Arrestee's last name

### Column: arrestee_suffix
**ReuseComponent**: @NIEM:person_name_suffix
**Description**: Arrestee's name suffix

### Column: arrestee_dob
**ReuseComponent**: @NIEM:date_representation
**Description**: Arrestee's date of birth

### Column: arrestee_ssn
**Type**: identifier
**Description**: Arrestee's Social Security Number
**Constraints**:
  - pattern: ^\d{3}-\d{2}-\d{4}$

### Column: arrestee_sex
**ReuseComponent**: @NIEM:person_sex
**Description**: Arrestee's gender

### Column: arrestee_race
**ReuseComponent**: @NIEM:person_race
**Description**: Arrestee's race

### Column: arrestee_ethnicity
**ReuseComponent**: @NIEM:ethnicity_code
**Description**: Arrestee's ethnicity (Hispanic/Non-Hispanic)

### Column: arrestee_height
**ReuseComponent**: @NIEM:person_height
**Description**: Arrestee's height in centimeters

### Column: arrestee_weight
**ReuseComponent**: @NIEM:person_weight
**Description**: Arrestee's weight in kilograms

### Column: arrestee_eye_color
**ReuseComponent**: @NIEM:person_eye_color
**Description**: Arrestee's eye color

### Column: arrestee_hair_color
**ReuseComponent**: @NIEM:person_hair_color
**Description**: Arrestee's hair color

### Column: arrestee_home_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: Arrestee's home street address

### Column: arrestee_home_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: Arrestee's home city

### Column: arrestee_home_state
**ReuseComponent**: @NIEM:location_state_code
**Description**: Arrestee's home state

### Column: arrestee_home_zip
**ReuseComponent**: @NIEM:location_postal_code
**Description**: Arrestee's home ZIP code

### Column: arrestee_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Arrestee's telephone number

### Column: arrestee_email
**ReuseComponent**: @NIEM:contact_email_id
**Description**: Arrestee's email address

## Sub-Cluster: Arresting Officer
**Parent**: Arrest Report

### Column: officer_badge_number
**Type**: identifier
**Description**: Badge number of arresting officer
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
**Examples**: Officer, Sergeant, Lieutenant, Detective, Agent

### Column: officer_unit
**Type**: text
**Description**: Officer's assigned unit or division
**Examples**: Patrol Division, Narcotics, Gang Unit, Traffic

### Column: officer_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Officer's contact phone number

### Column: officer_email
**ReuseComponent**: @NIEM:contact_email_id
**Description**: Officer's email address

## Sub-Cluster: Primary Charge
**Parent**: Arrest Report

### Column: charge_statute_code
**ReuseComponent**: @NIEM:charge_statute
**Description**: Statute or code section violated
**Examples**: PC 245(a)(1), 18 USC 1001, VC 23152(a)

### Column: charge_description_text
**ReuseComponent**: @NIEM:charge_description
**Description**: Description of the charge

### Column: charge_severity_level
**ReuseComponent**: @NIEM:charge_severity
**Description**: Severity level of charge (felony, misdemeanor, infraction)

### Column: charge_count
**Type**: integer
**Description**: Number of counts for this charge
**Examples**: 1, 2, 3
**Constraints**:
  - range: [1, 99]

## Sub-Cluster: Additional Charges
**Parent**: Arrest Report

### Column: additional_charge_statute
**ReuseComponent**: @NIEM:charge_statute
**Description**: Additional charge statute code

### Column: additional_charge_description
**ReuseComponent**: @NIEM:charge_description
**Description**: Additional charge description

### Column: additional_charge_severity
**ReuseComponent**: @NIEM:charge_severity
**Description**: Additional charge severity level

### Column: additional_charge_count
**Type**: integer
**Description**: Number of counts for additional charge
**Constraints**:
  - range: [1, 99]

## Sub-Cluster: Arrest Circumstances
**Parent**: Arrest Report

### Column: incident_report_number
**ReuseComponent**: @NIEM:incident_report_number
**Description**: Related incident report number if applicable

### Column: incident_category
**ReuseComponent**: @NIEM:incident_category
**Description**: Type of incident leading to arrest

### Column: arrest_type
**Type**: text
**Description**: Type or category of arrest
**Enumeration**:
  - on_view: On-View Arrest - Officer witnessed crime
  - warrant: Warrant Arrest - Arrest based on warrant
  - citizen: Citizen's Arrest - Private person arrest
  - summons: Summoned Arrest - Court summons

### Column: use_of_force
**Type**: boolean
**Description**: Whether force was used during arrest

### Column: use_of_force_description
**Type**: text
**Description**: Description of force used if applicable
**Examples**: Verbal commands, Physical control, OC spray, Taser, Firearm

### Column: arrestee_injured
**Type**: boolean
**Description**: Whether arrestee sustained injuries

### Column: arrestee_injury_description
**Type**: text
**Description**: Description of arrestee injuries if any

### Column: officer_injured
**Type**: boolean
**Description**: Whether officer sustained injuries

### Column: officer_injury_description
**Type**: text
**Description**: Description of officer injuries if any

### Column: property_seized
**Type**: boolean
**Description**: Whether property was seized from arrestee

### Column: property_description
**Type**: text
**Description**: Description of property seized
**Examples**: Cash ($500), Handgun (Glock 9mm), Narcotics (10g methamphetamine), Vehicle (2020 Honda Accord)

### Column: evidence_collected
**Type**: boolean
**Description**: Whether evidence was collected

### Column: evidence_description
**Type**: text
**Description**: Description of evidence collected

## Sub-Cluster: Custody Information
**Parent**: Arrest Report

### Column: custody_status
**ReuseComponent**: @NIEM:custody_status_code
**Description**: Current custody status of arrestee

### Column: booking_number
**Type**: identifier
**Description**: Jail booking number if booked
**Examples**: BK-2024-5678, 2024-BOOK-9012

### Column: booking_facility
**Type**: text
**Description**: Name of jail or detention facility where booked
**Examples**: County Jail, Metropolitan Detention Center

### Column: bail_amount
**ReuseComponent**: @NIEM:amount_value
**Description**: Bail amount set in US dollars

### Column: bail_currency
**ReuseComponent**: @NIEM:currency_code
**Description**: Currency code for bail amount (typically USD)

### Column: release_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time of release if released

### Column: release_type
**Type**: text
**Description**: Type of release if applicable
**Enumeration**:
  - bail: Released on Bail
  - bond: Released on Bond
  - own_recognizance: Released on Own Recognizance (OR)
  - citation: Cite and Release
  - other: Other

## Sub-Cluster: Vehicle Information
**Parent**: Arrest Report

### Column: vehicle_involved
**Type**: boolean
**Description**: Whether a vehicle was involved in the arrest

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

### Column: vehicle_disposition
**Type**: text
**Description**: What happened to the vehicle
**Enumeration**:
  - released: Released to Owner
  - impounded: Impounded
  - towed: Towed
  - evidence: Held as Evidence

## Sub-Cluster: Narrative
**Parent**: Arrest Report

### Column: arrest_narrative
**Type**: text
**Description**: Detailed narrative description of arrest circumstances and events
**Business Rules**: Should include: probable cause for arrest, sequence of events, subject behavior, officer actions, witness information, Miranda rights advisement

### Column: miranda_rights_given
**Type**: boolean
**Description**: Whether Miranda rights were read to arrestee

### Column: miranda_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time Miranda rights were given

### Column: arrestee_statement
**Type**: text
**Description**: Statement made by arrestee if any

### Column: witness_names
**Type**: text
**Description**: Names of witnesses to arrest

### Column: witness_statements
**Type**: text
**Description**: Witness statements if obtained

## Sub-Cluster: Follow-up
**Parent**: Arrest Report

### Column: case_number
**ReuseComponent**: @NIEM:case_tracking_id
**Description**: Court case number if filed

### Column: case_file_date
**ReuseComponent**: @NIEM:case_file_date
**Description**: Date case was filed with court/prosecutor

### Column: prosecutor_assigned
**Type**: text
**Description**: Name of prosecutor or DA assigned to case

### Column: arraignment_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Date of arraignment hearing

### Column: disposition
**ReuseComponent**: @NIEM:disposition_code
**Description**: Final disposition of arrest/charges

### Column: report_status
**ReuseComponent**: @NIEM:status_code
**Description**: Current status of arrest report

### Column: report_approved_by
**Type**: text
**Description**: Name of supervisor who approved report

### Column: report_approval_date
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date report was approved
