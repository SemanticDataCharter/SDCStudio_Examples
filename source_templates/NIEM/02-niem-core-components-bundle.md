---
template_version: "4.0.0"
dataset:
  name: "NIEM Core Components Bundle"
  description: "Bundle of NIEM core reusable components for addresses, person information, organizations, and common structures"
  domain: "Core"
  creator: "NIEM 6.0"
  project: "NIEM"
enrichment:
  enable_llm: false
---

# Dataset Overview

This is a bundle dataset containing NIEM core reusable components. After upload and processing, the individual components will be available for reuse as `@NIEM:ComponentLabel`. This wrapper data model can be deleted after successful upload - the individual components will persist.

**Purpose**: Create reusable core components following NIEM 6.0 nc: (NIEM Core) namespace standards.

**Note**: This is a temporary bundle for efficient upload. Delete this data model after processing completes.

## Root Cluster: NIEM Core Components

### Column: bundle_id
**Type**: xdstring
**Description**: Placeholder identifier for bundle (not reused)

## Sub-Cluster: Person Name
**Parent**: NIEM Core Components

### Column: person_given_name
**Type**: xdstring
**Description**: A first name of a person (NIEM nc:PersonGivenName)
**Examples**: John, Mary, Michael, Sarah

### Column: person_middle_name
**Type**: xdstring
**Description**: A middle name of a person (NIEM nc:PersonMiddleName)
**Examples**: James, Ann, Lee, Elizabeth

### Column: person_surname
**Type**: xdstring
**Description**: A last name or family name of a person (NIEM nc:PersonSurName)
**Examples**: Smith, Johnson, Garcia, Williams

### Column: person_name_suffix
**Type**: xdtoken
**Description**: A name suffix of a person (NIEM nc:PersonNameSuffixText)
**Enumeration**:
  - Jr.: Junior
  - Sr.: Senior
  - II: The Second
  - III: The Third
  - IV: The Fourth
  - V: The Fifth
  - Esq.: Esquire
  - PhD: Doctor of Philosophy
  - MD: Doctor of Medicine
  - DDS: Doctor of Dental Surgery

### Column: person_full_name
**Type**: xdstring
**Description**: A complete name of a person (NIEM nc:PersonFullName)
**Examples**: John Michael Smith Jr., Mary Elizabeth Garcia

## Sub-Cluster: US Address
**Parent**: NIEM Core Components

### Column: location_street_full_text
**Type**: xdstring
**Description**: A complete street address (NIEM nc:LocationStreetFullText)
**Examples**: 123 Main Street, 456 Oak Avenue Apt 2B

### Column: location_street_number
**Type**: xdstring
**Description**: A street number (NIEM nc:LocationStreetNumberText)
**Examples**: 123, 456, 789

### Column: location_street_name
**Type**: xdstring
**Description**: A street name (NIEM nc:LocationStreetName)
**Examples**: Main Street, Oak Avenue, Elm Boulevard

### Column: address_secondary_unit
**Type**: xdstring
**Description**: An apartment, suite, or unit designation (NIEM nc:AddressSecondaryUnitText)
**Examples**: Apt 2B, Suite 100, Unit 5, #12

### Column: location_city_name
**Type**: xdstring
**Description**: A name of a city or town (NIEM nc:LocationCityName)
**Examples**: Springfield, New York, Los Angeles

### Column: location_state_code
**Type**: xdtoken
**Description**: A state, commonwealth, province, or other such geopolitical subdivision of a country
**Enumeration**:
  - AL: Alabama
  - AK: Alaska
  - AZ: Arizona
  - AR: Arkansas
  - CA: California
  - CO: Colorado
  - CT: Connecticut
  - DE: Delaware
  - FL: Florida
  - GA: Georgia
  - HI: Hawaii
  - ID: Idaho
  - IL: Illinois
  - IN: Indiana
  - IA: Iowa
  - KS: Kansas
  - KY: Kentucky
  - LA: Louisiana
  - ME: Maine
  - MD: Maryland
  - MA: Massachusetts
  - MI: Michigan
  - MN: Minnesota
  - MS: Mississippi
  - MO: Missouri
  - MT: Montana
  - NE: Nebraska
  - NV: Nevada
  - NH: New Hampshire
  - NJ: New Jersey
  - NM: New Mexico
  - NY: New York
  - NC: North Carolina
  - ND: North Dakota
  - OH: Ohio
  - OK: Oklahoma
  - OR: Oregon
  - PA: Pennsylvania
  - RI: Rhode Island
  - SC: South Carolina
  - SD: South Dakota
  - TN: Tennessee
  - TX: Texas
  - UT: Utah
  - VT: Vermont
  - VA: Virginia
  - WA: Washington
  - WV: West Virginia
  - WI: Wisconsin
  - WY: Wyoming
  - DC: District of Columbia

