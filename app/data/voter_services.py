"""
Comprehensive Guide to Voter Services provided by Election Commission of India (ECI)
Sources: voters.eci.gov.in, ECI Handbook, Representation of the People Act 1950 & 1951
"""

VOTER_SERVICES_DATA = {
    "portal_name": "ECI Voter Service Portal",
    "portal_url": "https://voters.eci.gov.in",
    "helpline_number": "1950",
    "mobile_app": "Voter Helpline App (Android / iOS)",
    "overview": {
        "title": "Election Commission of India (ECI) Voter Services",
        "description": "The Election Commission of India provides full end-to-end digital services for citizens to register as electors, update details, download digital Voter ID (e-EPIC), and find polling booths under the Representation of the People Act.",
        "qualifying_dates": [
            "1st January",
            "1st April",
            "1st July",
            "1st October"
        ],
        "qualifying_dates_note": "As per the Election Laws (Amendment) Act, citizens turning 18 can now register in advance on four qualifying dates every year instead of just once a year."
    },
    "forms": [
        {
            "form_number": "Form 6",
            "title": "Application for New Voter Registration / Inclusion of Name",
            "hindi_title": "नए मतदाता के रूप में पंजीकरण (प्रारूप 6)",
            "purpose": "For citizens who have completed 18 years of age or are turning 18 on upcoming qualifying dates, or who have never registered as a voter in any constituency in India.",
            "eligibility": "Indian citizen, minimum 18 years of age on qualifying date, resident in the assembly constituency.",
            "documents_required": [
                "Proof of Age (Any ONE: Birth Certificate, Aadhaar Card, PAN Card, Driving License, Class 10/12 Passing Certificate, Indian Passport)",
                "Proof of Ordinary Residence (Any ONE: Aadhaar Card, Water/Electricity/Gas connection bill >= 1 year, Current Passbook of Nationalized/Scheduled Bank or Post Office, Indian Passport, Registered Sale Deed / Rent Deed)",
                "Recent passport size color photograph (white background, < 2MB)",
                "Declaration form if age is above 21 years and registering for the first time"
            ],
            "application_steps": [
                "Go to voters.eci.gov.in or open Voter Helpline App.",
                "Click on 'Fill Form 6 - Register as a New Elector/Voter'.",
                "Select your State, District, and Assembly Constituency.",
                "Fill personal details: Name, Surname, Relative's name (Father/Mother/Spouse), Contact Mobile Number, Email ID.",
                "Enter Aadhaar Number (optional for authentication) or mark not having Aadhaar.",
                "Select Gender, Date of Birth, and upload valid Age Proof document.",
                "Enter complete residential address with PIN code and upload Residence Proof.",
                "Provide details of any family member already registered in the same polling booth (helps in family tagging in same booth).",
                "Review the preview, agree to self-declaration, and submit.",
                "Note down the 12-digit Application Reference Number to track status.",
                "Booth Level Officer (BLO) will visit for physical verification within 15-21 days.",
                "Upon ERO approval, EPIC number is generated and e-EPIC becomes immediately downloadable."
            ]
        },
        {
            "form_number": "Form 6A",
            "title": "Application for Registration of Overseas / NRI Elector",
            "hindi_title": "प्रवासी / एनआरआई मतदाता पंजीकरण (प्रारूप 6A)",
            "purpose": "For Indian citizens residing outside India due to employment, education, or other reasons, who have not acquired citizenship of any other country.",
            "eligibility": "Indian Citizen holding a valid Indian Passport, living abroad, not disqualified as an elector.",
            "documents_required": [
                "Copy of valid Indian Passport containing photo, address in India, and visa endorsement pages",
                "Recent passport size color photograph",
                "Proof of current residential address in foreign country"
            ],
            "application_steps": [
                "Visit voters.eci.gov.in and choose 'Form 6A - Overseas Elector'.",
                "Select the Assembly Constituency corresponding to the residential address mentioned in your Indian Passport.",
                "Upload passport pages and visa details.",
                "Overseas electors can vote in person at the designated polling station in India by presenting original Indian Passport."
            ]
        },
        {
            "form_number": "Form 7",
            "title": "Objection for Proposed Inclusion / Deletion of Name in Electoral Roll",
            "hindi_title": "मतदाता सूची से नाम हटाने / आपत्ति (प्रारूप 7)",
            "purpose": "Used to request deletion of an elector's name due to death, permanent shifting to another city/state, duplicate registration, or objection against wrongful inclusion of an ineligible person.",
            "eligibility": "Any elector enrolled in the same electoral roll.",
            "documents_required": [
                "Death Certificate (in case of deceased elector deletion)",
                "EPIC Number of the person whose name is to be deleted",
                "Applicant's own EPIC details"
            ],
            "application_steps": [
                "Select Form 7 on voters.eci.gov.in.",
                "Choose option: 'Self' (if shifting) or 'Other' (death/duplicate).",
                "Enter EPIC number of elector to be deleted.",
                "Provide reason for deletion and attach supporting proof (e.g. death certificate).",
                "Submit and get reference number."
            ]
        },
        {
            "form_number": "Form 8",
            "title": "Correction of Entries, Shifting of Residence & Replacement EPIC",
            "hindi_title": "प्रविष्टियों में सुधार / निवास परिवर्तन / प्रतिस्थापन वोटर कार्ड (प्रारूप 8)",
            "purpose": "Multi-purpose form for: (1) Shifting of residence (within or to another constituency), (2) Correction of existing entries (Name, Age, DOB, Gender, Relation name, Photo, Mobile number), (3) Issue of Replacement EPIC (lost/mutilated/destroyed), (4) Marking of Person with Benchmark Disability (PwD).",
            "eligibility": "Already registered elector with an existing EPIC Number.",
            "documents_required": [
                "EPIC Number",
                "Supporting document for correction (e.g. Aadhaar / Class 10 Certificate for Name/DOB; Marriage certificate for surname change)",
                "Proof of New Address (if shifting residence)",
                "Disability Certificate (if marking PwD status for wheelchair/home voting facility)",
                "Police FIR / NCR copy (if replacement EPIC requested due to loss/theft)"
            ],
            "application_steps": [
                "Login to voters.eci.gov.in and click 'Form 8'.",
                "Choose application type: (a) Shifting of Residence, (b) Correction of Entries in Existing Roll, (c) Issue of Replacement EPIC without correction, (d) Marking of PwD.",
                "Enter EPIC number to fetch existing records.",
                "Check fields to correct (up to 4 entries can be corrected at once).",
                "Enter corrected details and upload documentary proof.",
                "Submit to receive tracking ID. ERO updates roll and dispatches updated physical EPIC card via Speed Post free of cost."
            ]
        }
    ],
    "digital_services": [
        {
            "name": "e-EPIC Download (Digital Voter ID Card)",
            "description": "A secure, portable PDF version of the Electoral Photo Identity Card with QR code containing voter serial, part number, and photo. Can be saved on Digilocker or printed.",
            "prerequisites": "Applicant's mobile number must be registered/linked to the EPIC in the electoral roll.",
            "how_to_download": [
                "Visit voters.eci.gov.in -> 'Download e-EPIC'.",
                "Enter your EPIC Number or Form Reference Number and select State.",
                "Click 'Send OTP' to the registered mobile number.",
                "Enter the 6-digit OTP and click 'Download e-EPIC PDF'.",
                "If mobile is not linked, submit Form 8 first to update mobile number with OTP verification."
            ]
        },
        {
            "name": "Electoral Search (Search Name in Voter List)",
            "description": "Check if your name is active in the voter list, find your Polling Station (Polling Booth), Part Number, and Serial Number.",
            "search_modes": [
                "Search by Details (Name, Relative Name, DOB, State, District, Assembly Constituency)",
                "Search by EPIC (Enter EPIC Number and State)",
                "Search by Mobile Number (Enter registered Mobile Number and verify OTP)"
            ],
            "portal_link": "https://electoralsearch.eci.gov.in"
        },
        {
            "name": "Know Your Polling Station & Officers (BLO / ERO / DEO)",
            "description": "Find the contact details, phone numbers, and designated office of your local Booth Level Officer (BLO), Electoral Registration Officer (ERO), and District Magistrate/Election Officer.",
            "portal_link": "https://voters.eci.gov.in"
        }
    ],
    "helpline_and_grievance": {
        "toll_free": "1950 (Dial from any mobile/landline with STD code for district assistance)",
        "working_hours": "10:00 AM to 5:00 PM (Monday to Saturday) / 24x7 during Election period",
        "grievance_portal": "National Grievances Service Portal (NGSP) at eci-citizenservices.eci.nic.in"
    }
}
