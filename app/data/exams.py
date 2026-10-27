"""
Popular National Civil Services & Competitive Examinations in India
Sources: upsc.gov.in, ssc.gov.in, nta.ac.in, jeemain.nta.nic.in, jeeadv.ac.in, neet.nta.nic.in, State PSCs
Updated with complete 2026 Examination Calendars, Schedules & Timelines
"""

POPULAR_EXAMS_DATA = [
    {
        "id": "nta-jee-main",
        "name": "JEE (Main & Advanced) Engineering Entrance",
        "name_hi": "संयुक्त प्रवेश परीक्षा (JEE Main & Advanced - IITs / NITs)",
        "conducted_by": "National Testing Agency (NTA) & IITs (JAB)",
        "official_url": "https://jeemain.nta.nic.in",
        "official_source": "jeemain.nta.nic.in / jeeadv.ac.in (NTA & IITs)",
        "eligibility_age": "Passed Class 12 in current or preceding 2 years (No upper age limit for JEE Main)",
        "qualification": "10+2 with Physics, Mathematics, and Chemistry/Computer Science",
        "stages": "JEE Main (Session 1 & 2) -> Top 2.5 Lakh qualifiers advance to JEE Advanced",
        "schedule_2026": "Session 1: Registration Nov-Dec 2025, Exam Jan 22-31, 2026. Session 2: Registration Feb-Mar 2026, Exam Apr 1-15, 2026. JEE Advanced: May 2026.",
        "schedule_2026_hi": "सत्र 1: पंजीकरण नवंबर-दिसंबर 2025, परीक्षा 22-31 जनवरी 2026। सत्र 2: पंजीकरण फरवरी-मार्च 2026, परीक्षा 1-15 अप्रैल 2026। जेईई एडवांस्ड: मई 2026।",
        "exam_dates_2026": {
            "session_1_registration": "November 2025 – December 2025",
            "session_1_exam": "January 22 – January 31, 2026",
            "session_2_registration": "February 2026 – March 2026",
            "session_2_exam": "April 1 – April 15, 2026",
            "jee_advanced_exam": "May 2026 (3rd or 4th Sunday of May)",
            "josaa_counseling": "June – July 2026"
        },
        "reservation_benefits": "Category rank lists, relaxed qualifying cutoffs, fee remissions (100% tuition waiver in IITs/NITs for SC/ST/PwD and families with income < ₹1 Lakh).",
        "key_services": ["Admissions to 23 IITs, 32 NITs, 26 IIITs and Centrally Funded Technical Institutes (CFTIs)"]
    },
    {
        "id": "nta-neet-ug",
        "name": "NEET-UG (National Eligibility cum Entrance Test)",
        "name_hi": "नीट-यूजी राष्ट्रीय पात्रता सह प्रवेश परीक्षा (MBBS / BDS / AYUSH)",
        "conducted_by": "National Testing Agency (NTA)",
        "official_url": "https://neet.nta.nic.in",
        "official_source": "nta.ac.in / neet.nta.nic.in (Under Ministry of Health & Education)",
        "eligibility_age": "Minimum 17 years completed as on 31st December of admission year (No upper age limit)",
        "qualification": "10+2 with Physics, Chemistry, Biology/Biotechnology and English",
        "stages": "Single Stage Pen-and-Paper (OMR) National Medical Entrance Examination",
        "schedule_2026": "Registration: February – March 2026. Exam Date: First Sunday of May 2026 (May 3, 2026). Results: June 2026.",
        "schedule_2026_hi": "पंजीकरण: फरवरी – मार्च 2026। परीक्षा तिथि: मई 2026 का पहला रविवार (3 मई 2026)। परिणाम: जून 2026।",
        "exam_dates_2026": {
            "notification_registration": "February – March 2026",
            "exam_date": "May 3, 2026 (First Sunday of May 2026, 2:00 PM – 5:20 PM)",
            "result_date": "June 2026",
            "mcc_aiq_counseling": "July – August 2026"
        },
        "reservation_benefits": "All India Quota (15%) + State Quota (85%) reservations for SC (15%), ST (7.5%), OBC-NCL (27%), EWS (10%), PwD (5%) with reduced qualifying percentile cutoffs.",
        "key_services": ["Admissions to All India AIIMS, JIPMER, Govt Medical Colleges (MBBS), Dental (BDS), AYUSH (BAMS, BHMS)"]
    },
    {
        "id": "upsc-cse",
        "name": "UPSC Civil Services Examination (CSE)",
        "name_hi": "संघ लोक सेवा आयोग सिविल सेवा परीक्षा (IAS / IPS / IFS)",
        "conducted_by": "Union Public Service Commission (UPSC)",
        "official_url": "https://upsc.gov.in",
        "official_source": "upsc.gov.in (Official UPSC Annual Examination Calendar)",
        "eligibility_age": "21 to 32 Years (General). Age relaxation: +5 yrs (SC/ST), +3 yrs (OBC-NCL), +10 yrs (PwD)",
        "qualification": "Graduation (Bachelor's Degree in any discipline from recognized University)",
        "stages": "Preliminary (Objective) -> Mains (Written 9 Papers) -> Personality Test (Interview)",
        "schedule_2026": "Notification: Mid-February 2026. Prelims Exam: Late May 2026 (May 24/31, 2026). Mains Exam: Late September 2026. Interviews: Jan-Apr 2027.",
        "schedule_2026_hi": "अधिसूचना: मध्य फरवरी 2026। प्रारंभिक परीक्षा: मई 2026 (24/31 मई 2026)। मुख्य परीक्षा: सितंबर 2026। साक्षात्कार: जनवरी-अप्रैल 2027।",
        "exam_dates_2026": {
            "notification_date": "February 2026",
            "last_date_to_apply": "March 2026",
            "prelims_exam_date": "May 2026 (Typically last Sunday of May)",
            "prelims_results": "June 2026",
            "mains_exam_date": "September 2026 (5-day written test)",
            "interview_dates": "January – April 2027 (Dholpur House, New Delhi)"
        },
        "reservation_benefits": "Constitutional reservation applies for SC (15%), ST (7.5%), OBC-NCL (27%), EWS (10%), and PwD (4%) with age & attempt relaxations (Unlimited for SC/ST, 9 attempts for OBC/EWS).",
        "key_services": ["Indian Administrative Service (IAS)", "Indian Police Service (IPS)", "Indian Foreign Service (IFS)", "Indian Revenue Service (IRS)"]
    },
    {
        "id": "ssc-cgl",
        "name": "SSC Combined Graduate Level (SSC CGL)",
        "name_hi": "कर्मचारी चयन आयोग संयुक्त स्नातक स्तरीय परीक्षा (SSC CGL)",
        "conducted_by": "Staff Selection Commission (SSC)",
        "official_url": "https://ssc.gov.in",
        "official_source": "ssc.gov.in (Official SSC Examination Calendar)",
        "eligibility_age": "18 to 30/32 Years (Post-wise). Relaxations: SC/ST +5 yrs, OBC +3 yrs",
        "qualification": "Bachelor's Degree in any stream from recognized University",
        "stages": "Tier-I (Computer Based Test) -> Tier-II (Computer Based Test & Skill/Typing Test)",
        "schedule_2026": "Notification: June 2026. Tier-I CBT Exam: September – October 2026. Tier-II CBT Exam: December 2026 – January 2027.",
        "schedule_2026_hi": "अधिसूचना: जून 2026। टियर-I परीक्षा: सितंबर – अक्टूबर 2026। टियर-II परीक्षा: दिसंबर 2026 – जनवरी 2027।",
        "exam_dates_2026": {
            "notification_date": "June 2026",
            "last_date_to_apply": "July 2026",
            "tier_1_exam_dates": "September – October 2026",
            "tier_2_exam_dates": "December 2026 – January 2027"
        },
        "reservation_benefits": "Category reservation, application fee exemption for Women/SC/ST/PwD/Ex-Servicemen, and lower qualifying cutoffs.",
        "key_services": ["Assistant Section Officer (ASO) in Central Secretariat", "Income Tax Inspector", "Central Excise Inspector", "Assistant Enforcement Officer (ED)", "Sub-Inspector in CBI"]
    },
    {
        "id": "state-pscs",
        "name": "State Civil Services (State PSCs - UPPSC, MPSC, BPSC, KPSC, etc.)",
        "name_hi": "राज्य लोक सेवा आयोग परीक्षाएं (SDM, DSP, BDO, तहसीलदार)",
        "conducted_by": "Respective State Public Service Commissions",
        "official_url": "https://uppsc.up.nic.in / https://mpsc.gov.in / https://bpsc.bih.nic.in",
        "official_source": "State Public Service Commission Official Portals",
        "eligibility_age": "21 to 40 Years (varies by state, e.g., 21-40 in UP/Bihar, 19-38 in Maharashtra)",
        "qualification": "Graduation in any discipline",
        "stages": "State Prelims -> State Mains Written -> Interview",
        "schedule_2026": "UPPSC PCS 2026: Prelims Mar/Apr 2026, Mains July 2026. BPSC CCE 2026: Prelims Sept 30, 2026. MPSC Rajyaseva 2026: Prelims Apr/May 2026.",
        "schedule_2026_hi": "UPPSC PCS 2026: प्रीलिम्स मार्च/अप्रैल 2026। BPSC CCE 2026: प्रीलिम्स 30 सितंबर 2026। MPSC 2026: प्रीलिम्स अप्रैल/मई 2026।",
        "exam_dates_2026": {
            "uppsc_pcs": "Prelims: March/April 2026 | Mains: July 2026",
            "bpsc_cce": "Prelims: September 30, 2026 | Mains: January 2027",
            "mpsc_rajyaseva": "Prelims: April/May 2026 | Mains: September 2026"
        },
        "reservation_benefits": "State domicile candidates receive state quota reservations for SC, ST, OBC, EWS, and Women candidates as per State Public Service Reservation Rules.",
        "key_services": ["Sub-Divisional Magistrate (SDM / Dy. Collector)", "Deputy Superintendent of Police (DSP)", "Block Development Officer (BDO)", "Naib Tehsildar / Commercial Tax Officer"]
    },
    {
        "id": "upsc-nda-cds",
        "name": "UPSC NDA & CDS (Defense Services Officer Entrance)",
        "name_hi": "एनडीए एवं सीडीएस रक्षा सेवा परीक्षा (Army, Navy, Air Force Officers)",
        "conducted_by": "Union Public Service Commission (UPSC)",
        "official_url": "https://upsc.gov.in",
        "official_source": "upsc.gov.in (Ministry of Defence)",
        "eligibility_age": "NDA: 16.5 to 19.5 Years (Unmarried Men & Women); CDS: 19 to 24 Years",
        "qualification": "NDA: 10+2 (with Physics & Maths for Air Force/Navy); CDS: Graduation",
        "stages": "UPSC Written Examination -> 5-Day Services Selection Board (SSB) Interview -> Medical Board",
        "schedule_2026": "NDA/CDS (I) 2026: Notification Dec 2025/Jan 2026, Exam April 2026. NDA/CDS (II) 2026: Notification May 2026, Exam September 2026.",
        "schedule_2026_hi": "NDA/CDS (I) 2026: अधिसूचना दिसंबर 2025, परीक्षा अप्रैल 2026। NDA/CDS (II) 2026: अधिसूचना मई 2026, परीक्षा सितंबर 2026।",
        "exam_dates_2026": {
            "nda_cds_1_exam": "April 2026",
            "nda_cds_2_exam": "September 2026"
        },
        "reservation_benefits": "Full scholarship & military cadet training allowances provided by Govt of India; fee exemption for Women/SC/ST candidates.",
        "key_services": ["Commissioned Officers in Indian Army (IMA/OTA), Indian Navy (INA), Indian Air Force (AFA)"]
    }
]