### Column: location_postal_code
**Type**: xdstring
**Description**: A ZIP code or postal code (NIEM nc:LocationPostalCode)
**Examples**: 90210, 10001, 60601-1234
**Constraints**:
  - pattern: ^\d{5}(-\d{4})?$

### Column: location_country_code
**Type**: xdtoken
**Description**: A country code (NIEM nc:LocationCountryISO3166Alpha2Code)
**Enumeration**:
  - US: United States
  - CA: Canada
  - MX: Mexico

## Sub-Cluster: Contact Information
**Parent**: NIEM Core Components

### Column: contact_telephone_number
**Type**: xdstring
**Description**: A telephone number (NIEM nc:ContactTelephoneNumber)
**Examples**: 555-1234, (555) 123-4567, +1-555-123-4567
**Constraints**:
  - pattern: ^[\d\s\(\)\-\+\.]+$

### Column: contact_email_id
**Type**: xdstring
**Description**: An email address (NIEM nc:ContactEmailID)
**Examples**: john.smith@example.com, info@company.org

### Column: contact_fax_number
**Type**: xdstring
**Description**: A fax telephone number (NIEM nc:ContactFaxNumber)
**Examples**: 555-9876, (555) 987-6543

### Column: contact_mailing_address
**Type**: xdstring
**Description**: A mailing address (NIEM nc:ContactMailingAddress)

### Column: contact_website_uri
**Type**: xdlink
**Description**: A website URL (NIEM nc:ContactWebsiteURI)
**Examples**: https://www.example.com, http://company.org

## Sub-Cluster: Organization Information
**Parent**: NIEM Core Components

### Column: organization_name
**Type**: xdstring
**Description**: A name of an organization (NIEM nc:OrganizationName)
**Examples**: ABC Corporation, State Police Department, Federal Bureau of Investigation

### Column: organization_abbreviation
**Type**: xdstring
**Description**: An abbreviation or acronym for an organization name (NIEM nc:OrganizationAbbreviationText)
**Examples**: FBI, DOJ, NYPD, ACME

### Column: organization_tax_id
**Type**: xdstring
**Description**: A tax identification number (TIN/EIN) for an organization (NIEM nc:OrganizationTaxIdentification)
**Examples**: 12-3456789, 98-7654321
**Constraints**:
  - pattern: ^\d{2}-\d{7}$

### Column: organization_location
**Type**: xdstring
**Description**: A location of an organization

## Sub-Cluster: Location Coordinates
**Parent**: NIEM Core Components

### Column: location_latitude_degree
**Type**: decimal
**Description**: A latitude degree value (NIEM nc:LocationLatitudeDegreeValue)
**Units**: degrees
**Constraints**:
  - range: [-90, 90]
**Examples**: 40.7128, 34.0522, -33.8688

### Column: location_longitude_degree
**Type**: decimal
**Description**: A longitude degree value (NIEM nc:LocationLongitudeDegreeValue)
**Units**: degrees
**Constraints**:
  - range: [-180, 180]
**Examples**: -74.0060, -118.2437, 151.2093

### Column: location_altitude
**Type**: decimal
**Description**: An altitude or elevation of a location (NIEM nc:LocationAltitudeMeasure)
**Units**: meters
**Examples**: 100, 1500, 2500

## Sub-Cluster: Date and Time
**Parent**: NIEM Core Components

### Column: date_representation
**Type**: xdtemporal
**Description**: A date (NIEM nc:DateRepresentation)
**Examples**: 2024-12-04, 2023-01-15

