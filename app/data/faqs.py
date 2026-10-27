"""
Frequently Asked Questions (FAQs) and Grievance Redressal Directory
For Indian Civil and Civic Services
"""

FAQS_DATA = [
    {
        "category": "Scholarships",
        "question": "What is NSP OTR (One Time Registration) and why is it mandatory?",
        "answer": "NSP OTR is a unique 14-digit identifier assigned to every student registering on the National Scholarship Portal (scholarships.gov.in). It authenticates the student using Aadhaar Face Authentication or Aadhaar OTP to eliminate ghost beneficiaries and duplicate applications. OTR is valid for the student's entire educational career."
    },
    {
        "category": "Scholarships",
        "question": "Why is Aadhaar-NPCI bank account seeding required for scholarship disbursement?",
        "answer": "Direct Benefit Transfer (DBT) funds are disbursed through the National Payments Corporation of India (NPCI) Aadhaar Payment Bridge System (APBS). Even if you have an active bank account, DBT will fail unless your bank account is mapped to your Aadhaar in the NPCI mapper. You can check seeding status on the official UIDAI website or your bank branch."
    },
    {
        "category": "Scholarships",
        "question": "Can I apply for both State and Central Government scholarships simultaneously?",
        "answer": "No. Under Government of India rules, a student can receive only ONE government scholarship at any given time. If you apply for multiple schemes and are selected, you must surrender one before claiming the other. Availing multiple government scholarships for the same course constitutes an offense."
    },
    {
        "category": "Caste Certificate",
        "question": "What is the difference between Central List OBC and State List OBC certificates?",
        "answer": "States maintain their own list of Other Backward Classes (OBC), and the Central Government (NCBC) maintains a Central OBC List. Some castes may be recognized as OBC in a specific state but not in the Central list. For Central government jobs (UPSC, SSC, Railways) and Central institutions (IITs, NITs, Central Universities), your caste must be in the Central List, and the certificate must follow the Central Govt Annexure format."
    },
    {
        "category": "Caste Certificate",
        "question": "Why does an OBC-NCL or EWS certificate expire every year while SC/ST is lifetime?",
        "answer": "SC and ST certificates are based purely on birth and social heritage, which is permanent. In contrast, OBC-NCL (Non-Creamy Layer) and EWS (Economically Weaker Sections) benefits are dependent on annual family income ceilings (under ₹8 Lakhs/year) and asset limits. Since family income changes annually, NCL and EWS certificates are issued on a financial year basis (valid from April 1 to March 31)."
    },
    {
        "category": "Caste Certificate",
        "question": "Can a woman get a caste certificate based on her husband's caste after marriage?",
        "answer": "No. The Supreme Court of India has ruled in multiple landmark judgments (e.g., Valsamma Paul case and R. Uma Devi case) that caste is determined strictly by birth and paternal lineage. A woman marrying a person of an SC, ST, or OBC community cannot acquire caste status or claim reservation benefits based on her husband's caste."
    },
    {
        "category": "Voter Services",
        "question": "How can I check if my name is in the voter list and download my e-EPIC?",
        "answer": "You can visit voters.eci.gov.in or electoralsearch.eci.gov.in and search using your EPIC Number or Name/District details. If your mobile number is linked in the electoral roll, you can click 'Download e-EPIC' and receive an OTP to instantly download the PDF version of your voter card."
    },
    {
        "category": "Voter Services",
        "question": "What is Form 8 used for in Voter Services?",
        "answer": "Form 8 is a single multi-purpose form used for: (1) Shifting of residence (within or to a new constituency), (2) Correcting details (Name, DOB, Gender, Relative's name, Photo), (3) Requesting a replacement EPIC card without correction (lost/damaged card), and (4) Marking yourself as a Person with Benchmark Disability (PwD) for accessible polling facilities."
    },
    {
        "category": "Civic Services",
        "question": "What happens if a birth or death is not registered within 21 days?",
        "answer": "Under the Registration of Births and Deaths Act: (1) 21-30 days requires permission of Registrar with nominal late fee. (2) 30 days to 1 year requires permission of Sub-Divisional Magistrate (SDM) with an affidavit. (3) Beyond 1 year requires an order from a First Class Magistrate/SDM along with a Non-Availability Certificate (NAC) from the local registrar."
    },
    {
        "category": "Civic Services",
        "question": "Can I use Parivahan Sewa to get a Learner's License without visiting the RTO?",
        "answer": "Yes! In most Indian states and UTs, contactless Learner's License (LL) services are enabled through Aadhaar authentication on parivahan.gov.in (Sarathi). You can submit documents, pay fees, and take the online proctored driving rules test from your home computer/mobile. Once passed, the Learner's License is available for instant download."
    }
]

GRIEVANCE_DIRECTORY = [
    {
        "portal_name": "CPGRAMS (Centralized Public Grievance Redress and Monitoring System)",
        "url": "https://pgportal.gov.in",
        "description": "National 24x7 web portal for citizens to lodge grievances against any Central Ministry, Department, or Autonomous Body.",
        "helpline": "1800-11-0031"
    },
    {
        "portal_name": "Election Commission of India National Grievance Portal (NGSP)",
        "url": "https://voters.eci.gov.in",
        "description": "Direct portal for voter service grievances, BLO complaints, EPIC card delays, and electoral roll disputes.",
        "helpline": "1950 (Toll-Free)"
    },
    {
        "portal_name": "RTI Online (Right to Information Portal)",
        "url": "https://rtionline.gov.in",
        "description": "Lodge RTI applications and first appeals online to obtain certified information from public authorities under RTI Act 2005.",
        "helpline": "011-24622461"
    },
    {
        "portal_name": "National Consumer Helpline (NCH - INGRAM)",
        "url": "https://consumerhelpline.gov.in",
        "description": "Lodge complaints regarding consumer rights, e-commerce, banking, municipal service failures, and private utility disputes.",
        "helpline": "1915 / 1800-11-4000"
    }
]
