"""
Comprehensive Guide and Information for Caste Certificates (Jati Praman Patra) in India
Categories: SC, ST, OBC-NCL, EWS
Statutory references: Articles 341, 342, 340 of the Constitution of India, DoPT O.M. guidelines
"""

CASTE_CERTIFICATE_DATA = {
    "overview": {
        "title": "Caste Certificate (जाति प्रमाण पत्र) Comprehensive Guide",
        "description": "A Caste Certificate is an essential legal document issued by the Government of India / State Governments testifying that a person belongs to a specific Scheduled Caste (SC), Scheduled Tribe (ST), Other Backward Class (OBC), or Economically Weaker Section (EWS) under Constitutional provisions.",
        "purposes": [
            "Availing constitutional reservations in Central & State Government jobs (UPSC, SSC, State PSC, Banking, Railways, Defense).",
            "Securing admission quota in Premier Educational Institutions (IITs, NITs, IIMs, AIIMS, Central & State Universities).",
            "Availing government fee concessions, age relaxations, and scholarship schemes (NSP, Post-Matric, PM-YASASVI).",
            "Obtaining subsidized housing, agricultural loans, land grants, and self-employment welfare schemes."
        ]
    },
    "categories": [
        {
            "id": "sc",
            "name": "Scheduled Caste (SC)",
            "hindi_name": "अनुसूचित जाति",
            "constitutional_basis": "Article 341 & Constitution (Scheduled Castes) Order, 1950",
            "cut_off_date": "10 August 1950 (Must prove residence/ancestry in India on or before this date)",
            "income_criteria": "No income ceiling for caste status itself (income criterion applies only for specific scholarship schemes)",
            "validity": "Lifetime validity (unless revoked due to fraud or de-notification of caste)",
            "key_requirements": [
                "Proof that the applicant or applicant's paternal ancestors resided in the state on 10-Aug-1950.",
                "Paternal lineage caste proof (Father's, Grandfather's, or Real Paternal Uncle's school record, land deed, or caste certificate).",
                "Self-declaration / Affidavit on stamp paper as per State revenue rules."
            ]
        },
        {
            "id": "st",
            "name": "Scheduled Tribe (ST)",
            "hindi_name": "अनुसूचित जनजाति",
            "constitutional_basis": "Article 342 & Constitution (Scheduled Tribes) Order, 1950",
            "cut_off_date": "6 September 1950 (Proof of paternal habitation in notified tribal area / state)",
            "income_criteria": "No income limit for caste status.",
            "validity": "Lifetime validity.",
            "key_requirements": [
                "Proof of tribal community belonging to the Presidential Order of the respective state.",
                "Paternal lineage proof / traditional land revenue records.",
                "Affidavit and recommendation from Gram Panchayat / Local Tribal Council (in Sixth Schedule / Tribal areas)."
            ]
        },
        {
            "id": "obc-ncl",
            "name": "Other Backward Classes - Non-Creamy Layer (OBC-NCL)",
            "hindi_name": "अन्य पिछड़ा वर्ग (गैर-क्रीमी लेयर)",
            "constitutional_basis": "Article 340 & DoPT OM No. 36012/22/93-Estt.(SCT) dated 08.09.1993",
            "cut_off_date": "Year 1993 (Must be in Central OBC List for Central jobs / State List for State jobs)",
            "income_criteria": "Gross Annual Family Income (excluding agricultural income & salary of parents in certain groups) strictly under ₹8,00,000 for preceding 3 consecutive financial years.",
            "validity": "1 Financial Year for NCL certificate (valid from 1st April to 31st March). Must be renewed annually with fresh income proof.",
            "creamy_layer_exclusion": [
                "Children of Constitutional post holders (President, VP, Judges, UPSC/SPSC members, etc.).",
                "Children of Group A / Class I officers in Central/State Govts (or direct recruitment before age 40).",
                "Children of Group B / Class II officers if entered service before age 40 and promoted to Group A before 40.",
                "Individuals having gross annual family income of ₹8 Lakhs or more consecutively for 3 years."
            ],
            "key_requirements": [
                "Caste must be listed in Central OBC List (published by NCBC at ncbc.nic.in) for Central admissions/recruitment.",
                "Father and Mother's last 3 years ITR / Salary Slips / Form 16 / Revenue Officer Income Certificate.",
                "Paternal caste proof (School TC / Land record)."
            ]
        },
        {
            "id": "ews",
            "name": "Economically Weaker Section (EWS)",
            "hindi_name": "आर्थिक रूप से कमजोर वर्ग",
            "constitutional_basis": "103rd Constitutional Amendment Act, 2019 (Articles 15(6) and 16(6))",
            "cut_off_date": "Not applicable (for citizens not covered under SC/ST/OBC reservation)",
            "income_criteria": "Gross annual family income below ₹8,00,000 from all sources (Salary, Agriculture, Business, Profession).",
            "asset_exclusions": [
                "Family owning 5 acres of agricultural land and above.",
                "Residential flat of 1,000 sq. ft. and above.",
                "Residential plot of 100 sq. yards and above in notified municipalities.",
                "Residential plot of 200 sq. yards and above in areas other than notified municipalities."
            ],
            "validity": "1 Financial Year (Valid for the financial year of issuance based on previous financial year's income).",
            "key_requirements": [
                "Must be in General / Unreserved category (not eligible for SC/ST/OBC benefits).",
                "Income & Asset Certificate issued by SDM / Tehsildar in prescribed Annexure-I format.",
                "Family property deeds, electricity bills, and bank statements."
            ]
        }
    ],
    "issuing_authorities": [
        "District Magistrate / Additional District Magistrate / Collector / Deputy Commissioner",
        "Sub-Divisional Magistrate (SDM) / Sub-Divisional Officer (SDO) / Taluka Magistrate / Executive Magistrate",
        "Chief Presidency Magistrate / Additional Chief Presidency Magistrate / Presidency Magistrate",
        "Revenue Officer not below the rank of Tehsildar",
        "Sub-Divisional Officer of the area where the candidate and/or his family normally resides"
    ],
    "mandatory_documents": [
        {
            "document": "Proof of Identity",
            "options": ["Aadhaar Card", "Voter ID Card", "Passport", "PAN Card", "Driving License"]
        },
        {
            "document": "Proof of Present & Permanent Address",
            "options": ["Ration Card", "Electricity Bill / Water Bill", "Domicile Certificate", "Registered Rent Agreement / Property Tax Receipt"]
        },
        {
            "document": "Proof of Caste from Paternal Line",
            "options": [
                "Father's / Paternal Uncle's / Grandfather's Caste Certificate",
                "School Leaving Certificate (TC) mentioning caste & religion of father or applicant",
                "Pre-1950 (SC/ST) or Pre-1993 (OBC) Land Revenue Record / Khatian / Jamabandi / 7/12 extract",
                "Panchayat / Municipal Ward Councillor Caste Verification report"
            ]
        },
        {
            "document": "Income & Asset Proof (For OBC-NCL & EWS)",
            "options": [
                "Salary Slips & Form 16 / ITR of parents for last 3 financial years",
                "Tehsildar / Revenue Inspector Income Certificate",
                "Land holding records (Khata/Khasra/Patta) for EWS asset verification"
            ]
        },
        {
            "document": "Self-Declaration & Photograph",
            "options": [
                "Self-declaration / Affidavit affirming caste, lineage, and no bogus claims (on non-judicial stamp paper if required)",
                "2 recent passport-size color photographs"
            ]
        }
    ],
    "application_procedure": {
        "online": [
            "Step 1: Open your state's official e-District / Citizen portal (e.g., eDistrict UP, Aaple Sarkar Maharashtra, Seva Sindhu Karnataka, RTPS Bihar, edistrict.delhigovt.nic.in).",
            "Step 2: Register a Citizen Account using Aadhaar / Mobile number OTP.",
            "Step 3: Navigate to 'Revenue Department' -> 'Issuance of Caste / Community Certificate'.",
            "Step 4: Choose the target category (SC / ST / OBC-Central / OBC-State / EWS).",
            "Step 5: Fill in applicant personal details, paternal ancestry names, address, and caste sub-category exactly as per government notified lists.",
            "Step 6: Upload scanned copies of required documents (PDF/JPEG, typically < 200 KB) and self-declaration affidavit.",
            "Step 7: Pay the statutory nominal government fee (₹15 to ₹50 depending on state) via UPI / Net Banking / Debit Card.",
            "Step 8: Download Application Acknowledgment with unique Application Reference Number (ARN).",
            "Step 9: Revenue Inspector (Lekhpal/Patwari) conducts local field verification.",
            "Step 10: Tehsildar / SDM digitally signs the certificate. Download the QR-coded digitally signed certificate directly from the portal."
        ],
        "offline": [
            "Step 1: Obtain Caste Certificate Application Form from the local Tehsildar / Taluk Office, SDM Office, or CSC (Common Service Center).",
            "Step 2: Fill in the form and attach self-attested photocopies of identity, residence, paternal caste proof, and affidavit.",
            "Step 3: Get the report endorsed by Village Administrative Officer (VAO) / Patwari / Lekhpal / Ward Member.",
            "Step 4: Submit at SDM / Tehsildar Citizen Facilitation Counter and collect acknowledgment receipt with due date.",
            "Step 5: Collect physical signed certificate or track online using application number (usually 15-30 days processing time)."
        ]
    },
    "central_vs_state": {
        "central_format": "Required for Central Govt jobs (UPSC, SSC, Railway, Banking, Defense) and Central institutions (IITs, IIMs, NITs, Central Universities). Must match the Central List of SC/ST/OBC published by NCBC/Govt of India in Annexure format.",
        "state_format": "Required for State PSCs, State Govt jobs, State CETs, and State Welfare Schemes. Must be in the respective state list (some communities are in state OBC list but not in central list)."
    }
}