### Column: datetime_representation
**Type**: xdtemporal
**Description**: A date and time (NIEM nc:DateTime)
**Examples**: 2024-12-04T14:30:00Z, 2023-01-15T09:00:00-05:00

### Column: time_representation
**Type**: xdstring
**Description**: A time (NIEM nc:Time)
**Examples**: 14:30:00, 09:00:00-05:00

### Column: date_range_start
**Type**: xdtemporal
**Description**: A start date of a date range (NIEM nc:StartDate)

### Column: date_range_end
**Type**: xdtemporal
**Description**: An end date of a date range (NIEM nc:EndDate)

## Sub-Cluster: Identification
**Parent**: NIEM Core Components

### Column: identification_id
**Type**: xdstring
**Description**: A value that identifies something (NIEM nc:IdentificationID)
**Examples**: AB123456, 987654321, UUID-1234-5678

### Column: identification_category
**Type**: xdstring
**Description**: A kind of identification (NIEM nc:IdentificationCategoryText)
**Examples**: Driver License, Passport, Social Security Number

### Column: identification_expiration_date
**Type**: xdtemporal
**Description**: A date after which an identification is no longer valid (NIEM nc:IdentificationExpirationDate)

### Column: identification_issuer
**Type**: xdstring
**Description**: An organization that issued an identification (NIEM nc:IdentificationSourceText)
**Examples**: California DMV, U.S. Department of State

## Sub-Cluster: Vehicle Information
**Parent**: NIEM Core Components

### Column: vehicle_identification_number
**Type**: xdstring
**Description**: A vehicle identification number (VIN) (NIEM nc:VehicleIdentification)
**Examples**: 1HGBH41JXMN109186
**Constraints**:
  - pattern: ^[A-HJ-NPR-Z0-9]{17}$

### Column: vehicle_make_name
**Type**: xdstring
**Description**: A manufacturer of a vehicle (NIEM nc:VehicleMakeName)
**Examples**: Ford, Toyota, Honda, Chevrolet

### Column: vehicle_model_name
**Type**: xdstring
**Description**: A model of a vehicle (NIEM nc:VehicleModelName)
**Examples**: F-150, Camry, Civic, Silverado

### Column: vehicle_year
**Type**: integer
**Description**: A year of a vehicle (NIEM nc:VehicleModelYearDate)
**Examples**: 2024, 2023, 2020
**Constraints**:
  - range: [1900, 2100]

### Column: vehicle_color_primary
**Type**: xdstring
**Description**: A primary color of a vehicle (NIEM nc:VehicleColorPrimaryText)
**Examples**: Black, White, Silver, Red, Blue

### Column: vehicle_license_plate_number
**Type**: xdstring
**Description**: A license plate or registration number (NIEM nc:VehicleLicensePlateID)
**Examples**: ABC 1234, 123-XYZ, FL-AB12CD

## Sub-Cluster: Physical Description
**Parent**: NIEM Core Components

### Column: person_height
**Type**: decimal
**Description**: A height of a person (NIEM nc:PersonHeightMeasure)
**Units**: centimeters
**Examples**: 175, 180, 165
**Constraints**:
  - range: [50, 250]

### Column: person_weight
**Type**: decimal
**Description**: A weight of a person (NIEM nc:PersonWeightMeasure)
**Units**: kilograms
**Examples**: 70, 80, 65
**Constraints**:
  - range: [20, 300]

### Column: person_eye_color
**Type**: xdtoken
**Description**: An eye color of a person (NIEM nc:PersonEyeColorCode)
**Enumeration**:
  - BLK: Black
  - BLU: Blue
  - BRO: Brown
  - GRY: Gray
  - GRN: Green
  - HAZ: Hazel
  - XXX: Unknown

### Column: person_hair_color
**Type**: xdtoken
**Description**: A hair color of a person (NIEM nc:PersonHairColorCode)
**Enumeration**:
  - BAL: Bald
  - BLK: Black
  - BLN: Blond
  - BRO: Brown
  - GRY: Gray
  - RED: Red
  - WHI: White
  - XXX: Unknown

