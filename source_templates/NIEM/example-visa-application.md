---
template_version: "4.0.0"
dataset:
  name: "Visa Application"
  description: "Immigration visa application capturing applicant information, travel details, purpose, and supporting documentation"
  domain: "Immigration"
  creator: "NIEM 6.0"
  project: "NIEM"
enrichment:
  enable_llm: true
---

# Dataset Overview

Comprehensive visa application form for processing nonimmigrant and immigrant visa requests, following NIEM Immigration domain (im:) standards. Documents applicant demographics, passport information, travel plans, employment, family ties, and security screening.

**Purpose**: Capture visa application information for consular processing, border management systems, and immigration case management.

**Business Context**: Used by U.S. Department of State consular posts, USCIS adjudication centers, and border inspection systems (CBP). Integrates with SEVIS (Student Exchange Visitor Information System), PIMS (Person Centric Query Service), and biometric systems.

**Standards Alignment**:
- NIEM Immigration Domain (im:) v6.0
- NIEM Core (nc:) v6.0
- Department of State visa classifications
- INA (Immigration and Nationality Act) regulations

## Root Cluster: Visa Application

### Column: application_number
**Type**: identifier
**Description**: Unique visa application identifier
**Examples**: DS-160-2024-1234567, APP-2024-5678901
**Constraints**:
  - required: true
  - pattern: ^[A-Z]{2,6}-\d{4}-\d{7}$

### Column: application_date
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time application was submitted

### Column: visa_type
**Type**: text
**Description**: Type of visa being requested
**Enumeration**:
  - B1: Business Visitor
  - B2: Tourist Visitor
  - F1: Academic Student
  - J1: Exchange Visitor
  - H1B: Specialty Occupation Worker
  - L1: Intracompany Transferee
  - O1: Extraordinary Ability
  - K1: Fiancé(e) of U.S. Citizen
  - CR1: Spouse of U.S. Citizen
  - IR1: Immediate Relative
  - EB1: Employment-Based First Preference
  - EB2: Employment-Based Second Preference
  - EB3: Employment-Based Third Preference

### Column: visa_class
**Type**: text
**Description**: Visa classification (immigrant vs nonimmigrant)
**Enumeration**:
  - immigrant: Immigrant Visa
  - nonimmigrant: Nonimmigrant Visa

### Column: application_status
**ReuseComponent**: @NIEM:status_code
**Description**: Current application processing status

### Column: consular_post
**Type**: text
**Description**: U.S. Embassy or Consulate processing application
**Examples**: U.S. Embassy London, U.S. Consulate Toronto, U.S. Embassy Mexico City

## Sub-Cluster: Applicant Information
**Parent**: Visa Application

### Column: applicant_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Applicant's first name (given name)

### Column: applicant_middle_name
**ReuseComponent**: @NIEM:person_middle_name
**Description**: Applicant's middle name

### Column: applicant_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Applicant's last name (surname/family name)

### Column: applicant_full_name
**ReuseComponent**: @NIEM:person_full_name
**Description**: Applicant's full name

### Column: applicant_dob
**ReuseComponent**: @NIEM:date_representation
**Description**: Applicant's date of birth

### Column: applicant_sex
**ReuseComponent**: @NIEM:person_sex
**Description**: Applicant's gender

### Column: applicant_nationality
**ReuseComponent**: @NIEM:country_code
**Description**: Applicant's country of nationality

### Column: applicant_country_of_birth
**ReuseComponent**: @NIEM:country_code
**Description**: Country where applicant was born

### Column: applicant_city_of_birth
**ReuseComponent**: @NIEM:location_city_name
**Description**: City where applicant was born

### Column: applicant_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Applicant's telephone number

### Column: applicant_email
**ReuseComponent**: @NIEM:contact_email_id
**Description**: Applicant's email address

### Column: marital_status
**Type**: text
**Description**: Applicant's marital status
**Enumeration**:
  - single: Single/Never Married
  - married: Married
  - divorced: Divorced
  - widowed: Widowed
  - separated: Legally Separated
  - domestic_partnership: Domestic Partnership

## Sub-Cluster: Passport Information
**Parent**: Visa Application

### Column: passport_number
**Type**: identifier
**Description**: Passport number
**Examples**: AB1234567, P1234567890

### Column: passport_country
**ReuseComponent**: @NIEM:country_code
**Description**: Country that issued passport

