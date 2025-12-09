---
template_version: "4.0.0"
dataset:
  name: "NIEM Code Lists Bundle"
  description: "Bundle of NIEM standard code lists for reuse across domains"
  domain: "Core"
  creator: "NIEM 6.0"
  project: "NIEM"
enrichment:
  enable_llm: false
---

# Dataset Overview

This is a bundle dataset containing NIEM standard code lists. After upload and processing, the individual code list components will be available for reuse as `@NIEM:ComponentLabel`. This wrapper data model can be deleted after successful upload - the individual code list components will persist.

**Purpose**: Create reusable enumerated code lists following NIEM 6.0 standards.

**Note**: This is a temporary bundle for efficient upload. Delete this data model after processing completes.

## Root Cluster: NIEM Code Lists

### Column: state_code
**Type**: xdtoken
**Description**: Two-letter US state and territory postal abbreviations per USPS Publication 28
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
  - AS: American Samoa
  - GU: Guam
  - MP: Northern Mariana Islands
  - PR: Puerto Rico
  - VI: Virgin Islands

### Column: country_code
**Type**: xdtoken
**Description**: ISO 3166-1 alpha-2 country codes
**Enumeration**:
  - US: United States
  - CA: Canada
  - MX: Mexico
  - GB: United Kingdom
  - FR: France
  - DE: Germany
  - IT: Italy
  - ES: Spain
  - JP: Japan
  - CN: China
  - IN: India
  - BR: Brazil
  - AU: Australia
  - RU: Russia
  - KR: South Korea
  - SA: Saudi Arabia
  - AE: United Arab Emirates
  - IL: Israel
  - TR: Turkey
  - EG: Egypt
  - ZA: South Africa
  - NG: Nigeria
  - AR: Argentina
  - CL: Chile
  - CO: Colombia
  - PE: Peru
  - PH: Philippines
  - TH: Thailand
  - VN: Vietnam
  - ID: Indonesia
  - MY: Malaysia
  - SG: Singapore
  - NZ: New Zealand
  - PK: Pakistan
  - BD: Bangladesh
  - AF: Afghanistan
  - IQ: Iraq
  - IR: Iran
  - SY: Syria
  - YE: Yemen
  - JO: Jordan
  - LB: Lebanon

### Column: severity_level
**Type**: xdtoken
**Description**: Standard severity level classifications for incidents, threats, and emergencies
**Enumeration**:
  - low: Low - Minimal impact, routine handling
  - moderate: Moderate - Some impact, standard response
  - high: High - Significant impact, priority response
  - critical: Critical - Severe impact, immediate response
  - extreme: Extreme - Catastrophic impact, maximum response

### Column: status_code
**Type**: xdtoken
**Description**: Standard status codes for records, cases, and processes
**Enumeration**:
  - active: Active - Currently in effect
  - inactive: Inactive - No longer in effect
  - pending: Pending - Awaiting action or approval
  - completed: Completed - Finished successfully
  - cancelled: Cancelled - Terminated before completion
  - suspended: Suspended - Temporarily halted
  - expired: Expired - No longer valid due to time limit

### Column: gender_code
**Type**: xdtoken
**Description**: Gender classifications per NIEM nc:PersonSexCode
**Enumeration**:
  - M: Male
  - F: Female
  - U: Unknown
  - X: Non-binary/Other

### Column: contact_method_type
**Type**: xdtoken
**Description**: Types of contact methods for communication
**Enumeration**:
  - phone: Telephone
  - mobile: Mobile Phone
  - email: Email
  - fax: Fax
  - mail: Postal Mail
  - sms: SMS Text Message
  - in_person: In Person

### Column: address_category_code
**Type**: xdtoken
**Description**: Categories of addresses per NIEM nc:AddressCategoryCode
**Enumeration**:
  - residential: Residential - Home address
  - business: Business - Work/office address
  - mailing: Mailing - Postal delivery address
  - temporary: Temporary - Short-term address
  - delivery: Delivery - Package/goods delivery address

### Column: identification_category_code
**Type**: xdtoken
**Description**: Categories of identification documents
**Enumeration**:
  - drivers_license: Driver's License
  - state_id: State-Issued ID Card
  - passport: Passport
  - military_id: Military ID
  - ssn: Social Security Number
  - ein: Employer Identification Number
  - tribal_id: Tribal ID
  - birth_certificate: Birth Certificate
  - visa: Visa
  - green_card: Permanent Resident Card

### Column: incident_category_code
**Type**: xdtoken
**Description**: Categories of incidents per NIEM j:IncidentCategoryCode
**Enumeration**:
  - accident: Accident - Unintentional incident
  - assault: Assault - Physical attack
  - burglary: Burglary - Unlawful entry
  - robbery: Robbery - Theft with force or threat
  - theft: Theft - Taking property without force
  - vandalism: Vandalism - Property damage
  - fraud: Fraud - Deception for financial gain
  - drug_offense: Drug Offense - Narcotics violation
  - dui: DUI/DWI - Impaired driving
  - domestic_violence: Domestic Violence
  - harassment: Harassment
  - missing_person: Missing Person
  - suspicious_activity: Suspicious Activity
  - traffic: Traffic Incident
  - fire: Fire
  - medical: Medical Emergency
  - other: Other

