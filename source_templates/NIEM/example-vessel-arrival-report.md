---
template_version: "4.0.0"
dataset:
  name: "Vessel Arrival Report"
  description: "Maritime vessel arrival notification capturing ship details, cargo, crew, voyage information, and port entry requirements"
  domain: "Maritime"
  creator: "NIEM 6.0"
  project: "NIEM"
enrichment:
  enable_llm: true
---

# Dataset Overview

Comprehensive vessel arrival report for port entry notification, following NIEM Maritime domain (m:) standards. Documents vessel identification, voyage information, crew manifest, cargo manifest, and regulatory compliance.

**Purpose**: Notify port authorities of incoming vessel arrival for customs clearance, security screening, port operations coordination, and regulatory compliance.

**Business Context**: Used by port authorities, U.S. Coast Guard, U.S. Customs and Border Protection (CBP), harbormaster offices, and shipping agents. Integrates with AIS (Automatic Identification System), port management systems, cargo tracking, and customs clearance systems.

**Standards Alignment**:
- NIEM Maritime Domain (m:) v6.0
- NIEM Core (nc:) v6.0
- IMO (International Maritime Organization) standards
- U.S. Coast Guard ANOA (Advance Notice of Arrival) requirements
- CBP ACE (Automated Commercial Environment) integration

## Root Cluster: Vessel Arrival Report

### Column: arrival_report_number
**Type**: identifier
**Description**: Unique identifier for this arrival report
**Examples**: VAR-2024-001234, ANOA-2024-567890
**Constraints**:
  - required: true
  - pattern: ^[A-Z]{3,5}-\d{4}-\d{6}$

### Column: report_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time this report was filed

### Column: eta_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Estimated Time of Arrival at port

### Column: eta_updated_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time ETA was last updated

### Column: port_of_arrival_name
**Type**: text
**Description**: Name of port where vessel will arrive
**Examples**: Port of Los Angeles, Port of New York/New Jersey, Port of Houston

### Column: port_of_arrival_code
**Type**: identifier
**Description**: UN/LOCODE or port identifier code
**Examples**: USLAX, USNYC, USHOU, USMIA
**Constraints**:
  - pattern: ^[A-Z]{2}[A-Z0-9]{3}$

### Column: port_country
**ReuseComponent**: @NIEM:country_code
**Description**: Country where port is located

### Column: berth_assignment
**Type**: text
**Description**: Assigned berth or dock
**Examples**: Berth 100, Dock 5, Terminal 3 Berth A

### Column: pilot_required
**Type**: boolean
**Description**: Whether pilot service is required for entry

### Column: tug_assistance_required
**Type**: boolean
**Description**: Whether tug assistance is required

## Sub-Cluster: Vessel Information
**Parent**: Vessel Arrival Report

### Column: vessel_name
**Type**: text
**Description**: Name of vessel
**Examples**: Ever Given, MSC Gülsün, Emma Maersk

### Column: vessel_imo_number
**Type**: identifier
**Description**: International Maritime Organization (IMO) number
**Examples**: IMO 9811000, IMO 9454436
**Constraints**:
  - pattern: ^IMO\s?\d{7}$

### Column: vessel_mmsi
**Type**: identifier
**Description**: Maritime Mobile Service Identity (MMSI) number
**Examples**: 366123456, 244567890
**Constraints**:
  - pattern: ^\d{9}$

### Column: vessel_call_sign
**Type**: identifier
**Description**: Vessel radio call sign
**Examples**: WKYZ, ABCD1, 9V1234

### Column: vessel_type
**ReuseComponent**: @NIEM:vehicle_type_code
**Description**: Type or category of vessel
**Note**: Uses vehicle_type_code but vessel-specific values below
**Enumeration**:
  - container_ship: Container Ship
  - bulk_carrier: Bulk Carrier
  - tanker: Tanker (Oil/Chemical)
  - ro_ro: Roll-on/Roll-off (Vehicle Carrier)
  - cruise_ship: Cruise Ship
  - ferry: Ferry
  - cargo_general: General Cargo Ship
  - fishing_vessel: Fishing Vessel
  - tug: Tug Boat
  - barge: Barge
  - yacht: Yacht/Pleasure Craft
  - naval: Naval Vessel