### Column: passport_issue_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Date passport was issued

### Column: passport_expiration_date
**ReuseComponent**: @NIEM:identification_expiration_date
**Description**: Date passport expires

### Column: passport_issuing_authority
**ReuseComponent**: @NIEM:identification_issuer
**Description**: Authority that issued passport
**Examples**: U.S. Department of State, UK Passport Office

## Sub-Cluster: Current Address
**Parent**: Visa Application

### Column: current_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: Current street address

### Column: current_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: Current city

### Column: current_state
**Type**: text
**Description**: Current state/province/region

### Column: current_postal_code
**ReuseComponent**: @NIEM:location_postal_code
**Description**: Current postal code

### Column: current_country
**ReuseComponent**: @NIEM:country_code
**Description**: Current country of residence

## Sub-Cluster: Travel Information
**Parent**: Visa Application

### Column: purpose_of_trip
**Type**: text
**Description**: Primary purpose of U.S. travel
**Enumeration**:
  - business: Business
  - tourism: Tourism/Vacation
  - education: Education/Study
  - employment: Employment
  - family_visit: Visit Family
  - medical_treatment: Medical Treatment
  - conference: Conference/Convention
  - cultural_exchange: Cultural Exchange
  - other: Other

### Column: purpose_description
**Type**: text
**Description**: Detailed description of travel purpose

### Column: intended_arrival_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Intended date of arrival in United States

### Column: intended_length_of_stay
**Type**: integer
**Description**: Intended length of stay in days
**Constraints**:
  - range: [1, 365]

### Column: address_in_us_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: U.S. address where applicant will stay

### Column: address_in_us_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: U.S. city where applicant will stay

### Column: address_in_us_state
**ReuseComponent**: @NIEM:location_state_code
**Description**: U.S. state where applicant will stay

### Column: address_in_us_zip
**ReuseComponent**: @NIEM:location_postal_code
**Description**: U.S. ZIP code

### Column: us_contact_name
**Type**: text
**Description**: Name of person or organization in U.S. to contact

### Column: us_contact_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Phone number of U.S. contact

### Column: us_contact_relationship
**Type**: text
**Description**: Relationship to U.S. contact
**Examples**: Friend, Employer, University, Hotel, Family Member

## Sub-Cluster: Employment Information
**Parent**: Visa Application

### Column: current_employer
**ReuseComponent**: @NIEM:organization_name
**Description**: Name of current employer

### Column: employer_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: Employer street address

### Column: employer_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: Employer city

### Column: employer_country
**ReuseComponent**: @NIEM:country_code
**Description**: Employer country

### Column: employer_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Employer telephone number

### Column: job_title
**Type**: text
**Description**: Current job title or occupation
**Examples**: Software Engineer, Teacher, Student, Retired

### Column: employment_start_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Date started current employment

### Column: monthly_income
**ReuseComponent**: @NIEM:amount_value
**Description**: Monthly income in applicant's local currency

### Column: income_currency
**ReuseComponent**: @NIEM:currency_code
**Description**: Currency code for income

## Sub-Cluster: Education Background
**Parent**: Visa Application

### Column: highest_education_level
**Type**: text
**Description**: Highest level of education completed
**Enumeration**:
  - primary: Primary School
  - secondary: Secondary/High School
  - vocational: Vocational/Technical
  - some_university: Some University
  - bachelors: Bachelor's Degree
  - masters: Master's Degree
  - doctorate: Doctorate/PhD
  - professional: Professional Degree (MD, JD, etc.)

### Column: educational_institution
**Type**: text
**Description**: Name of educational institution attended
**Examples**: University of Toronto, MIT, Cambridge University

### Column: field_of_study
**Type**: text
**Description**: Major field of study
**Examples**: Computer Science, Medicine, Business Administration

### Column: graduation_year
**Type**: integer
**Description**: Year of graduation
**Constraints**:
  - range: [1950, 2100]

## Sub-Cluster: Previous U.S. Travel
**Parent**: Visa Application

### Column: previously_visited_us
**Type**: boolean
**Description**: Whether applicant has previously visited United States

### Column: previous_visa_type
**Type**: text
**Description**: Type of previous U.S. visa held

### Column: previous_visa_number
**Type**: identifier
**Description**: Previous visa number

### Column: previous_visa_issue_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Date previous visa was issued

### Column: previous_visa_expiration_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Date previous visa expired