### Column: charge_severity_level
**Type**: xdtoken
**Description**: Severity levels for criminal charges per NIEM j:ChargeSeverityLevel
**Enumeration**:
  - felony: Felony - Most serious crimes
  - misdemeanor: Misdemeanor - Less serious crimes
  - infraction: Infraction - Minor violations
  - violation: Violation - Civil/administrative violations

### Column: vehicle_type_code
**Type**: xdtoken
**Description**: Types of vehicles per NIEM nc:VehicleCategoryCode
**Enumeration**:
  - automobile: Automobile/Car
  - truck: Truck
  - motorcycle: Motorcycle
  - bus: Bus
  - van: Van
  - suv: SUV
  - trailer: Trailer
  - rv: Recreational Vehicle
  - atv: All-Terrain Vehicle
  - boat: Boat
  - aircraft: Aircraft

### Column: weapon_category_code
**Type**: xdtoken
**Description**: Categories of weapons per NIEM j:WeaponCategoryCode
**Enumeration**:
  - firearm_handgun: Firearm - Handgun
  - firearm_rifle: Firearm - Rifle
  - firearm_shotgun: Firearm - Shotgun
  - knife: Knife/Cutting Instrument
  - club: Club/Blunt Object
  - explosive: Explosive Device
  - chemical: Chemical Agent
  - vehicle: Vehicle (as weapon)
  - hands_feet: Personal Weapons (hands, feet)
  - other: Other Weapon

### Column: case_status_code
**Type**: xdtoken
**Description**: Status codes for cases and investigations
**Enumeration**:
  - open: Open - Active investigation
  - closed_cleared: Closed - Cleared by Arrest
  - closed_exceptional: Closed - Exceptional Clearance
  - closed_unfounded: Closed - Unfounded
  - suspended: Suspended - Investigation suspended
  - reopened: Reopened - Previously closed, now reopened

### Column: custody_status_code
**Type**: xdtoken
**Description**: Custody status for persons in criminal justice system
**Enumeration**:
  - in_custody: In Custody
  - released_own: Released on Own Recognizance
  - released_bail: Released on Bail
  - released_bond: Released on Bond
  - escaped: Escaped
  - transferred: Transferred to Another Facility

### Column: disposition_code
**Type**: xdtoken
**Description**: Case disposition codes
**Enumeration**:
  - guilty: Guilty - Convicted
  - not_guilty: Not Guilty - Acquitted
  - dismissed: Dismissed
  - no_contest: No Contest/Nolo Contendere
  - deferred: Deferred Adjudication
  - pending: Pending - Awaiting disposition

### Column: relationship_code
**Type**: xdtoken
**Description**: Relationship types between persons per NIEM nc:PersonRelationshipCode
**Enumeration**:
  - spouse: Spouse
  - parent: Parent
  - child: Child
  - sibling: Sibling
  - grandparent: Grandparent
  - grandchild: Grandchild
  - aunt_uncle: Aunt/Uncle
  - cousin: Cousin
  - friend: Friend
  - acquaintance: Acquaintance
  - coworker: Coworker
  - neighbor: Neighbor
  - other: Other

### Column: ethnicity_code
**Type**: xdtoken
**Description**: Ethnicity classifications per NIEM nc:PersonEthnicityCode
**Enumeration**:
  - hispanic: Hispanic or Latino
  - not_hispanic: Not Hispanic or Latino
  - unknown: Unknown

### Column: race_code
**Type**: xdtoken
**Description**: Race classifications per NIEM nc:PersonRaceCode
**Enumeration**:
  - white: White
  - black: Black or African American
  - asian: Asian
  - native_american: American Indian or Alaska Native
  - pacific_islander: Native Hawaiian or Other Pacific Islander
  - other: Other
  - unknown: Unknown

### Column: eye_color_code
**Type**: xdtoken
**Description**: Eye color codes per NIEM nc:PersonEyeColorCode
**Enumeration**:
  - BLK: Black
  - BLU: Blue
  - BRO: Brown
  - GRY: Gray
  - GRN: Green
  - HAZ: Hazel
  - MAR: Maroon
  - PNK: Pink
  - XXX: Unknown

### Column: hair_color_code
**Type**: xdtoken
**Description**: Hair color codes per NIEM nc:PersonHairColorCode
**Enumeration**:
  - BAL: Bald
  - BLK: Black
  - BLN: Blond or Strawberry
  - BLU: Blue
  - BRO: Brown
  - GRY: Gray or Partially Gray
  - GRN: Green
  - ONG: Orange
  - PNK: Pink
  - PLE: Purple
  - RED: Red or Auburn
  - SDY: Sandy
  - WHI: White
  - XXX: Unknown

### Column: language_code
**Type**: xdtoken
**Description**: ISO 639-1 language codes
**Enumeration**:
  - en: English
  - es: Spanish
  - fr: French
  - de: German
  - zh: Chinese
  - ja: Japanese
  - ar: Arabic
  - ru: Russian
  - pt: Portuguese
  - hi: Hindi
  - ko: Korean
  - it: Italian
  - vi: Vietnamese
  - tl: Tagalog
  - pl: Polish
  - ur: Urdu
  - fa: Persian
  - uk: Ukrainian
  - ro: Romanian
  - nl: Dutch