### Column: vessel_flag_country
**ReuseComponent**: @NIEM:country_code
**Description**: Country of vessel registration (flag state)

### Column: vessel_gross_tonnage
**Type**: decimal
**Description**: Gross tonnage (GT) of vessel
**Units**: metric tons
**Examples**: 1200, 50000, 220000

### Column: vessel_net_tonnage
**Type**: decimal
**Description**: Net tonnage (NT) of vessel
**Units**: metric tons

### Column: vessel_length
**Type**: decimal
**Description**: Overall length of vessel
**Units**: meters
**Examples**: 50.5, 200, 400

### Column: vessel_beam
**Type**: decimal
**Description**: Beam (width) of vessel
**Units**: meters
**Examples**: 10, 32.3, 59

### Column: vessel_draft
**Type**: decimal
**Description**: Draft (depth below waterline) of vessel
**Units**: meters
**Examples**: 5.5, 10.2, 16

### Column: vessel_year_built
**Type**: integer
**Description**: Year vessel was built
**Constraints**:
  - range: [1900, 2100]

## Sub-Cluster: Vessel Owner/Operator
**Parent**: Vessel Arrival Report

### Column: vessel_owner
**ReuseComponent**: @NIEM:organization_name
**Description**: Vessel owner company name
**Examples**: Maersk Line, MSC Mediterranean Shipping Company

### Column: vessel_operator
**ReuseComponent**: @NIEM:organization_name
**Description**: Vessel operator company name

### Column: operator_address_street
**ReuseComponent**: @NIEM:location_street_full_text
**Description**: Operator street address

### Column: operator_address_city
**ReuseComponent**: @NIEM:location_city_name
**Description**: Operator city

### Column: operator_address_country
**ReuseComponent**: @NIEM:country_code
**Description**: Operator country

### Column: operator_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Operator telephone number

### Column: operator_email
**ReuseComponent**: @NIEM:contact_email_id
**Description**: Operator email address

### Column: local_agent_name
**ReuseComponent**: @NIEM:organization_name
**Description**: Local shipping agent/representative at port

### Column: local_agent_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Local agent telephone number

### Column: local_agent_email
**ReuseComponent**: @NIEM:contact_email_id
**Description**: Local agent email address

## Sub-Cluster: Voyage Information
**Parent**: Vessel Arrival Report

### Column: voyage_number
**Type**: identifier
**Description**: Voyage or trip identifier
**Examples**: VOY-2024-1234, V123W

### Column: port_of_departure
**Type**: text
**Description**: Last port of departure
**Examples**: Shanghai, Singapore, Rotterdam

### Column: port_of_departure_code
**Type**: identifier
**Description**: UN/LOCODE of departure port
**Examples**: CNSHA, SGSIN, NLRTM

### Column: departure_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time of departure from last port

### Column: next_port_of_call
**Type**: text
**Description**: Next port after this arrival

### Column: next_port_code
**Type**: identifier
**Description**: UN/LOCODE of next port

### Column: final_destination_port
**Type**: text
**Description**: Final destination port of voyage

### Column: ports_of_call
**Type**: text
**Description**: Comma-separated list of all ports on this voyage
**Examples**: Shanghai, Hong Kong, Singapore, Los Angeles

### Column: purpose_of_call
**Type**: text
**Description**: Purpose of port call
**Enumeration**:
  - load_cargo: Load Cargo
  - discharge_cargo: Discharge Cargo
  - load_discharge: Load and Discharge Cargo
  - refuel: Refueling/Bunkering
  - provisions: Provisions/Supplies
  - repairs: Repairs/Maintenance
  - crew_change: Crew Change
  - emergency: Emergency
  - other: Other

## Sub-Cluster: Captain Information
**Parent**: Vessel Arrival Report

### Column: captain_first_name
**ReuseComponent**: @NIEM:person_given_name
**Description**: Captain's first name

### Column: captain_last_name
**ReuseComponent**: @NIEM:person_surname
**Description**: Captain's last name