### Column: person_race
**Type**: xdtoken
**Description**: A race of a person (NIEM nc:PersonRaceCode)
**Enumeration**:
  - white: White
  - black: Black or African American
  - asian: Asian
  - native_american: American Indian or Alaska Native
  - pacific_islander: Native Hawaiian or Other Pacific Islander
  - other: Other

### Column: person_sex
**Type**: xdtoken
**Description**: A gender or sex of a person (NIEM nc:PersonSexCode)
**Enumeration**:
  - M: Male
  - F: Female
  - U: Unknown
  - X: Non-binary/Other

## Sub-Cluster: Monetary Amount
**Parent**: NIEM Core Components

### Column: amount_value
**Type**: decimal
**Description**: A monetary amount (NIEM nc:Amount)
**Units**: currency
**Examples**: 100.00, 1500.50, 25.99

### Column: currency_code
**Type**: xdtoken
**Description**: A currency code (NIEM nc:CurrencyCode)
**Enumeration**:
  - USD: United States Dollar
  - EUR: Euro
  - GBP: British Pound Sterling
  - JPY: Japanese Yen
  - CAD: Canadian Dollar
  - AUD: Australian Dollar
  - CNY: Chinese Yuan
  - MXN: Mexican Peso

## Sub-Cluster: Case Information
**Parent**: NIEM Core Components

### Column: case_tracking_id
**Type**: xdstring
**Description**: A case tracking identifier (NIEM nc:CaseTrackingID)
**Examples**: 2024-CR-001234, CV-2023-5678

### Column: case_title
**Type**: xdstring
**Description**: A title or name of a case (NIEM nc:CaseTitleText)
**Examples**: State v. Smith, Jones v. ABC Corporation

### Column: case_file_date
**Type**: xdtemporal
**Description**: A date a case was filed (NIEM nc:CaseFiledDate)

### Column: case_status
**Type**: xdtoken
**Description**: A status of a case
**Enumeration**:
  - open: Open
  - closed: Closed
  - pending: Pending
  - suspended: Suspended

## Sub-Cluster: Arrest Information
**Parent**: NIEM Core Components

### Column: arrest_date
**Type**: xdtemporal
**Description**: A date of an arrest (NIEM j:ArrestDate)

### Column: arrest_location
**Type**: xdstring
**Description**: A location where an arrest occurred (NIEM j:ArrestLocation)

### Column: arrest_agency
**Type**: xdstring
**Description**: An agency that made an arrest (NIEM j:ArrestAgency)

## Sub-Cluster: Charge Information
**Parent**: NIEM Core Components

### Column: charge_statute
**Type**: xdstring
**Description**: A statute or ordinance that was violated (NIEM j:ChargeStatute)
**Examples**: PC 245(a)(1), 18 USC 1001, VC 23152(a)

### Column: charge_description
**Type**: xdstring
**Description**: A description of a charge (NIEM j:ChargeDescriptionText)
**Examples**: Assault with a Deadly Weapon, False Statements, Driving Under the Influence

### Column: charge_severity
**Type**: xdtoken
**Description**: A severity level of a charge
**Enumeration**:
  - felony: Felony
  - misdemeanor: Misdemeanor
  - infraction: Infraction

### Column: charge_filing_date
**Type**: xdtemporal
**Description**: A date a charge was filed (NIEM j:ChargeFilingDate)

## Sub-Cluster: Incident Information
**Parent**: NIEM Core Components

### Column: incident_date
**Type**: xdtemporal
**Description**: A date and time an incident occurred (NIEM j:IncidentDate)

### Column: incident_location
**Type**: xdstring
**Description**: A location where an incident occurred (NIEM nc:Location)

### Column: incident_category
**Type**: xdtoken
**Description**: A category of an incident (NIEM j:IncidentCategoryCode)
**Enumeration**:
  - accident: Accident
  - assault: Assault
  - burglary: Burglary
  - robbery: Robbery
  - theft: Theft
  - vandalism: Vandalism
  - other: Other

### Column: incident_report_number
**Type**: xdstring
**Description**: A report number for an incident (NIEM j:IncidentReportNumber)
**Examples**: 2024-001234, IR-2023-5678
