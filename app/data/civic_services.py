"""
Comprehensive Guide to Civic, Municipal and Citizen Registration Services in India
Covers: Birth/Death Certificates, Domicile, Income, Parivahan (DL/RC), Ration Card, Property Tax
"""

CIVIC_SERVICES_DATA = [
    {
        "id": "birth-death-registration",
        "category_title": "Birth & Death Registration",
        "icon": "file-badge",
        "statutory_act": "Registration of Births and Deaths (RBD) Act, 1969 & RBD (Amendment) Act, 2023",
        "issuing_portal": "Civil Registration System (CRS) / Municipal Corporation Portals",
        "official_url": "https://crsorgi.gov.in",
        "overview": "Registration of every birth and death is legally mandatory in India. Under the 2023 Amendment Act, the digital Birth Certificate serves as single conclusive proof of date and place of birth for school admission, voter enrollment, passport, marriage registration, and government jobs.",
        "time_limits_and_rules": [
            "Within 21 Days: Free of cost registration. Handled directly by hospital/nursing home for institutional events or Gram Panchayat/Municipal registrar for home events.",
            "21 to 30 Days: Registered with permission of Registrar upon payment of late fee (₹2).",
            "30 Days to 1 Year: Requires written permission of District Registrar (SDM/Tehsildar) and late fee (₹5) with affidavit.",
            "After 1 Year: Requires order from First Class Magistrate / Sub-Divisional Magistrate (SDM) through delayed registration petition."
        ],
        "documents_required": [
            "Proof of birth/death letter issued by hospital or medical attendant",
            "Aadhaar card / Identity proof of parents (for birth) or deceased & informant (for death)",
            "Marriage certificate of parents (optional/supporting)",
            "Address proof of informant / parent",
            "Non-Availability Certificate (NAC) if registering after 1 year"
        ],
        "application_steps": [
            "Institutional births/deaths are reported directly by hospital authorities on the CRS portal (crsorgi.gov.in) or municipal portal.",
            "For home births/deaths, informant logs in to crsorgi.gov.in or visits local Registrar (Gram Sevak in villages / Health Officer in Municipalities).",
            "Fill in date, time, exact place of occurrence, parents' details, and informant declaration.",
            "Submit and receive Registration Number.",
            "Download QR-code verified digital Birth / Death Certificate from the portal or DigiLocker."
        ]
    },
    {
        "id": "domicile-residence-certificate",
        "category_title": "Domicile / Residence Certificate (मूल निवास प्रमाण पत्र)",
        "icon": "home",
        "statutory_act": "State Revenue Codes / Citizen Charters",
        "issuing_portal": "State e-District / Citizen Service Portals",
        "official_url": "https://serviceonline.gov.in",
        "overview": "A Domicile or Permanent Residence Certificate proves that a person is a bona fide resident of a particular state or union territory. It is mandatory for state quota admissions in engineering/medical colleges, state government recruitments, and state welfare subsidies.",
        "time_limits_and_rules": [
            "Residency Requirement: Continuous residence in the state for 5 to 15 years (varies per state, e.g., 3 years in UP, 15 years in Maharashtra/Karnataka) OR proof that parents are permanent residents.",
            "Validity: Lifetime (permanent resident) unless the individual relocates permanently or takes domicile of another state.",
            "Processing Time: Typically 7 to 15 working days."
        ],
        "documents_required": [
            "Proof of continuous residence (School leaving certificates, electricity bills for consecutive years, land/house ownership deed)",
            "Aadhaar Card / Voter ID Card / Passport",
            "Parents' Domicile / Voter ID / Land Records",
            "Self-declaration / Affidavit stating period of continuous residence and non-possession of domicile of another state",
            "Passport-size photo"
        ],
        "application_steps": [
            "Login to respective state e-District portal (e.g. eDistrict UP, Aaple Sarkar, Seva Sindhu, RTPS Bihar).",
            "Select 'Revenue Department' -> 'Domicile / Residence Certificate'.",
            "Fill applicant details, years of continuous stay, school education details, and local address.",
            "Upload residence proof documents and affidavit.",
            "Pay fee (₹15 - ₹30) and download acknowledgment receipt.",
            "Field inquiry is done by Area Lekhpal/Patwari/Revenue Inspector.",
            "Tehsildar approves and issues digitally signed certificate."
        ]
    },
    {
        "id": "income-certificate",
        "category_title": "Income Certificate (आय प्रमाण पत्र)",
        "icon": "indian-rupee",
        "statutory_act": "State Revenue & Public Services Delivery Acts",
        "issuing_portal": "State e-District / Service Plus Portals",
        "official_url": "https://serviceonline.gov.in",
        "overview": "An Income Certificate is an official statement certifying the annual income of an individual or family from all sources (salary, agriculture, trade, rent, business). It is crucial for fee concessions, scholarship eligibility, EWS certification, and social welfare pensions.",
        "time_limits_and_rules": [
            "Validity: Typically 1 Financial Year (1st April to 31st March) or 3 years (in some states like UP unless income changes).",
            "Income Calculation: Includes total income earned by family members from all sources.",
            "Processing Time: 7 to 15 days."
        ],
        "documents_required": [
            "Salary slip / Form 16 / Income Tax Return (ITR) for salaried employees",
            "Land revenue record (Khatauni/7-12) / Agriculture produce estimate for farmers",
            "Self-declaration of income on stamp paper / prescribed format for unorganized workers",
            "Aadhaar Card and Ration Card",
            "Electricity Bill / Proof of Residence"
        ],
        "application_steps": [
            "Apply online through State e-District portal or at CSC (Common Service Center).",
            "Enter breakdown of family members, occupations, and declared annual income.",
            "Upload ITR/Salary slip/Affidavit and identity proof.",
            "Patwari/Lekhpal conducts income assessment survey.",
            "Tehsildar/Revenue Officer signs and issues certificate."
        ]
    },
    {
        "id": "parivahan-driving-vehicle",
        "category_title": "Driving License & Vehicle Services (Parivahan)",
        "icon": "car",
        "statutory_act": "Motor Vehicles Act, 1988 & Central Motor Vehicles Rules (CMVR) 1989",
        "issuing_portal": "Sarathi & Vahan Portals (Ministry of Road Transport and Highways - MoRTH)",
        "official_url": "https://parivahan.gov.in",
        "overview": "Ministry of Road Transport and Highways provides unified national portals for citizen driving licenses (Sarathi) and vehicle registrations (Vahan), offering contactless online learner license tests, DL renewals, RC transfer, and HSRP booking.",
        "time_limits_and_rules": [
            "Learner's License (LL): Valid for 6 months across India. Can be applied online with Aadhaar authentication (home computer-based LL test in most states).",
            "Permanent Driving License (DL): Can be applied after 30 days and within 180 days of LL issuance. Requires practical driving track test at RTO/Automated Driving Test Track (ADTT).",
            "DL Validity: Non-transport license valid for 20 years or until age 40 (thereafter renewed every 10/5 years)."
        ],
        "documents_required": [
            "Age Proof: Aadhaar, PAN, School Leaving Certificate, Passport",
            "Address Proof: Aadhaar Card, Electricity bill, Voter ID",
            "Form 1 (Self-Declaration of Physical Fitness) / Form 1A (Medical Certificate by registered MBBS doctor for commercial DL or age > 40)",
            "Active Learner's License (for permanent DL)",
            "Passport photo & signature scan"
        ],
        "application_steps": [
            "Visit parivahan.gov.in -> Online Services -> 'Driving License Related Services' (Sarathi).",
            "Select your State and click 'Apply for Learner License (LL)'.",
            "Choose 'Applicant holding Aadhaar' to take the online video-proctored test from home.",
            "Upload Form 1 self-declaration and fee payment.",
            "Complete online LL test (questions on traffic signs and road safety). Download instant LL PDF.",
            "After 30 days, book slot for Permanent DL Driving Test at RTO.",
            "Pass practical driving test; permanent smart card DL is dispatched via Speed Post."
        ]
    },
    {
        "id": "ration-card-food-security",
        "category_title": "Ration Card & Food Security (PDS / ONORC)",
        "icon": "shopping-bag",
        "statutory_act": "National Food Security Act (NFSA), 2013",
        "issuing_portal": "Department of Food and Public Distribution / State Food Portals",
        "official_url": "https://nfsa.gov.in",
        "overview": "Ration Cards enable eligible families to purchase subsidized or free foodgrains (wheat, rice, coarse grains) under the Pradhan Mantri Garib Kalyan Anna Yojana (PMGKAY) and NFSA. Under 'One Nation One Ration Card' (ONORC), beneficiaries can lift rations from any Fair Price Shop (FPS) across India.",
        "time_limits_and_rules": [
            "Antyodaya Anna Yojana (AAY): Poorest of the poor households (Yellow Card) - Entitled to 35 kg foodgrain per family per month free.",
            "Priority Household (PHH): Lower income families based on state inclusion criteria - Entitled to 5 kg foodgrain per person per month free.",
            "Non-NFSA / APL: General households for identity and address proof purposes."
        ],
        "documents_required": [
            "Aadhaar cards of all family members to be included in the ration card",
            "Income certificate of head of household",
            "LPG connection book / declaration of no gas connection",
            "Proof of residence (Electricity bill / Rent agreement)",
            "Joint passport-size photograph of head of household (female senior member)"
        ],
        "application_steps": [
            "Visit state Food & Civil Supplies portal or nfsa.gov.in.",
            "Select 'Apply for New Ration Card' / 'Add Member in Ration Card'.",
            "Designate eldest adult female as Head of Household (as per Section 13 of NFSA).",
            "Enter Aadhaar numbers of all members and upload address & income proof.",
            "Food Supply Officer conducts door-to-door verification.",
            "Digital e-Ration card is generated and linked to electronic Point of Sale (ePoS) machines."
        ]
    },
    {
        "id": "property-tax-municipal-services",
        "category_title": "Property Tax & Urban Local Body (ULB) Services",
        "icon": "building",
        "statutory_act": "State Municipal Corporation / Municipality Acts",
        "issuing_portal": "Urban Development & Municipal Corporation Portals",
        "official_url": "https://mohua.gov.in",
        "overview": "Municipal Corporations, Municipal Councils, and Nagar Panchayats provide civic infrastructure, property tax assessment, water supply & sewerage connections, trade licenses, and solid waste management.",
        "time_limits_and_rules": [
            "Property Tax Payment: Assessed annually based on Unit Area Value (UAV) or Annual Rateable Value (ARV). Most municipalities offer 5% to 10% early-bird rebate if paid in the first quarter (April - June).",
            "Grievance Redressal: Complaints regarding streetlights, garbage, water leaks, stray animals can be registered on Swachhata App or municipal helpline."
        ],
        "documents_required": [
            "Property Unique ID / Assessment Number / Khata Number",
            "Previous Property Tax Paid Receipt",
            "Sale Deed / Registered Conveyance Deed / Mutation Certificate",
            "Building Sanction Plan & Plinth Area measurement"
        ],
        "application_steps": [
            "Open your local Municipal Corporation portal (e.g. MCD Delhi, BMC Mumbai, BBMP Bengaluru, GHMC Hyderabad, KMC Kolkata).",
            "Click on 'Pay Property Tax / ULB Citizen Services'.",
            "Search property by Property Tax ID / Old Assessment Number / Owner Name.",
            "Verify built-up area, usage (residential/commercial), and calculate net payable tax with rebate.",
            "Pay online via payment gateway and immediately download digitally signed Property Tax Payment Receipt."
        ]
    }
]