### Column: captain_nationality
**ReuseComponent**: @NIEM:country_code
**Description**: Captain's nationality

### Column: captain_phone
**ReuseComponent**: @NIEM:contact_telephone_number
**Description**: Captain's contact phone (satellite phone)

### Column: captain_email
**ReuseComponent**: @NIEM:contact_email_id
**Description**: Captain's email address

## Sub-Cluster: Crew Manifest Summary
**Parent**: Vessel Arrival Report

### Column: total_crew_count
**Type**: integer
**Description**: Total number of crew members on board
**Constraints**:
  - range: [1, 500]

### Column: officers_count
**Type**: integer
**Description**: Number of officers
**Constraints**:
  - range: [0, 50]

### Column: crew_count
**Type**: integer
**Description**: Number of non-officer crew
**Constraints**:
  - range: [0, 450]

### Column: crew_nationalities
**Type**: text
**Description**: Comma-separated list of crew nationalities
**Examples**: Philippines, India, Ukraine, Poland

### Column: crew_list_attached
**Type**: boolean
**Description**: Whether complete crew manifest is attached

## Sub-Cluster: Passenger Information
**Parent**: Vessel Arrival Report

### Column: passengers_on_board
**Type**: boolean
**Description**: Whether vessel is carrying passengers

### Column: total_passenger_count
**Type**: integer
**Description**: Total number of passengers
**Constraints**:
  - range: [0, 10000]

### Column: passenger_list_attached
**Type**: boolean
**Description**: Whether passenger manifest is attached

## Sub-Cluster: Cargo Summary
**Parent**: Vessel Arrival Report

### Column: cargo_on_board
**Type**: boolean
**Description**: Whether vessel is carrying cargo

### Column: total_cargo_weight
**Type**: decimal
**Description**: Total weight of cargo
**Units**: metric tons

### Column: total_teu_containers
**Type**: integer
**Description**: Total Twenty-foot Equivalent Units (TEU) if container ship
**Constraints**:
  - range: [0, 25000]

### Column: cargo_type
**Type**: text
**Description**: Primary type of cargo
**Enumeration**:
  - containers: Containerized Cargo
  - bulk_dry: Dry Bulk (grain, coal, ore)
  - bulk_liquid: Liquid Bulk (oil, chemicals)
  - vehicles: Vehicles
  - general_cargo: General/Breakbulk Cargo
  - refrigerated: Refrigerated Cargo
  - livestock: Livestock
  - none: No Cargo

### Column: hazardous_cargo
**Type**: boolean
**Description**: Whether vessel is carrying hazardous materials

### Column: hazmat_class
**Type**: text
**Description**: Hazardous material classes on board (if applicable)
**Examples**: Class 1 Explosives, Class 3 Flammable Liquids, Class 8 Corrosives

### Column: cargo_manifest_attached
**Type**: boolean
**Description**: Whether detailed cargo manifest is attached

## Sub-Cluster: Customs and Immigration
**Parent**: Vessel Arrival Report

### Column: customs_declaration_filed
**Type**: boolean
**Description**: Whether customs declaration has been filed

### Column: customs_reference_number
**Type**: identifier
**Description**: Customs filing reference number

### Column: crew_visa_required
**Type**: boolean
**Description**: Whether crew members require visas for shore leave

### Column: crew_shore_leave_requested
**Type**: boolean
**Description**: Whether crew shore leave is requested

### Column: immigration_inspection_required
**Type**: boolean
**Description**: Whether immigration inspection is required

## Sub-Cluster: Health and Security
**Parent**: Vessel Arrival Report

### Column: maritime_declaration_of_health
**Type**: boolean
**Description**: Whether Maritime Declaration of Health is required/filed

### Column: illness_on_board
**Type**: boolean
**Description**: Whether there are ill persons on board

### Column: illness_description
**Type**: text
**Description**: Description of illness if applicable

### Column: death_on_board
**Type**: boolean
**Description**: Whether there were deaths during voyage

### Column: medical_assistance_required
**Type**: boolean
**Description**: Whether medical assistance is needed upon arrival