### Column: previous_visa_lost_or_stolen
**Type**: boolean
**Description**: Whether previous visa was lost or stolen

### Column: previous_visa_cancelled
**Type**: boolean
**Description**: Whether previous visa was cancelled or revoked

### Column: ever_denied_us_visa
**Type**: boolean
**Description**: Whether applicant was ever denied a U.S. visa

### Column: visa_denial_explanation
**Type**: text
**Description**: Explanation if previously denied visa

## Sub-Cluster: Family Information
**Parent**: Visa Application

### Column: father_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Father's first name

### Column: father_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Father's last name

### Column: father_dob
**ReuseComponent**: @NIEM:date_representation
**Description**: Father's date of birth

### Column: mother_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Mother's first name

### Column: mother_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Mother's maiden name

### Column: mother_dob
**ReuseComponent**: @NIEM:date_representation
**Description**: Mother's date of birth

### Column: spouse_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Spouse's first name (if married)

### Column: spouse_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Spouse's last name

### Column: spouse_dob
**ReuseComponent**: @NIEM:date_representation
**Description**: Spouse's date of birth

### Column: spouse_nationality
**ReuseComponent**: @NIEM:country_code
**Description**: Spouse's nationality

## Sub-Cluster: Security and Background
**Parent**: Visa Application

### Column: convicted_of_crime
**Type**: boolean
**Description**: Whether applicant has been convicted of a crime

### Column: crime_description
**Type**: text
**Description**: Description of crime if applicable

### Column: drug_abuse_or_addiction
**Type**: boolean
**Description**: Whether applicant has history of drug abuse or addiction

### Column: terrorist_activities
**Type**: boolean
**Description**: Whether applicant has engaged in terrorist activities

### Column: human_trafficking
**Type**: boolean
**Description**: Whether applicant has engaged in human trafficking

### Column: money_laundering
**Type**: boolean
**Description**: Whether applicant has engaged in money laundering

### Column: previously_deported
**Type**: boolean
**Description**: Whether applicant was previously deported from U.S.

### Column: deportation_explanation
**Type**: text
**Description**: Explanation if previously deported

### Column: immigration_fraud
**Type**: boolean
**Description**: Whether applicant committed immigration fraud

### Column: overstayed_visa
**Type**: boolean
**Description**: Whether applicant previously overstayed a U.S. visa

## Sub-Cluster: Supporting Documents
**Parent**: Visa Application

### Column: passport_photo_uploaded
**Type**: boolean
**Description**: Whether passport-style photo was uploaded

### Column: financial_documents_provided
**Type**: boolean
**Description**: Whether proof of financial support was provided

### Column: employment_letter_provided
**Type**: boolean
**Description**: Whether employment verification letter was provided

### Column: invitation_letter_provided
**Type**: boolean
**Description**: Whether invitation letter was provided

### Column: travel_itinerary_provided
**Type**: boolean
**Description**: Whether travel itinerary was provided

### Column: additional_documents
**Type**: text
**Description**: List of additional supporting documents provided

## Sub-Cluster: Processing Information
**Parent**: Visa Application

### Column: interview_scheduled
**Type**: boolean
**Description**: Whether interview has been scheduled

### Column: interview_date
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time of visa interview

### Column: interview_location
**Type**: text
**Description**: Location of visa interview
**Examples**: U.S. Embassy London - Consular Section

### Column: biometrics_collected
**Type**: boolean
**Description**: Whether biometrics (fingerprints, photo) were collected

### Column: biometrics_date
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date biometrics were collected

### Column: decision_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Date visa decision was made

### Column: decision
**Type**: text
**Description**: Visa application decision
**Enumeration**:
  - approved: Approved
  - denied: Denied
  - pending: Pending
  - administrative_processing: Administrative Processing
  - withdrawn: Withdrawn by Applicant

### Column: denial_reason
**Type**: text
**Description**: Reason for denial if applicable

### Column: visa_issued_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Date visa was issued

### Column: visa_number
**Type**: identifier
**Description**: Issued visa number

### Column: visa_expiration_date
**ReuseComponent**: @NIEM:date_representation
**Description**: Date visa expires

### Column: number_of_entries
**Type**: text
**Description**: Number of entries permitted
**Enumeration**:
  - single: Single Entry
  - double: Double Entry
  - multiple: Multiple Entry

### Column: notes
**Type**: text
**Description**: Additional notes or comments about application