### Column: security_level
**ReuseComponent**: @NIEM:severity_level
**Description**: ISPS (International Ship and Port Facility Security) Code level
**Note**: Uses severity_level as proxy for security levels

### Column: last_10_ports
**Type**: text
**Description**: Last 10 ports visited in past 180 days
**Examples**: Shanghai, Hong Kong, Singapore, Colombo, Suez

### Column: stowaway_on_board
**Type**: boolean
**Description**: Whether stowaways are on board

### Column: security_incident_during_voyage
**Type**: boolean
**Description**: Whether security incident occurred during voyage

### Column: security_incident_description
**Type**: text
**Description**: Description of security incident if applicable

## Sub-Cluster: Environmental Compliance
**Parent**: Vessel Arrival Report

### Column: ballast_water_management_plan
**Type**: boolean
**Description**: Whether vessel has Ballast Water Management Plan

### Column: ballast_water_exchange_required
**Type**: boolean
**Description**: Whether ballast water exchange was performed

### Column: waste_discharge_required
**Type**: boolean
**Description**: Whether waste discharge at port is required

### Column: waste_type
**Type**: text
**Description**: Types of waste to be discharged
**Examples**: Sewage, Garbage, Oil residues, Bilge water

### Column: fuel_type
**Type**: text
**Description**: Type of fuel being used
**Enumeration**:
  - hfo: Heavy Fuel Oil
  - mgo: Marine Gas Oil
  - mdo: Marine Diesel Oil
  - lng: Liquefied Natural Gas
  - methanol: Methanol
  - other: Other

### Column: sulfur_content_compliant
**Type**: boolean
**Description**: Whether fuel sulfur content meets regulatory requirements

## Sub-Cluster: Certificates and Documentation
**Parent**: Vessel Arrival Report

### Column: vessel_certificate_of_registry
**Type**: boolean
**Description**: Certificate of Registry valid

### Column: international_tonnage_certificate
**Type**: boolean
**Description**: International Tonnage Certificate valid

### Column: safety_equipment_certificate
**Type**: boolean
**Description**: Safety Equipment Certificate valid

### Column: load_line_certificate
**Type**: boolean
**Description**: Load Line Certificate valid

### Column: insurance_certificate
**Type**: boolean
**Description**: Protection and Indemnity (P&I) insurance certificate valid

### Column: certificate_expiration_warnings
**Type**: text
**Description**: List of certificates that are expired or expiring soon

## Sub-Cluster: Port Services Required
**Parent**: Vessel Arrival Report

### Column: pilotage_required
**Type**: boolean
**Description**: Pilot service required

### Column: tug_required
**Type**: boolean
**Description**: Tug assistance required

### Column: number_of_tugs
**Type**: integer
**Description**: Number of tugs requested
**Constraints**:
  - range: [0, 10]

### Column: mooring_service_required
**Type**: boolean
**Description**: Mooring service required

### Column: stevedore_service_required
**Type**: boolean
**Description**: Stevedore (cargo handling) service required

### Column: bunkering_required
**Type**: boolean
**Description**: Fuel bunkering required

### Column: provisions_required
**Type**: boolean
**Description**: Provisions/supplies required

### Column: repairs_required
**Type**: boolean
**Description**: Repairs or maintenance required

### Column: waste_removal_required
**Type**: boolean
**Description**: Waste removal service required

## Sub-Cluster: Processing Status
**Parent**: Vessel Arrival Report

### Column: arrival_approved
**Type**: boolean
**Description**: Whether arrival has been approved by port authority

### Column: approval_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Date and time arrival was approved

### Column: approved_by
**Type**: text
**Description**: Name or identifier of approving authority

### Column: conditions_or_restrictions
**Type**: text
**Description**: Any conditions or restrictions on arrival/berthing

### Column: actual_arrival_date_time
**ReuseComponent**: @NIEM:datetime_representation
**Description**: Actual date and time of arrival (once occurred)

### Column: actual_berth_assignment
**Type**: text
**Description**: Actual berth assigned (may differ from request)

### Column: notes
**Type**: text
**Description**: Additional notes or comments about arrival
