"""
CivicGuide AI - Citizen Assistant Intelligent Conversational Engine
Provides accurate, context-aware answers on Indian Civil Services,
Competitive Exams (UPSC, SSC, State PSCs, NEET, JEE Main & Advanced, NDA/CDS),
Welfare Schemes (PM-Kisan, Ayushman Bharat, PMAY, PM Vishwakarma, PM Ujjwala),
Scholarships (NSP, Post-Matric, CSSS, AICTE, PM-YASASVI, OTR),
Caste Certificates (OBC-NCL, EWS, SC, ST), Voter Forms (6, 8, e-EPIC),
Civic Services (Driving License, Birth/Death, Domicile, Ration),
and State Welfares with verified official .gov.in sources in English & Hindi.

Completely updated with 2026 Examination Calendars, Schedules, Timelines,
and Welfare Scheme Installment / Application release dates.
"""

import re
from app.data.scholarships import SCHOLARSHIPS_DATA
from app.data.caste_certificate import CASTE_CERTIFICATE_DATA
from app.data.voter_services import VOTER_SERVICES_DATA
from app.data.civic_services import CIVIC_SERVICES_DATA
from app.data.state_portals import STATE_PORTALS_DATA
from app.data.exams import POPULAR_EXAMS_DATA
from app.data.welfare_schemes import NATIONAL_WELFARES_DATA
from app.data.faqs import FAQS_DATA, GRIEVANCE_DIRECTORY


def has_word(pattern: str, text: str) -> bool:
    """Matches exact word boundaries or literal phrases to eliminate false substring collisions."""
    p_lower = pattern.lower()
    t_lower = text.lower()
    if ' ' in p_lower or '-' in p_lower or '/' in p_lower or '.' in p_lower or any(ord(c) > 127 for c in p_lower):
        return p_lower in t_lower
    return bool(re.search(r'\b' + re.escape(p_lower) + r'\b', t_lower))


def has_any(patterns: list, text: str) -> bool:
    return any(has_word(p, text) for p in patterns)


def get_exam_aspect(q: str) -> str:
    """Detects what specific aspect/dimension of an exam the user is inquiring about."""
    # 1. Time / Duration / Shift Timings
    duration_words = [
        "time alloted", "time allotted", "allotted time", "alloted time", "duration", 
        "how many hours", "how much time", "exam time", "exam timing", "exam timings", 
        "shift time", "shift timing", "shift timings", "total time", "hours", "minutes", 
        "reporting time", "gate closing", "samay", "kitna samay", "kitne ghante", "avdhi",
        "समय", "अवधि", "कितने घंटे", "कितना समय", "परीक्षा का समय"
    ]
    if any(w in q for w in duration_words):
        return "duration"

    # 2. Marking Scheme / Negative Marking
    marking_words = [
        "negative marking", "marking scheme", "marks deducted", "negative marks", 
        "minus marking", "marking", "how many marks deducted", "wrong answer", 
        "penalty", "minus mark", "कटाव", "नेगेटिव मार्किंग", "अंकन योजना", "गलत उत्तर", "माइनस मार्किंग"
    ]
    if any(w in q for w in marking_words):
        return "marking"

    # 3. Exam Pattern / Total Marks / Number of Questions / Sections
    pattern_words = [
        "pattern", "exam pattern", "total marks", "how many questions", "number of questions", 
        "how many marks", "sections", "subjects", "paper 1", "paper 2", "tier 1", "tier 2", 
        "kul ank", "kitne question", "kitne marks", "कितने प्रश्न", "पैटर्न", "कुल अंक", "परीक्षा प्रारूप"
    ]
    if any(w in q for w in pattern_words):
        return "pattern"

    # 4. Eligibility / Age Limit / Attempts / 75% Rule / Educational Criteria
    eligibility_words = [
        "eligibility", "age limit", "age", "qualification", "how many attempts", "attempts", 
        "75%", "75 percent", "percentage", "minimum marks", "criteria", "who can apply", 
        "educational qualification", "eligibility criteria", "पात्रता", "आयु सीमा", "प्रयास", "योग्यता"
    ]
    if any(w in q for w in eligibility_words):
        return "eligibility"

    # 5. Syllabus / Topics / Chapters
    syllabus_words = [
        "syllabus", "what to study", "topics", "chapters", "subjects to prepare", 
        "curriculum", "high weightage", "important topics", "पाठ्यक्रम", "सिलेबस"
    ]
    if any(w in q for w in syllabus_words):
        return "syllabus"

    # 6. Fees / Application Cost / Concessions
    fee_words = [
        "fee", "fees", "cost", "application fee", "registration fee", "form fee", 
        "how much fee", "concession", "waiver", "शुल्क", "फीस"
    ]
    if any(w in q for w in fee_words):
        return "fees"

    # 7. Admit Card / Center Guidelines / Dress Code / Permitted Items
    admit_words = [
        "admit card", "hall ticket", "dress code", "what to carry", "rules", 
        "guidelines", "stationery", "allowed items", "prohibited items", "exam hall rules", 
        "एडमिट कार्ड", "प्रवेश पत्र", "ड्रेस कोड"
    ]
    if any(w in q for w in admit_words):
        return "admit_card"

    # 8. Counseling / Cutoff / Rank vs Percentile
    counseling_words = [
        "counseling", "counselling", "cutoff", "cut off", "cut-off", "josaa", 
        "csab", "mcc", "seat allotment", "percentile", "rank", "कटऑफ", "काउंसलिंग"
    ]
    if any(w in q for w in counseling_words):
        return "counseling"

    # 9. Dates / Schedule / 2026 Timeline
    schedule_words = [
        "when", "date", "dates", "start", "schedule", "calendar", "timeline", 
        "registration date", "kab hoga", "kab shuru", "tarikh", "2026", 
        "कब शुरू", "तिथि", "तारीख", "कैलेंडर"
    ]
    if any(w in q for w in schedule_words):
        return "schedule"

    return "overview"


def is_schedule_query(q: str) -> bool:
    """Detects if query asks about dates, schedules, start times, deadlines, calendar, or 2026/2027 timelines."""
    schedule_keywords = [
        "when", "date", "dates", "start", "starts", "starting", "schedule", "scheduled",
        "calendar", "timeline", "deadline", "month", "year", "2025", "2026", "2027",
        "session", "phase", "installment", "kist", "kab", "shuru", "tarikh", "samay",
        "aayegi", "milenge", "last date", "end date", "application date", "exam date",
        "समय", "कब", "तारीख", "शुरू", "कैलेंडर", "किस्त", "अंतिम तिथि", "लास्ट डेट", "दिनांक"
    ]
    return has_any(schedule_keywords, q)


def process_citizen_query(query: str, lang: str = "en") -> dict:
    q = query.lower().strip()
    is_hi = lang == "hi" or any(ord(c) >= 0x0900 and ord(c) <= 0x097F for c in query)
    is_time_query = is_schedule_query(q)

    # =========================================================================
    # 1. SPECIALIZED OTR (ONE TIME REGISTRATION) INTENT
    # =========================================================================
    
    # 1.1 NSP OTR (National Scholarship Portal)
    if (has_any(["nsp otr", "scholarship otr", "scholarships otr", "otr face", "face auth", "nsp face", "otr app", "aadhaarfacerd"], q)
            or (has_word("otr", q) and has_any(["nsp", "scholarship", "scholarships", "student", "छात्रवृत्ति", "स्कूल", "कॉलेज"], q))):
        return {
            "title": "NSP One Time Registration (OTR) Complete Guide" if not is_hi else "NSP वन टाइम रजिस्ट्रेशन (OTR) संपूर्ण गाइड",
            "answer": (
                "**NSP OTR (One Time Registration) on `scholarships.gov.in`:**\n\n"
                "1. **What is NSP OTR?**\n"
                "   A unique **14-digit identifier** mandatory for all central and state scholarships on the National Scholarship Portal.\n\n"
                "2. **Step-by-Step Registration Procedure:**\n"
                "   - **Step 1:** Download **'NSP OTR App'** and **'AadhaarFaceRd App'** from Google Play Store on your Android mobile.\n"
                "   - **Step 2:** Open NSP OTR App, enter your Aadhaar number, and complete **Aadhaar Face Authentication** using your mobile camera.\n"
                "   - **Step 3:** Receive your permanent 14-digit OTR Reference Number via SMS.\n"
                "   - **Step 4:** Login to `scholarships.gov.in` using your OTR ID to apply for schemes (Post-Matric, CSSS, AICTE, PM-YASASVI).\n\n"
                "3. **Crucial DBT Requirement:**\n"
                "   Ensure your active bank account is **seeded with Aadhaar in the NPCI mapper**. Scholarships are disbursed strictly via Direct Benefit Transfer (DBT)."
                if not is_hi else
                "**राष्ट्रीय छात्रवृत्ति पोर्टल (NSP) OTR रजिस्ट्रेशन गाइड (`scholarships.gov.in`):**\n\n"
                "1. **NSP OTR क्या है?**\n"
                "   यह 14 अंकों की एक विशिष्ट पहचान संख्या है जो NSP पर सभी केंद्र एवं राज्य सरकार की छात्रवृत्तियों हेतु अनिवार्य है।\n\n"
                "2. **आवेदन की चरणबद्ध प्रक्रिया:**\n"
                "   - **चरण 1:** गूगल प्ले स्टोर से **'NSP OTR App'** एवं **'AadhaarFaceRd App'** डाउनलोड करें।\n"
                "   - **चरण 2:** ऐप में आधार नंबर दर्ज कर कैमरे से **आधार फेस ऑथेंटिकेशन** पूर्ण करें।\n"
                "   - **चरण 3:** मोबाइल पर 14 अंकों का स्थायी OTR नंबर प्राप्त होगा।\n"
                "   - **चरण 4:** `scholarships.gov.in` पर OTR लॉगिन कर अपनी लक्षित छात्रवृत्ति हेतु आवेदन पत्र भरें।\n\n"
                "3. **DBT हेतु आवश्यक शर्त:**\n"
                "   अपना बैंक खाता **NPCI मैपर (आधार सीडिंग)** से अवश्य लिंक रखें, जिससे छात्रवृत्ति राशि सीधे खाते में प्राप्त हो सके।"
            ),
            "official_source": "National Scholarship Portal (https://scholarships.gov.in)",
            "suggested_links": [
                {"label": "NSP Official Portal", "url": "https://scholarships.gov.in"},
                {"label": "Explore Scholarships Hub", "url": "/scholarships"}
            ]
        }

    # 1.2 UPSC OTR (Union Public Service Commission Examination Portal)
    if (has_any(["upsc otr", "upsconline", "upsc registration", "upsconline.nic.in"] , q)
            or (has_word("otr", q) and has_any(["upsc", "ias", "ips", "cse", "nda", "cds", "civil services exam", "यूपीएससी"], q))):
        return {
            "title": "UPSC One Time Registration (OTR) Guide" if not is_hi else "UPSC वन टाइम रजिस्ट्रेशन (OTR) गाइड",
            "answer": (
                "**UPSC OTR (One Time Registration) on `upsconline.nic.in`:**\n\n"
                "1. **Purpose:** Mandatory 1-time profile creation for applying to all UPSC exams (Civil Services CSE, NDA, CDS, CMS, IES, CAPF).\n\n"
                "2. **Registration Steps:**\n"
                "   - Visit `upsconline.nic.in` and click on **'New Registration'**.\n"
                "   - Provide basic personal details (Name as per 10th certificate, Gender, DOB, Father's Name, Mother's Name).\n"
                "   - Verify Mobile Number & Email ID via OTP.\n"
                "   - Set security questions and password to generate your **OTR ID**.\n\n"
                "3. **Benefit:** Saves 70% application time. Information pre-populates automatically for all future UPSC notifications with a 7-day correction window."
                if not is_hi else
                "**UPSC OTR (One Time Registration) पोर्टल गाइड (`upsconline.nic.in`):**\n\n"
                "1. **उद्देश्य:** संघ लोक सेवा आयोग (UPSC) की सभी परीक्षाओं (IAS, IPS, NDA, CDS आदि) में आवेदन हेतु एकल प्रोफाइल निर्माण।\n\n"
                "2. **पंजीकरण प्रक्रिया:**\n"
                "   - `upsconline.nic.in` पर जाकर **'New Registration'** पर क्लिक करें।\n"
                "   - 10वीं के प्रमाणपत्र अनुसार व्यक्तिगत विवरण (नाम, जन्मतिथि, माता-पिता का नाम) भरें।\n"
                "   - मोबाइल व ईमेल पर प्राप्त OTP द्वारा सत्यापन करें।\n"
                "   - स्थायी **OTR ID** प्राप्त होगी।\n\n"
                "3. **लाभ:** एक बार OTR बनने के बाद भविष्य की सभी UPSC परीक्षाओं में बिना दोबारा विवरण भरे सीधे आवेदन किया जा सकता है।"
            ),
            "official_source": "Union Public Service Commission (https://upsconline.nic.in)",
            "suggested_links": [
                {"label": "UPSC OTR Portal", "url": "https://upsconline.nic.in"},
                {"label": "UPSC Official Portal", "url": "https://upsc.gov.in"}
            ]
        }

    # 1.3 General OTR (Disambiguation between NSP OTR & UPSC OTR)
    if has_any(["what is otr", "otr registration", "how to do otr", "otr kya hai", "otr kaise kare", "one time registration", "वन टाइम रजिस्ट्रेशन"], q) and not has_any(["exam", "upsc", "scholarship", "nsp"], q):
        return {
            "title": "One Time Registration (OTR) Guidance (NSP vs UPSC)" if not is_hi else "वन टाइम रजिस्ट्रेशन (OTR) संपूर्ण मार्गदर्शन (NSP एवं UPSC)",
            "answer": (
                "**Government of India uses One Time Registration (OTR) on two major portals:**\n\n"
                "1. 🎓 **NSP OTR (For National Scholarships - `scholarships.gov.in`):**\n"
                "   - Unique 14-digit student identifier created using **Aadhaar Face Authentication** on the **NSP OTR App**.\n"
                "   - Mandatory for all Pre-Matric, Post-Matric, AICTE, CSSS, and PM-YASASVI scholarships.\n\n"
                "2. 🏛️ **UPSC OTR (For Civil Services & Defense Exams - `upsconline.nic.in`):**\n"
                "   - Permanent applicant profile for UPSC exams (IAS, IPS, NDA, CDS, CAPF).\n"
                "   - Created via Mobile/Email OTP on `upsconline.nic.in`.\n\n"
                "👉 *Please specify whether you want guidance for **NSP Scholarships OTR** or **UPSC Exam OTR**.*"
                if not is_hi else
                "**भारत सरकार के दो प्रमुख पोर्टलों पर One Time Registration (OTR) लागू है:**\n\n"
                "1. 🎓 **NSP OTR (छात्रवृत्तियों हेतु - `scholarships.gov.in`):**\n"
                "   - 14 अंकों की पहचान संख्या जो **NSP OTR App** पर **आधार फेस ऑथेंटिकेशन** द्वारा बनती है।\n"
                "   - पोस्ट-मैट्रिक, प्रगति, यशस्वी एवं केंद्रीय छात्रवृत्तियों हेतु अनिवार्य।\n\n"
                "2. 🏛️ **UPSC OTR (प्रतियोगी परीक्षाओं हेतु - `upsconline.nic.in`):**\n"
                "   - UPSC सिविल सेवा (IAS/IPS), NDA, CDS परीक्षाओं हेतु एकल प्रोफाइल पंजीकरण।\n\n"
                "👉 *कृपया बताएं कि आप **NSP छात्रवृत्ति OTR** या **UPSC परीक्षा OTR** के संबंध में जानकारी चाहते हैं।* "
            ),
            "official_source": "NSP (scholarships.gov.in) & UPSC (upsconline.nic.in)",
            "suggested_links": [
                {"label": "NSP Scholarships Portal", "url": "https://scholarships.gov.in"},
                {"label": "UPSC OTR Portal", "url": "https://upsconline.nic.in"}
            ]
        }

    # =========================================================================
    # 2. COMPETITIVE EXAMINATIONS INTENT (Targeted Multi-Aspect Intelligence)
    # =========================================================================
    
    aspect = get_exam_aspect(q)

    # 2.1 JEE Main & JEE Advanced (Engineering Entrance)
    if has_any(["jee", "jee main", "jee advanced", "iit", "nit", "जेईई"], q) and not has_any(["neet", "mbbs"], q):
        
        # 2.1.1 Time Allotted / Duration / Shift Timings
        if aspect == "duration":
            return {
                "title": "JEE Main & Advanced Exam Duration, Time Allotted & Shift Timings" if not is_hi else "जेईई मेन एवं एडवांस्ड: परीक्षा अवधि, आवंटित समय व शिफ्ट टाइमिंग",
                "answer": (
                    "**Joint Entrance Examination (JEE Main & JEE Advanced) - Time Allotted & Shift Timings:**\n\n"
                    "1. **JEE Main Paper 1 (B.E. / B.Tech):**\n"
                    "   - **Exact Time Allotted:** **3 Hours (180 Minutes)**.\n"
                    "   - **For PwD / PwBD Candidates:** **4 Hours (240 Minutes)** (1 hour compensatory time with scribe).\n"
                    "   - **Timing Per Question:** Average of ~2.4 minutes per question (75 questions across Physics, Chemistry, and Mathematics).\n\n"
                    "2. **Daily Shift Timings (JEE Main):**\n"
                    "   - **Shift 1 (Morning Session):** **9:00 AM to 12:00 PM** (Candidate reporting: 7:30 AM to 8:30 AM; Gate strictly closes at 8:30 AM).\n"
                    "   - **Shift 2 (Afternoon Session):** **3:00 PM to 6:00 PM** (Candidate reporting: 1:30 PM to 2:30 PM; Gate strictly closes at 2:30 PM).\n\n"
                    "3. **JEE Main Paper 2 (B.Arch & B.Planning):**\n"
                    "   - **Paper 2A (B.Arch only):** **3 Hours (180 Minutes)**.\n"
                    "   - **Paper 2B (B.Planning only):** **3 Hours (180 Minutes)**.\n"
                    "   - **Both Papers Combined (B.Arch + B.Planning):** **3 Hours 30 Minutes (210 Minutes)**.\n\n"
                    "4. **JEE Advanced (For 23 IITs) Duration:**\n"
                    "   - Conducted on a single day across two mandatory papers:\n"
                    "   - **Paper 1:** **3 Hours** (9:00 AM to 12:00 PM).\n"
                    "   - **Paper 2:** **3 Hours** (2:30 PM to 5:30 PM).\n"
                    "   - **Total Duration:** **6 Hours** (Both papers compulsory to qualify for IIT admissions)."
                    if not is_hi else
                    "**संयुक्त प्रवेश परीक्षा (JEE Main एवं JEE Advanced) - परीक्षा का समय व अवधि:**\n\n"
                    "1. **जेईई मेन पेपर 1 (B.E. / B.Tech):**\n"
                    "   - **कुल आवंटित समय:** **3 घंटे (180 मिनट)**।\n"
                    "   - **दिव्यांग (PwD) अभ्यर्थियों हेतु:** **4 घंटे (240 मिनट)** (1 घंटा अतिरिक्त प्रतिपूरक समय)।\n"
                    "   - **प्रति प्रश्न औसत समय:** लगभग 2.4 मिनट (कुल 75 प्रश्न: भौतिकी, रसायन, गणित)।\n\n"
                    "2. **दैनिक परीक्षा शिफ्ट का समय (JEE Main):**\n"
                    "   - **शिफ्ट 1 (सुबह की पाली):** प्रातः **9:00 बजे से दोपहर 12:00 बजे** तक (गेट बंद होने का समय: 8:30 AM)।\n"
                    "   - **शिफ्ट 2 (दोपहर की पाली):** दोपहर **3:00 बजे से शाम 6:00 बजे** तक (गेट बंद होने का समय: 2:30 PM)।\n\n"
                    "3. **जेईई मेन पेपर 2 (वास्तुकला एवं प्लानिंग):**\n"
                    "   - केवल बी.आर्क अथवा बी.प्लानिंग: **3 घंटे (180 मिनट)**।\n"
                    "   - दोनों पेपर एक साथ: **3 घंटे 30 मिनट (210 मिनट)**।\n\n"
                    "4. **जेईई एडवांस्ड (IIT प्रवेश परीक्षा) अवधि:**\n"
                    "   - एक ही दिन में दो अनिवार्य पेपर:\n"
                    "   - **पेपर 1:** प्रातः 9:00 से 12:00 (**3 घंटे**)\n"
                    "   - **पेपर 2:** दोपहर 2:30 से 5:30 (**3 घंटे**)\n"
                    "   - **कुल अवधि:** **6 घंटे** (दोनों पेपर देना अनिवार्य)।"
                ),
                "official_source": "National Testing Agency (https://jeemain.nta.nic.in) & IITs (https://jeeadv.ac.in)",
                "suggested_links": [
                    {"label": "JEE Main Official Portal", "url": "https://jeemain.nta.nic.in"},
                    {"label": "JEE Advanced Official Portal", "url": "https://jeeadv.ac.in"}
                ]
            }

        # 2.1.2 Marking Scheme / Negative Marking
        if aspect == "marking":
            return {
                "title": "JEE Main & Advanced Official Marking Scheme & Negative Marking" if not is_hi else "जेईई मेन एवं एडवांस्ड: आधिकारिक मार्किंग स्कीम व नेगेटिव मार्किंग",
                "answer": (
                    "**JEE Main & JEE Advanced Official Marking Scheme:**\n\n"
                    "1. **JEE Main Marking Rules (Paper 1 - B.E. / B.Tech):**\n"
                    "   - **Correct Answer:** **+4 Marks**.\n"
                    "   - **Incorrect Answer:** **-1 Mark** (Negative marking deducted for wrong answers).\n"
                    "   - **Unattempted / Marked for Review:** **0 Marks** (No penalty).\n"
                    "   - ⚠️ *Note:* Negative marking of -1 applies to **BOTH Section A (MCQs) and Section B (Numerical Value Questions)**.\n"
                    "   - **Maximum Total Marks:** **300 Marks** (75 questions x 4 marks).\n\n"
                    "2. **JEE Advanced Marking Rules:**\n"
                    "   - Uses variable scoring per question type as specified on the paper instructions:\n"
                    "   - **Single Option Correct:** +3 for correct, -1 for incorrect, 0 if unattempted.\n"
                    "   - **One or More Than One Option Correct:** +4 for all correct options, Partial marks (+1, +2, +3) if some correct options chosen without wrong options, **-2 for any incorrect option**.\n"
                    "   - **Numerical Value:** +3 or +4 for correct, 0 for incorrect (usually no negative marking for integers)."
                    if not is_hi else
                    "**जेईई मेन एवं जेईई एडवांस्ड अंकन पद्धति (Marking Scheme):**\n\n"
                    "1. **जेईई मेन मार्किंग नियम (पेपर 1):**\n"
                    "   - **सही उत्तर:** **+4 अंक** प्राप्त होते हैं।\n"
                    "   - **गलत उत्तर:** **-1 अंक** काटा जाता है (नेगेटिव मार्किंग)।\n"
                    "   - **बिना हल किया प्रश्न:** **0 अंक** (कोई कटौती नहीं)।\n"
                    "   - ⚠️ *विशेष नियम:* नेगेटिव मार्किंग (-1 अंक) बहुविकल्पीय (MCQ) तथा संख्यात्मक (Numerical) दोनों खंडों पर लागू होती है।\n"
                    "   - **कुल पूर्णांक:** **300 अंक** (75 प्रश्न x 4 अंक)।\n\n"
                    "2. **जेईई एडवांस्ड मार्किंग नियम:**\n"
                    "   - इसमें विभिन्न वर्गों के अनुसार +3/-1 या +4/-2 तथा बहु-विकल्पीय प्रश्नों में आंशिक अंक (Partial Marking) का प्रावधान होता है।"
                ),
                "official_source": "NTA JEE Information Bulletin (https://jeemain.nta.nic.in)",
                "suggested_links": [
                    {"label": "JEE Main Information Bulletin", "url": "https://jeemain.nta.nic.in"},
                    {"label": "JEE Advanced Rules", "url": "https://jeeadv.ac.in"}
                ]
            }

        # 2.1.3 Exam Pattern / Number of Questions / Total Marks
        if aspect == "pattern":
            return {
                "title": "JEE Main & Advanced Exam Pattern, Subjects & Total Marks" if not is_hi else "जेईई मेन एवं एडवांस्ड: परीक्षा पैटर्न, विषय एवं कुल अंक",
                "answer": (
                    "**JEE Main & Advanced Complete Exam Pattern:**\n\n"
                    "1. **JEE Main Paper 1 (B.E./B.Tech) Structure:**\n"
                    "   - **Mode:** Computer Based Test (CBT).\n"
                    "   - **Total Marks:** **300 Marks**.\n"
                    "   - **Total Questions:** **75 Questions** (25 in Physics, 25 in Chemistry, 25 in Mathematics).\n"
                    "   - **Section A:** 20 Multiple Choice Questions (MCQs) per subject - All 20 compulsory.\n"
                    "   - **Section B:** 5 Numerical Value Questions per subject - All 5 compulsory.\n"
                    "   - **Languages:** Question paper available in 13 languages (English, Hindi, Assamese, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu, Urdu).\n\n"
                    "2. **JEE Main Paper 2A (B.Arch):** Total 400 Marks (Maths: 100 Marks, Aptitude: 200 Marks, Drawing: 100 Marks on pen-paper).\n\n"
                    "3. **JEE Advanced Pattern:** Two compulsory 3-hour papers (Paper 1 & Paper 2) covering Physics, Chemistry, and Mathematics testing deep conceptual problem solving."
                    if not is_hi else
                    "**जेईई मेन एवं एडवांस्ड परीक्षा पैटर्न:**\n\n"
                    "1. **जेईई मेन पेपर 1 (B.E./B.Tech) संरचना:**\n"
                    "   - **माध्यम:** कंप्यूटर आधारित परीक्षा (CBT)।\n"
                    "   - **कुल पूर्णांक:** **300 अंक**।\n"
                    "   - **कुल प्रश्न:** **75 प्रश्न** (भौतिकी: 25, रसायन: 25, गणित: 25)।\n"
                    "   - **खंड A:** प्रत्येक विषय में 20 बहुविकल्पीय प्रश्न (सभी अनिवार्य)।\n"
                    "   - **खंड B:** प्रत्येक विषय में 5 संख्यात्मक प्रश्न (सभी अनिवार्य)।\n"
                    "   - **भाषाएं:** 13 भारतीय भाषाओं में परीक्षा उपलब्ध (हिंदी, अंग्रेजी आदि)।"
                ),
                "official_source": "National Testing Agency (https://jeemain.nta.nic.in)",
                "suggested_links": [
                    {"label": "NTA JEE Pattern", "url": "https://jeemain.nta.nic.in"}
                ]
            }

        # 2.1.4 Eligibility / Age Limit / Attempts / 75% Rule
        if aspect == "eligibility":
            return {
                "title": "JEE Main & Advanced Eligibility, Age Limit, Attempts & 75% Rule" if not is_hi else "जेईई मेन एवं एडवांस्ड: पात्रता, आयु सीमा, प्रयास व 75% बोर्ड नियम",
                "answer": (
                    "**JEE Main & Advanced Eligibility Criteria & Regulations:**\n\n"
                    "1. **Age Limit:** **No upper or lower age limit** for appearing in JEE Main.\n\n"
                    "2. **Year of Passing 12th Class:**\n"
                    "   - Eligible if passed Class 12 in **2024, 2025**, or appearing in **2026**.\n"
                    "   - Compulsory subjects: Physics, Mathematics, and one of Chemistry/Biology/Biotechnology/Technical Vocational subject.\n\n"
                    "3. **Number of Attempts:**\n"
                    "   - **JEE Main:** Maximum of **3 consecutive years** from passing 12th (with 2 sessions per year = up to 6 opportunities).\n"
                    "   - **JEE Advanced:** Maximum of **2 consecutive years** immediately after passing Class 12.\n\n"
                    "4. **The 75% Board Eligibility Rule (For IITs, NITs, IIITs, CFTIs Admission):**\n"
                    "   - Candidates must secure at least **75% aggregate marks in Class 12 board examination** (**65% for SC, ST, and PwD** candidates), OR fall within the **Top 20 Percentile** of their respective state/central board.\n\n"
                    "5. **Fee Waivers in IITs & NITs:**\n"
                    "   - 100% full tuition fee waiver for SC/ST/PwD students and families with annual income under ₹1 Lakh.\n"
                    "   - 2/3rd tuition fee remission for students whose family income is between ₹1 Lakh and ₹5 Lakhs."
                    if not is_hi else
                    "**जेईई मेन एवं एडवांस्ड पात्रता व नियम:**\n\n"
                    "1. **आयु सीमा:** जेईई मेन में बैठने हेतु **कोई आयु सीमा नहीं** है।\n"
                    "2. **12वीं उत्तीर्ण वर्ष:** 2024 या 2025 में 12वीं उत्तीर्ण अथवा 2026 में 12वीं बोर्ड परीक्षार्थी। अनिवार्य विषय: भौतिकी, गणित व रसायन/जीवविज्ञान।\n"
                    "3. **अधिकतम प्रयास (Attempts):**\n"
                    "   - **जेईई मेन:** लगातार **3 वर्ष** तक (प्रतिवर्ष 2 सत्र = कुल 6 बार)।\n"
                    "   - **जेईई एडवांस्ड:** 12वीं के तुरंत बाद लगातार **2 वर्ष** तक।\n"
                    "4. **75% बोर्ड नियम (IITs, NITs, IIITs में प्रवेश हेतु):**\n"
                    "   - 12वीं बोर्ड में न्यूनतम **75% अंक** (SC/ST/PwD हेतु **65% अंक**) अथवा संबंधित बोर्ड की **टॉप 20 पर्सेंटाइल** में आना अनिवार्य है।\n"
                    "5. **ट्यूशन फीस छूट:** SC/ST/PwD एवं ₹1 लाख से कम पारिवारिक आय वाले छात्रों हेतु IIT/NIT में **100% फीस मुफ्त**।"
                ),
                "official_source": "JoSAA & NTA (https://jeemain.nta.nic.in / https://josaa.nic.in)",
                "suggested_links": [
                    {"label": "JoSAA Eligibility Criteria", "url": "https://josaa.nic.in"},
                    {"label": "JEE Main Portal", "url": "https://jeemain.nta.nic.in"}
                ]
            }

        # 2.1.5 Syllabus / Important Chapters
        if aspect == "syllabus":
            return {
                "title": "JEE Main 2026 Syllabus & High-Weightage Chapters" if not is_hi else "जेईई मेन 2026 पाठ्यक्रम (Syllabus) एवं महत्वपूर्ण विषय",
                "answer": (
                    "**JEE Main Official Syllabus (NCERT Aligned & Rationalized by NTA):**\n\n"
                    "1. **Physics:** Kinematics, Laws of Motion, Work Energy Power, Gravitation, Thermodynamics, Electrostatics, Current Electricity, Magnetic Effects, Optics, Modern Physics (Atoms, Nuclei, Semiconductors).\n\n"
                    "2. **Chemistry:**\n"
                    "   - *Physical:* Mole Concept, Atomic Structure, Chemical Thermodynamics, Chemical & Ionic Equilibrium, Chemical Kinetics.\n"
                    "   - *Inorganic:* Periodic Classification, Chemical Bonding, Coordination Compounds, p-block & d-block elements.\n"
                    "   - *Organic:* Hydrocarbons, Haloalkanes, Alcohols, Aldehydes & Ketones, Amines, Biomolecules.\n\n"
                    "3. **Mathematics:** Coordinate Geometry (Circles, Parabola), Differential & Integral Calculus, Vectors & 3D Geometry, Matrices & Determinants, Sequences & Series, Complex Numbers, Probability."
                    if not is_hi else
                    "**जेईई मेन आधिकारिक पाठ्यक्रम (NTA):**\n\n"
                    "1. **भौतिकी:** यांत्रिकी, गति के नियम, कार्य ऊर्जा व शक्ति, गुरुत्वाकर्षण, ऊष्मागतिकी, स्थिरवैद्युतिकी, धारा विद्युत, प्रकाशिकी, आधुनिक भौतिकी।\n"
                    "2. **रसायन विज्ञान:** भौतिक रसायन (परमाणु संरचना, साम्यावस्था, ऊष्मागतिकी), अकार्बनिक रसायन (रासायनिक आबंधन, उपसहसंयोजक यौगिक), कार्बनिक रसायन (हाइड्रोकार्बन, जैव-अणु)।\n"
                    "3. **गणित:** कैलकुलस (अवकलन व समाकलन), निर्देशांक ज्यामिति, सदिश व त्रिविमीय ज्यामिति (3D), आव्यूह व सारणिक, प्रायिकता।"
                ),
                "official_source": "NTA JEE Syllabus (https://jeemain.nta.nic.in)",
                "suggested_links": [
                    {"label": "Download JEE Syllabus PDF", "url": "https://jeemain.nta.nic.in"}
                ]
            }

        # 2.1.6 Schedule / Dates / Default Overview
        return {
            "title": "JEE Main & Advanced 2026 Official Dates & Examination Schedule" if not is_hi else "जेईई मेन एवं एडवांस्ड 2026 आधिकारिक तिथियां एवं परीक्षा कैलेंडर",
            "answer": (
                "**Joint Entrance Examination (JEE Main & JEE Advanced 2026) Schedule:**\n\n"
                "1. **JEE Main 2026 Session 1 (January Session):**\n"
                "   - **Registration Window:** Opens **November 2025**; Closes **December 2025**.\n"
                "   - **Exam Dates:** Starts in **late January 2026 (typically January 22 to January 31, 2026)**.\n"
                "   - **Results:** Early February 2026.\n\n"
                "2. **JEE Main 2026 Session 2 (April Session):**\n"
                "   - **Registration Window:** Opens **February 2026**; Closes **March 2026**.\n"
                "   - **Exam Dates:** Starts in **early April 2026 (typically April 1 to April 15, 2026)**.\n"
                "   - **Results & All India Ranks (AIR):** Late April 2026.\n\n"
                "3. **JEE Advanced 2026 (For 23 IITs):**\n"
                "   - **Registration:** Opens late April / early May 2026 for top 2,50,000 qualifiers of JEE Main.\n"
                "   - **Exam Date:** **May 2026 (3rd or 4th Sunday of May 2026)** (Paper 1: 9:00 AM – 12:00 PM; Paper 2: 2:30 PM – 5:30 PM).\n"
                "   - **JoSAA Counseling:** Begins in **June 2026**.\n\n"
                "4. **Fee Waivers in IITs/NITs:** 100% full tuition fee waiver for SC/ST/PwD students and families with annual income < ₹1 Lakh; 2/3rd fee remission for income between ₹1L to ₹5L."
                if not is_hi else
                "**संयुक्त प्रवेश परीक्षा (JEE Main एवं JEE Advanced 2026) परीक्षा कार्यक्रम:**\n\n"
                "1. **जेईई मेन 2026 सत्र 1 (जनवरी सत्र):**\n"
                "   - **ऑनलाइन पंजीकरण:** **नवंबर 2025** से शुरू होकर **दिसंबर 2025** तक।\n"
                "   - **परीक्षा तिथियां:** **22 जनवरी से 31 जनवरी 2026** के मध्य आयोजित।\n"
                "   - **परिणाम:** फरवरी 2026 के प्रथम सप्ताह में।\n\n"
                "2. **जेईई मेन 2026 सत्र 2 (अप्रैल सत्र):**\n"
                "   - **ऑनलाइन पंजीकरण:** **फरवरी 2026** से शुरू होकर **मार्च 2026** तक।\n"
                "   - **परीक्षा तिथियां:** **1 अप्रैल से 15 अप्रैल 2026** के मध्य आयोजित।\n"
                "   - **अखिल भारतीय रैंक (AIR):** अप्रैल 2026 के अंत में।\n\n"
                "3. **जेईई एडवांस्ड 2026 (23 IITs में प्रवेश हेतु):**\n"
                "   - **पंजीकरण:** अप्रैल/मई 2026 (जेईई मेन के शीर्ष 2.5 लाख सफल अभ्यर्थियों हेतु)।\n"
                "   - **परीक्षा तिथि:** **मई 2026 का तीसरा/चौथा रविवार** (पेपर 1: 9:00 से 12:00; पेपर 2: 2:30 से 5:30)।\n"
                "   - **JoSAA काउंसलिंग:** **जून 2026** से शुरू होगी।\n\n"
                "4. **IITs/NITs में फीस छूट:** SC/ST/PwD एवं ₹1 लाख से कम आय वाले परिवारों हेतु **100% ट्यूशन फीस पूर्णतः मुफ्त**; ₹1L से ₹5L आय हेतु 2/3 फीस छूट।"
            ),
            "official_source": "NTA & IITs (https://jeemain.nta.nic.in / https://jeeadv.ac.in)",
            "suggested_links": [
                {"label": "JEE Main Official Portal", "url": "https://jeemain.nta.nic.in"},
                {"label": "JEE Advanced Official Portal", "url": "https://jeeadv.ac.in"},
                {"label": "JoSAA Counseling Portal", "url": "https://josaa.nic.in"}
            ]
        }

    # 2.2 NEET-UG (National Eligibility cum Entrance Test for Medical)
    if has_any(["neet", "neet ug", "mbbs", "bds", "aiims", "नीट", "नीट-यूजी"], q):
        
        # 2.2.1 Time Allotted / Duration / Shift Timings
        if aspect == "duration":
            return {
                "title": "NEET-UG Exam Duration, Total Time Allotted & Shift Timings" if not is_hi else "नीट-यूजी: परीक्षा अवधि, आवंटित समय व शिफ्ट टाइमिंग",
                "answer": (
                    "**NEET-UG National Medical Entrance Exam - Exact Time Allotted & Shift Timings:**\n\n"
                    "1. **Total Time Allotted:**\n"
                    "   - **Exact Duration:** **3 Hours and 20 Minutes (200 Minutes)**.\n"
                    "   - **Total Questions:** 200 Questions (Candidates need to attempt **180 Questions**).\n"
                    "   - **Timing Per Question:** Slightly over **1 minute per question** (~66 seconds).\n\n"
                    "2. **Official Shift Timing (Single Session Nationwide):**\n"
                    "   - **Exam Time:** Afternoon shift from **2:00 PM to 5:20 PM IST**.\n"
                    "   - **Mode:** Pen and Paper (OMR sheet offline test) in 550+ cities across India.\n\n"
                    "3. **Reporting & Gate Closing Rules:**\n"
                    "   - **Center Gates Open:** 11:30 AM.\n"
                    "   - **Strict Gate Closing Time:** **1:30 PM** (No candidate permitted entry under any circumstances after 1:30 PM).\n"
                    "   - **OMR Booklet Distribution:** 1:45 PM to 1:50 PM.\n\n"
                    "4. **PwD / Compensatory Time:**\n"
                    "   - Persons with benchmark disabilities (PwD) are granted **1 hour extra (compensatory time)**, making their total allotted duration **4 Hours and 20 Minutes (260 Minutes)**."
                    if not is_hi else
                    "**नीट-यूजी (NEET-UG) परीक्षा अवधि एवं शिफ्ट समय:**\n\n"
                    "1. **कुल आवंटित समय:**\n"
                    "   - **परीक्षा अवधि:** **3 घंटे 20 मिनट (200 मिनट)**।\n"
                    "   - **कुल प्रश्न:** 200 प्रश्न (जिनमें से **180 प्रश्न हल करने होते हैं**)।\n"
                    "   - **प्रति प्रश्न समय:** लगभग 1 मिनट 6 सेकंड।\n\n"
                    "2. **परीक्षा का समय (एकल शिफ्ट):**\n"
                    "   - **समय:** दोपहर **2:00 बजे से शाम 5:20 बजे** तक (ऑफलाइन पेन-पेपर ओएमआर मोड)।\n\n"
                    "3. **रिपोर्टिंग व गेट बंद होने का समय:**\n"
                    "   - परीक्षा केंद्र में प्रवेश: प्रातः 11:30 बजे से।\n"
                    "   - **गेट बंद होने का निश्चित समय:** दोपहर **1:30 बजे** (इसके पश्चात प्रवेश पूर्णतः वर्जित)।\n\n"
                    "4. **दिव्यांग (PwD) अभ्यर्थियों हेतु समय:**\n"
                    "   - 1 घंटा अतिरिक्त प्रतिपूरक समय, कुल **4 घंटे 20 मिनट (260 मिनट)** का समय दिया जाता है।"
                ),
                "official_source": "National Testing Agency (https://neet.nta.nic.in)",
                "suggested_links": [
                    {"label": "NEET Official Portal", "url": "https://neet.nta.nic.in"}
                ]
            }

        # 2.2.2 Marking Scheme / Negative Marking
        if aspect == "marking":
            return {
                "title": "NEET-UG Official Marking Scheme & Negative Marking Rules" if not is_hi else "नीट-यूजी: आधिकारिक मार्किंग स्कीम व नेगेटिव मार्किंग नियम",
                "answer": (
                    "**NEET-UG Official Marking Scheme & Scoring Rules:**\n\n"
                    "1. **Scoring Breakdown:**\n"
                    "   - **Correct Answer:** **+4 Marks**.\n"
                    "   - **Incorrect Answer:** **-1 Mark** (deducted as negative marking for wrong bubble shaded).\n"
                    "   - **Unattempted / Unanswered Question:** **0 Marks** (No marks awarded or deducted).\n"
                    "   - **Multiple Shading:** If more than one option is marked for a single question, it is treated as **Incorrect (-1 Mark)**.\n\n"
                    "2. **Total Maximum Score:** **720 Marks** (180 questions x 4 marks).\n\n"
                    "3. **Tie-Breaking Criteria (in order of priority):** Higher marks in Biology -> Higher marks in Chemistry -> Higher marks in Physics -> Lower ratio of incorrect to correct answers."
                    if not is_hi else
                    "**नीट-यूजी अंकन पद्धति (Marking Scheme):**\n\n"
                    "1. **अंक गणना:**\n"
                    "   - **सही उत्तर:** **+4 अंक**।\n"
                    "   - **गलत उत्तर:** **-1 अंक** काटा जाता है (नेगेटिव मार्किंग)।\n"
                    "   - **अनुत्तरित प्रश्न:** **0 अंक**।\n"
                    "   - **एक से अधिक विकल्प भरने पर:** -1 अंक कटेगा।\n\n"
                    "2. **कुल पूर्णांक:** **720 अंक** (180 प्रश्न x 4 अंक)।"
                ),
                "official_source": "National Testing Agency (https://neet.nta.nic.in)",
                "suggested_links": [
                    {"label": "NEET Information Bulletin", "url": "https://neet.nta.nic.in"}
                ]
            }

        # 2.2.3 Exam Pattern / Number of Questions / Total Marks
        if aspect == "pattern":
            return {
                "title": "NEET-UG Exam Pattern, Subject Breakdown & Total Marks" if not is_hi else "नीट-यूजी: परीक्षा पैटर्न, विषयवार प्रश्न व कुल अंक",
                "answer": (
                    "**NEET-UG Complete Exam Pattern:**\n\n"
                    "1. **Total Questions & Attempt Requirement:**\n"
                    "   - Paper contains **200 Questions**; Candidate must attempt **180 Questions**.\n"
                    "   - **Total Marks:** **720 Marks**.\n\n"
                    "2. **Subject-Wise Question Distribution:**\n"
                    "   - **Physics:** Section A (35 Qs, 140 Marks) + Section B (10 out of 15 Qs, 40 Marks) = **45 Qs (180 Marks)**.\n"
                    "   - **Chemistry:** Section A (35 Qs, 140 Marks) + Section B (10 out of 15 Qs, 40 Marks) = **45 Qs (180 Marks)**.\n"
                    "   - **Botany:** Section A (35 Qs, 140 Marks) + Section B (10 out of 15 Qs, 40 Marks) = **45 Qs (180 Marks)**.\n"
                    "   - **Zoology:** Section A (35 Qs, 140 Marks) + Section B (10 out of 15 Qs, 40 Marks) = **45 Qs (180 Marks)**.\n"
                    "   - Total Biology (Botany + Zoology) accounts for **50% of the entire exam (360 Marks)**.\n\n"
                    "3. **Question Type:** Objective multiple choice questions (MCQs) with 4 options."
                    if not is_hi else
                    "**नीट-यूजी परीक्षा पैटर्न व संरचना:**\n\n"
                    "1. **कुल प्रश्न व पूर्णांक:** कुल 200 प्रश्न, जिनमें से **180 प्रश्न हल करने होते हैं**। कुल पूर्णांक **720 अंक**।\n"
                    "2. **विषयवार विभाजन:**\n"
                    "   - **भौतिकी (Physics):** खंड A (35 प्रश्न) + खंड B (15 में से 10 प्रश्न) = **45 प्रश्न (180 अंक)**।\n"
                    "   - **रसायन (Chemistry):** खंड A (35 प्रश्न) + खंड B (15 में से 10 प्रश्न) = **45 प्रश्न (180 अंक)**।\n"
                    "   - **वनस्पति विज्ञान (Botany):** **45 प्रश्न (180 अंक)**।\n"
                    "   - **प्राणी विज्ञान (Zoology):** **45 प्रश्न (180 अंक)**।\n"
                    "   - जीव विज्ञान (बायोलॉजी) अकेले **360 अंक (50%)** का होता है।"
                ),
                "official_source": "National Testing Agency (https://neet.nta.nic.in)",
                "suggested_links": [
                    {"label": "NEET Portal", "url": "https://neet.nta.nic.in"}
                ]
            }

        # 2.2.4 Eligibility / Age Limit / Attempts
        if aspect == "eligibility":
            return {
                "title": "NEET-UG Eligibility Criteria, Age Limits & Attempts" if not is_hi else "नीट-यूजी: पात्रता, आयु सीमा, प्रयास एवं शैक्षणिक योग्यता",
                "answer": (
                    "**NEET-UG Eligibility Criteria & Qualification Rules:**\n\n"
                    "1. **Age Limit:**\n"
                    "   - **Minimum Age:** Must have completed **17 years** on or before 31st December of the admission year.\n"
                    "   - **Upper Age Limit:** **NO upper age limit** (Removed by National Medical Commission and Hon'ble Supreme Court of India).\n\n"
                    "2. **Number of Attempts:** **Unlimited attempts** (Candidates can appear as many times as desired).\n\n"
                    "3. **Educational Qualification:**\n"
                    "   - Must have passed Class 12 (10+2) or equivalent with **Physics, Chemistry, Biology / Biotechnology, and English**.\n"
                    "   - **Minimum Aggregate Marks in PCB:**\n"
                    "     - General / EWS: **50%**\n"
                    "     - OBC-NCL / SC / ST: **40%**\n"
                    "     - PwD (General): **45%**\n\n"
                    "4. **Appearing Students:** Students currently appearing for their Class 12 board examinations are fully eligible to apply."
                    if not is_hi else
                    "**नीट-यूजी पात्रता एवं शैक्षणिक नियम:**\n\n"
                    "1. **आयु सीमा:**\n"
                    "   - **न्यूनतम आयु:** प्रवेश वर्ष के 31 दिसंबर तक **17 वर्ष** पूर्ण होना अनिवार्य।\n"
                    "   - **अधिकतम आयु सीमा:** **कोई ऊपरी आयु सीमा नहीं है** (NMC एवं सुप्रीम कोर्ट आदेशानुसार)।\n"
                    "2. **अधिकतम प्रयास:** प्रयासों की **कोई सीमा नहीं (Unlimited Attempts)**।\n"
                    "3. **शैक्षणिक योग्यता:** 12वीं में भौतिकी, रसायन, जीवविज्ञान (बायोलॉजी/बायोटेक्नोलॉजी) एवं अंग्रेजी विषय के साथ उत्तीर्ण।\n"
                    "   - PCB में न्यूनतम अंक: सामान्य/EWS: **50%**, OBC/SC/ST: **40%**, दिव्यांग: **45%**।"
                ),
                "official_source": "National Medical Commission & NTA (https://neet.nta.nic.in)",
                "suggested_links": [
                    {"label": "NMC Guidelines", "url": "https://www.nmc.org.in"},
                    {"label": "NEET Official Portal", "url": "https://neet.nta.nic.in"}
                ]
            }

        # 2.2.5 Schedule / Dates / Default Overview
        return {
            "title": "NEET-UG 2026 Official Dates & Examination Schedule" if not is_hi else "नीट-यूजी (NEET-UG 2026) आधिकारिक तिथियां एवं परीक्षा कार्यक्रम",
            "answer": (
                "**NEET-UG 2026 National Medical Entrance Examination Schedule:**\n\n"
                "1. **Notification & Online Registration:**\n"
                "   - Application portal opens in **February 2026** on `neet.nta.nic.in`.\n"
                "   - Last date for online submission: **March 2026**.\n\n"
                "2. **Exact Examination Date:**\n"
                "   - **Date:** **Sunday, May 3, 2026 (First Sunday of May 2026)**.\n"
                "   - **Exam Timing:** Single shift from **2:00 PM to 5:20 PM** (Pen-and-Paper OMR mode across 550+ cities in India and abroad).\n\n"
                "3. **Results & Counseling Timeline:**\n"
                "   - **NTA Scorecards & Cutoffs:** **June 2026**.\n"
                "   - **MCC All India Quota (15%) Counseling:** Begins in **July 2026**.\n"
                "   - **State Quota (85%) Counseling:** Conducted by state authorities from **August 2026**.\n\n"
                "4. **Eligibility:** Minimum 17 years completed by 31st December 2026. No upper age limit. 10+2 with Physics, Chemistry, Biology/Biotechnology."
                if not is_hi else
                "**नीट-यूजी (NEET-UG 2026) मेडिकल प्रवेश परीक्षा कार्यक्रम:**\n\n"
                "1. **अधिसूचना एवं ऑनलाइन आवेदन:**\n"
                "   - आवेदन पत्र **फरवरी 2026** में `neet.nta.nic.in` पर जारी होंगे।\n"
                "   - आवेदन की अंतिम तिथि: **मार्च 2026**।\n\n"
                "2. **निश्चित परीक्षा तिथि:**\n"
                "   - **तिथि:** **रविवार, 3 मई 2026 (मई 2026 का पहला रविवार)**।\n"
                "   - **परीक्षा का समय:** दोपहर **2:00 बजे से शाम 5:20 बजे** तक (पेन एवं पेपर ओएमआर मोड में)।\n\n"
                "3. **परिणाम एवं काउंसलिंग:**\n"
                "   - **परिणाम घोषणा:** **जून 2026**।\n"
                "   - **MCC 15% अखिल भारतीय कोटा काउंसलिंग:** **जुलाई 2026** से।\n"
                "   - **85% राज्य कोटा काउंसलिंग:** **अगस्त 2026** से।\n\n"
                "4. **पात्रता:** 31 दिसंबर 2026 तक न्यूनतम 17 वर्ष आयु। कोई ऊपरी आयु सीमा नहीं। 12वीं में PCB विषय अनिवार्य।"
            ),
            "official_source": "National Testing Agency (https://neet.nta.nic.in)",
            "suggested_links": [
                {"label": "NEET Official Portal", "url": "https://neet.nta.nic.in"},
                {"label": "MCC Medical Counseling", "url": "https://mcc.nic.in"}
            ]
        }

    # 2.3 UPSC Civil Services (IAS / IPS / IFS / CSE)
    if has_any(["upsc", "ias", "ips", "ifs", "civil services exam", "cse", "सिविल सेवा", "यूपीएससी", "कलेक्टर", "collector"], q) and not has_any(["scholarship", "nsp"], q):
        
        # 2.3.1 Time Allotted / Duration / Shift Timings
        if aspect == "duration":
            return {
                "title": "UPSC Civil Services (CSE) Exam Duration & Shift Timings" if not is_hi else "UPSC सिविल सेवा: परीक्षा अवधि, आवंटित समय व शिफ्ट टाइमिंग",
                "answer": (
                    "**UPSC Civil Services Examination (CSE) - Exact Time Allotted & Shift Timings:**\n\n"
                    "1. **CSE Preliminary Examination (Single Day - 2 Shifts):**\n"
                    "   - **Paper I (General Studies 1):** **2 Hours (120 Minutes)** from **9:30 AM to 11:30 AM** (100 Questions, 200 Marks).\n"
                    "   - **Break:** 3 Hours gap between shifts (11:30 AM to 2:30 PM).\n"
                    "   - **Paper II (CSAT):** **2 Hours (120 Minutes)** from **2:30 PM to 4:30 PM** (80 Questions, 200 Marks).\n"
                    "   - **Total Prelims Duration:** **4 Hours** of examination on a single Sunday.\n\n"
                    "2. **CSE Mains Examination (9 Descriptive Papers over 5 Days):**\n"
                    "   - **Duration of Each Paper:** **3 Hours (180 Minutes)**.\n"
                    "   - **Forenoon Session:** **9:00 AM to 12:00 PM** (3 Hours).\n"
                    "   - **Afternoon Session:** **2:00 PM to 5:00 PM** (3 Hours).\n"
                    "   - Conducted over Friday, Saturday, Sunday, followed by the next weekend.\n\n"
                    "3. **Gate Closing Rules:** Entry to exam hall closes **30 minutes prior** to commencement (9:00 AM for forenoon, 2:00 PM for afternoon)."
                    if not is_hi else
                    "**UPSC सिविल सेवा परीक्षा (CSE) - परीक्षा का समय व अवधि:**\n\n"
                    "1. **प्रारंभिक परीक्षा (Prelims - एक ही दिन में 2 शिफ्ट):**\n"
                    "   - **पेपर I (सामान्य अध्ययन GS):** **2 घंटे (120 मिनट)**, प्रातः **9:30 से 11:30 बजे** तक।\n"
                    "   - **पेपर II (सीसैट CSAT):** **2 घंटे (120 मिनट)**, दोपहर **2:30 से 4:30 बजे** तक।\n"
                    "   - **कुल प्रारंभिक परीक्षा अवधि:** **4 घंटे**।\n\n"
                    "2. **मुख्य परीक्षा (Mains - 5 दिनों में 9 वर्णात्मक पेपर):**\n"
                    "   - **प्रत्येक पेपर का समय:** **3 घंटे (180 मिनट)**।\n"
                    "   - **सुबह की पाली:** 9:00 AM से 12:00 PM।\n"
                    "   - **दोपहर की पाली:** 2:00 PM से 5:00 PM।"
                ),
                "official_source": "Union Public Service Commission (https://upsc.gov.in)",
                "suggested_links": [
                    {"label": "UPSC Examination Rules", "url": "https://upsc.gov.in"}
                ]
            }

        # 2.3.2 Marking Scheme / Negative Marking
        if aspect == "marking":
            return {
                "title": "UPSC Civil Services Marking Scheme & Negative Marking" if not is_hi else "UPSC सिविल सेवा: मार्किंग स्कीम व नेगेटिव मार्किंग नियम",
                "answer": (
                    "**UPSC Civil Services Examination Marking Scheme:**\n\n"
                    "1. **Prelims Paper I (General Studies - 100 Questions, 200 Marks):**\n"
                    "   - Correct Answer: **+2.00 Marks**.\n"
                    "   - Incorrect Answer: **-0.66 Marks (1/3rd penalty deduction)**.\n"
                    "   - Unattempted: **0 Marks**.\n"
                    "   - *Cutoff Determinant:* Marks in Paper I determine qualifying for Mains.\n\n"
                    "2. **Prelims Paper II (CSAT - 80 Questions, 200 Marks):**\n"
                    "   - Correct Answer: **+2.50 Marks**.\n"
                    "   - Incorrect Answer: **-0.83 Marks (1/3rd penalty deduction)**.\n"
                    "   - *Qualifying Nature:* Must score minimum **33% (66.00 Marks out of 200)** to qualify. CSAT marks are not counted for merit rank.\n\n"
                    "3. **Mains & Interview (Merit Ranking):**\n"
                    "   - 7 Merit Papers (Essay, GS 1-4, Optional 1-2): 7 x 250 = **1,750 Marks** (Written descriptive, no negative marks).\n"
                    "   - Personality Test (Interview): **275 Marks**.\n"
                    "   - **Grand Total for Final AIR:** **2,025 Marks**."
                    if not is_hi else
                    "**UPSC सिविल सेवा अंकन पद्धति (Marking Scheme):**\n\n"
                    "1. **प्रारंभिक परीक्षा पेपर 1 (GS - 100 प्रश्न, 200 अंक):**\n"
                    "   - सही उत्तर: **+2.00 अंक**।\n"
                    "   - गलत उत्तर: **-0.66 अंक (1/3 नेगेटिव मार्किंग)**।\n\n"
                    "2. **प्रारंभिक परीक्षा पेपर 2 (CSAT - 80 प्रश्न, 200 अंक):**\n"
                    "   - सही उत्तर: **+2.50 अंक**।\n"
                    "   - गलत उत्तर: **-0.83 अंक (1/3 नेगेटिव मार्किंग)**।\n"
                    "   - क्वालिफाइंग पेपर: न्यूनतम **33% (66 अंक)** लाना अनिवार्य है।\n\n"
                    "3. **मुख्य परीक्षा व साक्षात्कार पूर्णांक:** 1,750 अंक (लिखित) + 275 अंक (इंटरव्यू) = **कुल 2,025 अंक** में से मेरिट बनती है।"
                ),
                "official_source": "Union Public Service Commission (https://upsc.gov.in)",
                "suggested_links": [
                    {"label": "UPSC Scheme of Examination", "url": "https://upsc.gov.in"}
                ]
            }

        # 2.3.3 Eligibility / Age Limit / Attempts
        if aspect == "eligibility":
            return {
                "title": "UPSC Civil Services Age Limits, Attempts & Eligibility Criteria" if not is_hi else "UPSC सिविल सेवा: आयु सीमा, अधिकतम प्रयास व पात्रता नियम",
                "answer": (
                    "**UPSC Civil Services Examination (IAS/IPS/IFS) Eligibility Rules:**\n\n"
                    "1. **Age Limits (Calculated as on 1st August of the exam year):**\n"
                    "   - **General & EWS:** **21 to 32 Years** (Maximum **6 Attempts**).\n"
                    "   - **OBC-NCL:** **21 to 35 Years** (Maximum **9 Attempts**).\n"
                    "   - **SC / ST:** **21 to 37 Years** (**Unlimited Attempts** until age 37).\n"
                    "   - **PwBD Candidates:** **21 to 42 Years** (9 attempts for General/OBC, Unlimited for SC/ST).\n"
                    "   - **Ex-Servicemen:** 5 years relaxation up to 37 years.\n\n"
                    "2. **Educational Qualification:**\n"
                    "   - Bachelor's Degree in ANY discipline (Arts, Science, Commerce, Engineering, MBBS) from a recognized university.\n"
                    "   - Candidates in the final year or awaiting final degree results can write Prelims.\n\n"
                    "3. **Nationality:** Indian citizen for IAS, IFS, and IPS. For other services, citizen of India/Nepal/Bhutan.\n\n"
                    "4. **Application Fee Exemption:** Female, SC, ST, and PwBD candidates pay **₹0 fee**."
                    if not is_hi else
                    "**UPSC सिविल सेवा (IAS/IPS) पात्रता एवं नियम:**\n\n"
                    "1. **आयु सीमा व प्रयास (1 अगस्त के अनुसार):**\n"
                    "   - **सामान्य (General / EWS):** **21 से 32 वर्ष** (अधिकतम **6 प्रयास**)।\n"
                    "   - **ओबीसी (OBC-NCL):** **21 से 35 वर्ष** (अधिकतम **9 प्रयास**)।\n"
                    "   - **अनुसूचित जाति/जनजाति (SC / ST):** **21 से 37 वर्ष** (**असीमित प्रयास**)।\n"
                    "   - **दिव्यांग (PwBD):** **21 से 42 वर्ष**।\n\n"
                    "2. **शैक्षणिक योग्यता:** किसी भी संकाय में स्नातक (Graduation) डिग्री। अंतिम वर्ष के छात्र भी प्रारंभिक परीक्षा में बैठ सकते हैं।\n\n"
                    "3. **आवेदन शुल्क:** महिला, SC, ST व PwBD अभ्यर्थियों हेतु आवेदन पूर्णतः निःशुल्क (₹0) है।"
                ),
                "official_source": "Union Public Service Commission (https://upsc.gov.in)",
                "suggested_links": [
                    {"label": "UPSC Eligibility Rules", "url": "https://upsc.gov.in"}
                ]
            }

        # 2.3.4 Syllabus & Subject Breakdown
        if aspect == "syllabus":
            return {
                "title": "UPSC Civil Services (CSE) Prelims & Mains Syllabus" if not is_hi else "UPSC सिविल सेवा: प्रारंभिक व मुख्य परीक्षा पाठ्यक्रम (Syllabus)",
                "answer": (
                    "**UPSC Civil Services Examination (CSE) Detailed Syllabus:**\n\n"
                    "1. **Preliminary Examination Syllabus:**\n"
                    "   - **Paper I (General Studies - 200 Marks):** Current National & International Events, History of India & Indian National Movement, Indian and World Geography, Indian Polity and Governance (Constitution, Political System, Panchayati Raj, Public Policy), Economic and Social Development, General issues on Environmental Ecology, Biodiversity & Climate Change, and General Science.\n"
                    "   - **Paper II (CSAT - 200 Marks, 33% Qualifying):** Reading Comprehension, Interpersonal skills including communication, Logical reasoning & analytical ability, Decision making, General mental ability, Basic numeracy (Class X level), Data interpretation.\n\n"
                    "2. **Main Examination Syllabus (9 Papers - 1,750 Marks):**\n"
                    "   - **Qualifying Papers:** Paper A (Indian Language - 300 Marks), Paper B (English - 300 Marks) - 25% qualifying.\n"
                    "   - **Merit Ranking Papers (250 Marks Each):**\n"
                    "     * **Paper I:** Essay\n"
                    "     * **Paper II (GS-I):** Indian Heritage & Culture, History & Geography of the World & Society\n"
                    "     * **Paper III (GS-II):** Governance, Constitution, Polity, Social Justice & International Relations\n"
                    "     * **Paper IV (GS-III):** Technology, Economic Development, Bio-diversity, Environment, Security & Disaster Management\n"
                    "     * **Paper V (GS-IV):** Ethics, Integrity, and Aptitude\n"
                    "     * **Papers VI & VII:** Optional Subject Papers 1 & 2 (Choose from 26 recognized optional subjects).\n\n"
                    "3. **Personality Test (Interview):** 275 Marks. Grand Total: **2,025 Marks**."
                    if not is_hi else
                    "**UPSC सिविल सेवा परीक्षा (CSE) आधिकारिक पाठ्यक्रम (Syllabus):**\n\n"
                    "1. **प्रारंभिक परीक्षा (Prelims):**\n"
                    "   - **पेपर I (सामान्य अध्ययन 1 - 200 अंक):** राष्ट्रीय व अंतर्राष्ट्रीय समसामयिक घटनाएं, भारत का इतिहास व भारतीय राष्ट्रीय आंदोलन, भारत एवं विश्व भूगोल, भारतीय राजतंत्र व शासन (संविधान, राजनीतिक प्रणाली, पंचायती राज), आर्थिक एवं सामाजिक विकास, पर्यावरण पारिस्थितिकी व जलवायु परिवर्तन, सामान्य विज्ञान।\n"
                    "   - **पेपर II (CSAT - 200 अंक, 33% क्वालीफाइंग):** बौद्धगम्यता (Comprehension), तार्किक क्षमता, निर्णय निर्माण क्षमता, सामान्य मानसिक योग्यता, आधारभूत संख्यान (कक्षा 10 स्तर)।\n\n"
                    "2. **मुख्य परीक्षा (Mains - कुल 1,750 अंक):**\n"
                    "   - **क्वालीफाइंग पेपर:** भारतीय भाषा (300 अंक) व अंग्रेजी (300 अंक)।\n"
                    "   - **मेरिट पेपर (प्रत्येक 250 अंक):** निबंध (Essay), GS-1 (इतिहास, समाज, भूगोल), GS-2 (राजव्यवस्था, शासन, IR), GS-3 (अर्थव्यवस्था, विज्ञान, पर्यावरण, आंतरिक सुरक्षा), GS-4 (नीतिशास्त्र - Ethics), तथा वैकल्पिक विषय (Optional) पेपर 1 व 2।\n\n"
                    "3. **साक्षात्कार (Interview):** 275 अंक। कुल प्राप्तांक: **2,025 अंक**।"
                ),
                "official_source": "Union Public Service Commission (https://upsc.gov.in)",
                "suggested_links": [
                    {"label": "UPSC CSE Official Syllabus PDF", "url": "https://upsc.gov.in"},
                    {"label": "UPSC OTR Registration Portal", "url": "https://upsconline.nic.in"}
                ]
            }

        # 2.3.4 Schedule / Dates / Default Overview
        return {
            "title": "UPSC Civil Services Examination (CSE) 2026 Dates & Rules" if not is_hi else "UPSC सिविल सेवा परीक्षा (CSE 2026) परीक्षा कैलेंडर एवं नियम",
            "answer": (
                "**UPSC Civil Services Examination (CSE 2026) Official Calendar & Rules:**\n\n"
                "1. **2026 Examination Schedule:**\n"
                "   - **Official Notification Released:** **February 2026** (mid-February).\n"
                "   - **Last Date to Apply:** **March 2026** via `upsconline.nic.in` (Mandatory UPSC OTR).\n"
                "   - **CSE Preliminary Examination 2026 Date:** **Late May 2026 (typically May 24 / May 31, 2026)**.\n"
                "   - **Prelims Results:** **June 2026**.\n"
                "   - **CSE Mains Examination 2026 Date:** Starts in **late September 2026** (conducted over 5 days).\n"
                "   - **Personality Test (Interview):** Conducted **January to April 2027** at Dholpur House, New Delhi.\n\n"
                "2. **Age Limits (as on 1st August 2026):**\n"
                "   - **General / EWS:** 21 to 32 Years (Max 6 Attempts)\n"
                "   - **OBC-NCL:** 21 to 35 Years (Max 9 Attempts)\n"
                "   - **SC / ST:** 21 to 37 Years (Unlimited Attempts)\n"
                "   - **PwBD:** 21 to 42 Years (9 attempts for Gen/OBC, Unlimited for SC/ST)\n\n"
                "3. **Educational Qualification:** Bachelor's Degree in any discipline from a recognized University. Final year students are eligible for Prelims.\n\n"
                "4. **Complete Fee Exemption:** Female, SC, ST, and PwBD candidates pay ₹0 application fee."
                if not is_hi else
                "**UPSC सिविल सेवा परीक्षा (CSE 2026) परीक्षा कैलेंडर एवं नियम:**\n\n"
                "1. **वर्ष 2026 परीक्षा कार्यक्रम:**\n"
                "   - **आधिकारिक अधिसूचना जारी:** **फरवरी 2026** (मध्य फरवरी)।\n"
                "   - **आवेदन की अंतिम तिथि:** **मार्च 2026** (`upsconline.nic.in` पर OTR अनिवार्य)।\n"
                "   - **सिविल सेवा प्रारंभिक परीक्षा (Prelims 2026):** **मई 2026 के अंतिम रविवार (24/31 मई 2026)**।\n"
                "   - **मुख्य परीक्षा (Mains 2026):** **सितंबर 2026** के अंतिम सप्ताह में (5 दिवसीय लिखित परीक्षा)।\n"
                "   - **साक्षात्कार (Interview):** **जनवरी से अप्रैल 2027** (धौलपुर हाउस, नई दिल्ली)।\n\n"
                "2. **आयु सीमा (1 अगस्त 2026 के अनुसार):**\n"
                "   - सामान्य (Gen/EWS): 21 से 32 वर्ष (अधिकतम 6 प्रयास)\n"
                "   - ओबीसी (OBC-NCL): 21 से 35 वर्ष (अधिकतम 9 प्रयास)\n"
                "   - एससी/एसटी (SC/ST): 21 से 37 वर्ष (असीमित प्रयास)\n"
                "   - दिव्यांग (PwBD): 21 से 42 वर्ष\n\n"
                "3. **योग्यता:** किसी भी मान्यता प्राप्त विश्वविद्यालय से स्नातक (Graduation) की डिग्री।\n\n"
                "4. **शुल्क छूट:** महिला, SC, ST एवं दिव्यांग अभ्यर्थियों हेतु आवेदन पूर्णतः निःशुल्क है।"
            ),
            "official_source": "Union Public Service Commission (https://upsc.gov.in)",
            "suggested_links": [
                {"label": "UPSC Official Portal", "url": "https://upsc.gov.in"},
                {"label": "UPSC OTR Registration", "url": "https://upsconline.nic.in"}
            ]
        }

    # 2.4 SSC Examinations (SSC CGL / CHSL / MTS)
    if has_any(["ssc", "cgl", "chsl", "mts", "एसएससी", "सीजीएल", "कर्मचारी चयन आयोग", "income tax inspector", "aso", "excise inspector"], q):
        
        # 2.4.1 Time Allotted / Duration / Shift Timings
        if aspect == "duration":
            return {
                "title": "SSC CGL Exam Duration, Shift Timings & Time Limit" if not is_hi else "SSC CGL: परीक्षा अवधि, शिफ्ट टाइमिंग व समय सीमा",
                "answer": (
                    "**Staff Selection Commission (SSC CGL) - Exact Time Allotted & Shift Timings:**\n\n"
                    "1. **Tier-I Examination (Computer Based Test):**\n"
                    "   - **Exact Duration:** **1 Hour (60 Minutes)** for all 100 questions.\n"
                    "   - **For PwD / Scribe Candidates:** **1 Hour and 20 Minutes (80 Minutes)**.\n"
                    "   - **Shift Timings:** Conducted across 3 to 4 shifts daily:\n"
                    "     - Shift 1: 9:00 AM to 10:00 AM\n"
                    "     - Shift 2: 12:30 PM to 1:30 PM\n"
                    "     - Shift 3: 4:00 PM to 5:00 PM\n\n"
                    "2. **Tier-II Examination (Paper 1):**\n"
                    "   - **Session I (Written CBT):** **2 Hours and 15 Minutes (135 Minutes)**:\n"
                    "     - Section I (Maths + Reasoning): 1 Hour (60 Minutes).\n"
                    "     - Section II (English + General Awareness): 1 Hour (60 Minutes).\n"
                    "     - Section III Module 1 (Computer Knowledge): 15 Minutes.\n"
                    "   - **Session II (DEST Typing Test):** **15 Minutes** (2,000 key depressions typing test)."
                    if not is_hi else
                    "**कर्मचारी चयन आयोग (SSC CGL) - परीक्षा का समय व अवधि:**\n\n"
                    "1. **टियर-I परीक्षा (कंप्यूटर आधारित परीक्षा CBT):**\n"
                    "   - **आवंटित समय:** **1 घंटा (60 मिनट)** (100 प्रश्नों हेतु)।\n"
                    "   - **दिव्यांग (PwD) अभ्यर्थियों हेतु:** **80 मिनट**।\n"
                    "   - **शिफ्ट समय:** प्रातः 9:00 से 10:00, दोपहर 12:30 से 1:30, शाम 4:00 से 5:00।\n\n"
                    "2. **टियर-II परीक्षा (पेपर 1):**\n"
                    "   - **सत्र 1:** **2 घंटे 15 मिनट** (गणित व रीजनिंग: 1 घंटा, अंग्रेजी व सामान्य ज्ञान: 1 घंटा, कंप्यूटर: 15 मिनट)।\n"
                    "   - **सत्र 2 (टाइपिंग टेस्ट DEST):** **15 मिनट** (2000 की-डिप्रेशन टाइपिंग)।"
                ),
                "official_source": "Staff Selection Commission (https://ssc.gov.in)",
                "suggested_links": [
                    {"label": "SSC Official Portal", "url": "https://ssc.gov.in"}
                ]
            }

        # 2.4.2 Marking Scheme / Negative Marking
        if aspect == "marking":
            return {
                "title": "SSC CGL Marking Scheme & Negative Marking Rules" if not is_hi else "SSC CGL: मार्किंग स्कीम व नेगेटिव मार्किंग नियम",
                "answer": (
                    "**SSC CGL Official Marking Scheme:**\n\n"
                    "1. **Tier-I Marking Scheme (200 Marks Total):**\n"
                    "   - Correct Answer: **+2.00 Marks**.\n"
                    "   - Incorrect Answer: **-0.50 Marks (1/4th negative deduction)**.\n"
                    "   - Unattempted: **0 Marks**.\n\n"
                    "2. **Tier-II Marking Scheme (390 Marks Merit):**\n"
                    "   - **Section I & II (Maths, Reasoning, English, GA):**\n"
                    "     - Correct Answer: **+3.00 Marks**.\n"
                    "     - Incorrect Answer: **-1.00 Mark (1/3rd negative deduction)**.\n"
                    "   - **Section III (Computer Knowledge Module):** Correct: **+3 Marks**, Incorrect: **-1 Mark** (Qualifying nature, 18 marks required for UR)."
                    if not is_hi else
                    "**SSC CGL अंकन पद्धति (Marking Scheme):**\n\n"
                    "1. **टियर-I मार्किंग (कुल 200 अंक):** सही उत्तर: **+2 अंक**, गलत उत्तर: **-0.50 अंक** (1/4 नेगेटिव मार्किंग)।\n"
                    "2. **टियर-II मार्किंग (मेरिट 390 अंक):** सही उत्तर: **+3 अंक**, गलत उत्तर: **-1.00 अंक** (1/3 नेगेटिव मार्किंग)।"
                ),
                "official_source": "Staff Selection Commission (https://ssc.gov.in)",
                "suggested_links": [
                    {"label": "SSC Scheme Notice", "url": "https://ssc.gov.in"}
                ]
            }

        # 2.4.3 Eligibility / Posts / Qualification
        if aspect == "eligibility":
            return {
                "title": "SSC CGL Posts, Eligibility Criteria & Age Limits" if not is_hi else "SSC CGL: प्रमुख पद, शैक्षणिक योग्यता व आयु सीमा",
                "answer": (
                    "**Staff Selection Commission (SSC CGL) Posts & Eligibility:**\n\n"
                    "1. **Educational Qualification:**\n"
                    "   - Bachelor's Degree in ANY discipline from a recognized University or equivalent.\n"
                    "   - For Junior Statistical Officer (JSO): Degree with 60% in Mathematics at 12th standard or Statistics as a degree subject.\n\n"
                    "2. **Age Limits (Post Specific):**\n"
                    "   - Most Inspector & ASO posts: **18 to 30 Years** (e.g., ASO in CSS, Income Tax Inspector, Excise Inspector, Sub-Inspector in CBI).\n"
                    "   - Tax Assistant & Auditor posts: **18 to 27 Years**.\n"
                    "   - JSO: Up to **32 Years**.\n"
                    "   - Age relaxations: OBC (+3 years), SC/ST (+5 years), PwD (+10 years).\n\n"
                    "3. **Application Fee:** ₹100 (100% Fee Exemption for Women, SC, ST, PwD, and Ex-Servicemen)."
                    if not is_hi else
                    "**SSC CGL प्रमुख पद व पात्रता:**\n\n"
                    "1. **शैक्षणिक योग्यता:** किसी भी संकाय में स्नातक (Bachelor's Degree) उत्तीर्ण।\n"
                    "2. **आयु सीमा:** विभिन्न पदों के अनुसार **18 से 30/32 वर्ष**। आरक्षित वर्गों को नियमानुसार आयु छूट।\n"
                    "3. **प्रमुख पद:** आयकर निरीक्षक (Income Tax Inspector), जीएसटी व एक्साइज इंस्पेक्टर, केंद्रीय सचिवालय में ASO, सीबीआई में सब-इंस्पेक्टर, CAG ऑडिटर।"
                ),
                "official_source": "Staff Selection Commission (https://ssc.gov.in)",
                "suggested_links": [
                    {"label": "SSC Official Portal", "url": "https://ssc.gov.in"}
                ]
            }

        # 2.4.4 Schedule / Dates / Default Overview
        return {
            "title": "SSC CGL 2026 Official Dates & Examination Schedule" if not is_hi else "SSC CGL 2026 आधिकारिक तिथियां एवं परीक्षा कार्यक्रम",
            "answer": (
                "**Staff Selection Commission (SSC CGL 2026) Schedule & Guide:**\n\n"
                "1. **SSC CGL 2026 Official Recruitment Calendar:**\n"
                "   - **Notification & Registration:** Opens **June 2026**; Closes **July 2026** on `ssc.gov.in`.\n"
                "   - **Tier-I Exam Date (CBT):** Starts in **September – October 2026** across multiple shifts.\n"
                "   - **Tier-I Results:** Announced in **November 2026**.\n"
                "   - **Tier-II Exam Date (CBT & DEST):** Conducted in **December 2026 – January 2027**.\n\n"
                "2. **Key Target Posts:** Assistant Section Officer (ASO) in Central Secretariat, Income Tax Inspector, Central GST & Excise Inspector, Sub-Inspector in CBI/NIA, Assistant Enforcement Officer in ED, CAG Auditor.\n\n"
                "3. **Age Criteria:** 18 to 30/32 Years (post-specific). Age relaxations: SC/ST (+5 years), OBC-NCL (+3 years), PwD (+10 years).\n\n"
                "4. **Application Fee:** ₹100 (100% Fee Exemption for Women, SC, ST, PwD, and Ex-Servicemen)."
                if not is_hi else
                "**कर्मचारी चयन आयोग (SSC CGL 2026) परीक्षा कैलेंडर एवं विवरण:**\n\n"
                "1. **वर्ष 2026 भर्ती कार्यक्रम:**\n"
                "   - **अधिसूचना एवं ऑनलाइन आवेदन:** **जून 2026** से शुरू, अंतिम तिथि **जुलाई 2026**।\n"
                "   - **टियर-I कंप्यूटर परीक्षा (CBT):** **सितंबर – अक्टूबर 2026** में विभिन्न पालियों में।\n"
                "   - **टियर-I परिणाम:** **नवंबर 2026**।\n"
                "   - **टियर-II मुख्य परीक्षा एवं टाइपिंग:** **दिसंबर 2026 – जनवरी 2027**।\n\n"
                "2. **प्रमुख पद:** केंद्रीय सचिवालय में ASO, आयकर निरीक्षक (Income Tax Inspector), जीएसटी इंस्पेक्टर, सीबीआई में सब-इंस्पेक्टर, ईडी में सहायक प्रवर्तन अधिकारी।\n\n"
                "3. **आयु सीमा:** 18 से 30/32 वर्ष। आयु छूट: SC/ST (+5 वर्ष), OBC (+3 वर्ष), PwD (+10 वर्ष)।\n\n"
                "4. **आवेदन शुल्क:** ₹100 (महिला, SC, ST, PwD एवं भूतपूर्व सैनिकों हेतु पूर्णतः निःशुल्क)।"
            ),
            "official_source": "Staff Selection Commission (https://ssc.gov.in)",
            "suggested_links": [
                {"label": "SSC Official Portal", "url": "https://ssc.gov.in"},
                {"label": "SSC Annual Calendar", "url": "https://ssc.gov.in"}
            ]
        }

    # 2.5 Defense Services (NDA & CDS)
    if has_any(["nda", "cds", "defense", "defence", "army", "navy", "air force", "एनडीए", "सीडीएस"], q):
        
        # 2.5.1 Duration / Timings
        if aspect == "duration":
            return {
                "title": "UPSC NDA & CDS Exam Duration, Paper Timings & Shifts" if not is_hi else "UPSC एनडीए एवं सीडीएस: परीक्षा अवधि व पेपर टाइमिंग",
                "answer": (
                    "**UPSC National Defence Academy (NDA) & CDS Exam Duration & Paper Timings:**\n\n"
                    "1. **NDA Examination (Single Day - 5 Hours Total):**\n"
                    "   - **Paper 1 (Mathematics):** **2 Hours and 30 Minutes (150 Minutes)** from **10:00 AM to 12:30 PM** (120 Questions, 300 Marks).\n"
                    "   - **Paper 2 (General Ability Test - GAT):** **2 Hours and 30 Minutes (150 Minutes)** from **2:00 PM to 4:30 PM** (150 Questions, 600 Marks).\n\n"
                    "2. **CDS Examination (IMA / INA / AFA - 6 Hours Total; OTA - 4 Hours):**\n"
                    "   - **Paper 1 (English):** **2 Hours** from 9:00 AM to 11:00 AM (100 Marks).\n"
                    "   - **Paper 2 (General Knowledge):** **2 Hours** from 12:00 PM to 2:00 PM (100 Marks).\n"
                    "   - **Paper 3 (Elementary Mathematics):** **2 Hours** from 3:00 PM to 5:00 PM (100 Marks) *(Not required for Officers Training Academy - OTA)*."
                    if not is_hi else
                    "**UPSC एनडीए एवं सीडीएस परीक्षा का समय व अवधि:**\n\n"
                    "1. **NDA परीक्षा (एक ही दिन में 5 घंटे):**\n"
                    "   - **गणित (Mathematics):** **2 घंटे 30 मिनट**, प्रातः **10:00 से 12:30 बजे** (300 अंक)।\n"
                    "   - **सामान्य योग्यता (GAT):** **2 घंटे 30 मिनट**, दोपहर **2:00 से 4:30 बजे** (600 अंक)।\n\n"
                    "2. **CDS परीक्षा:**\n"
                    "   - अंग्रेजी: **2 घंटे** (9:00 से 11:00 AM)\n"
                    "   - सामान्य ज्ञान: **2 घंटे** (12:00 से 2:00 PM)\n"
                    "   - प्रारंभिक गणित: **2 घंटे** (3:00 से 5:00 PM) (OTA हेतु गणित आवश्यक नहीं)।"
                ),
                "official_source": "Union Public Service Commission (https://upsc.gov.in)",
                "suggested_links": [
                    {"label": "UPSC NDA/CDS Portal", "url": "https://upsc.gov.in"},
                    {"label": "Join Indian Army", "url": "https://joinindianarmy.nic.in"}
                ]
            }

        # 2.5.2 Marking Scheme / Negative Marking
        if aspect == "marking":
            return {
                "title": "NDA & CDS Marking Scheme & Negative Marking Rules" if not is_hi else "एनडीए एवं सीडीएस: मार्किंग स्कीम व नेगेटिव मार्किंग",
                "answer": (
                    "**NDA & CDS Official Marking Scheme:**\n\n"
                    "1. **NDA Marking Rules:**\n"
                    "   - **Mathematics (120 Questions, 300 Marks):** Correct: **+2.5 Marks**, Incorrect: **-0.83 Marks (1/3rd deduction)**.\n"
                    "   - **GAT (150 Questions, 600 Marks):** Correct: **+4.0 Marks**, Incorrect: **-1.33 Marks (1/3rd deduction)**.\n"
                    "   - SSB Interview: 900 Marks. Grand Total: **1,800 Marks**.\n\n"
                    "2. **CDS Marking Rules:**\n"
                    "   - Correct: +0.83 to +1.0 Mark (depending on paper); Incorrect: **1/3rd deduction (negative marking)**."
                    if not is_hi else
                    "**NDA एवं CDS मार्किंग पद्धति:**\n\n"
                    "1. **NDA अंक विभाजन:**\n"
                    "   - गणित: सही उत्तर: **+2.5 अंक**, गलत उत्तर: **-0.83 अंक**।\n"
                    "   - GAT: सही उत्तर: **+4.0 अंक**, गलत उत्तर: **-1.33 अंक** (1/3 नेगेटिव मार्किंग)।\n"
                    "   - SSB इंटरव्यू: 900 अंक। कुल योग: 1,800 अंक।"
                ),
                "official_source": "Union Public Service Commission (https://upsc.gov.in)",
                "suggested_links": [
                    {"label": "UPSC NDA Guidelines", "url": "https://upsc.gov.in"}
                ]
            }

        # 2.5.3 Eligibility / Age Limit / Educational Criteria
        if aspect in ["eligibility", "pattern", "syllabus"]:
            return {
                "title": "UPSC NDA & CDS Eligibility Criteria, Age Limits & Educational Rules" if not is_hi else "NDA एवं CDS: पात्रता मापदंड, आयु सीमा व शैक्षणिक योग्यता",
                "answer": (
                    "**UPSC National Defence Academy (NDA) & CDS Complete Eligibility Rules:**\n\n"
                    "1. **NDA Eligibility & Age Limit:**\n"
                    "   - **Age Window:** **16.5 to 19.5 Years** at commencement of course (strictly unmarried male and female candidates).\n"
                    "   - **Educational Qualification:**\n"
                    "     * **Army Wing of NDA:** 12th Class pass of the 10+2 pattern of School Education or equivalent with any stream.\n"
                    "     * **Air Force & Naval Wings of NDA / 10+2 Cadet Entry Scheme at INA:** 12th Class pass with **Physics, Chemistry, and Mathematics (PCM)**.\n"
                    "     * Candidates appearing in the 12th Class under 10+2 pattern are also eligible to apply.\n\n"
                    "2. **CDS Eligibility & Age Limit:**\n"
                    "   - **Indian Military Academy (IMA) & INA:** **19 to 24 Years**, Unmarried male candidates with a recognized Degree (Engineering degree for INA).\n"
                    "   - **Air Force Academy (AFA):** **20 to 24 Years**, Degree with Physics and Mathematics at 10+2 level OR Bachelor of Engineering.\n"
                    "   - **Officers Training Academy (OTA - Men & Women):** **19 to 25 Years**, Degree of a recognized University (Married/Unmarried).\n\n"
                    "3. **Physical & Medical Standards:** Candidates must be physically fit according to physical standards for admission to National Defence Academy and Naval Academy as per UPSC official guidelines."
                    if not is_hi else
                    "**UPSC राष्ट्रीय रक्षा अकादमी (NDA) एवं CDS संपूर्ण पात्रता नियम:**\n\n"
                    "1. **NDA आयु सीमा व पात्रता:**\n"
                    "   - **आयु सीमा:** पाठ्यक्रम प्रारंभ होने पर **16.5 से 19.5 वर्ष** (अविवाहित महिला एवं पुरुष अभ्यर्थी)।\n"
                    "   - **शैक्षणिक योग्यता:**\n"
                    "     * **थल सेना विंग (Army):** किसी भी मान्यता प्राप्त बोर्ड से 12वीं (10+2) उत्तीर्ण।\n"
                    "     * **वायु सेना (Air Force) व नौसेना (Navy) विंग:** 12वीं में **भौतिकी, रसायन विज्ञान व गणित (PCM)** अनिवार्य।\n"
                    "     * 12वीं की परीक्षा दे रहे छात्र भी आवेदन के पात्र हैं।\n\n"
                    "2. **CDS आयु सीमा व शैक्षणिक योग्यता:**\n"
                    "   - **IMA व नौसेना अकादमी:** 19 से 24 वर्ष, मान्यता प्राप्त स्नातक डिग्री।\n"
                    "   - **वायु सेना अकादमी (AFA):** 20 से 24 वर्ष, 12वीं में गणित-भौतिकी के साथ डिग्री या B.E./B.Tech।\n"
                    "   - **ऑफिसर्स ट्रेनिंग एकेडमी (OTA):** 19 से 25 वर्ष, मान्यता प्राप्त स्नातक डिग्री।"
                ),
                "official_source": "Union Public Service Commission (https://upsc.gov.in)",
                "suggested_links": [
                    {"label": "UPSC NDA Official Portal", "url": "https://upsc.gov.in"},
                    {"label": "Join Indian Army Official Portal", "url": "https://joinindianarmy.nic.in"}
                ]
            }

        # 2.5.3 Schedule / Dates / Default Overview
        return {
            "title": "UPSC NDA & CDS 2026 Official Examination Dates" if not is_hi else "UPSC एनडीए एवं सीडीएस 2026 आधिकारिक परीक्षा कार्यक्रम",
            "answer": (
                "**National Defence Academy (NDA) & Combined Defence Services (CDS 2026) Schedule:**\n\n"
                "1. **NDA & CDS (I) 2026 (Spring Cycle):**\n"
                "   - **Notification & Registration:** Opens **December 2025 / January 2026**.\n"
                "   - **Written Examination Date:** Starts in **mid-April 2026**.\n"
                "   - **SSB Interview:** Commences from **July – August 2026**.\n\n"
                "2. **NDA & CDS (II) 2026 (Autumn Cycle):**\n"
                "   - **Notification & Registration:** Opens in **May 2026**.\n"
                "   - **Written Examination Date:** Starts in **September 2026**.\n"
                "   - **SSB Interview:** Commences from **December 2026 – January 2027**.\n\n"
                "3. **Eligibility:** NDA (16.5 to 19.5 Years, Unmarried Men & Women, 10+2); CDS (19 to 24/25 Years, Degree). Full cadet training and officer stipend provided by Government of India."
                if not is_hi else
                "**राष्ट्रीय रक्षा अकादमी (NDA) एवं सीडीएस (CDS 2026) परीक्षा कार्यक्रम:**\n\n"
                "1. **NDA एवं CDS (I) 2026 (प्रथम सत्र):**\n"
                "   - **अधिसूचना व आवेदन:** **दिसंबर 2025 / जनवरी 2026**।\n"
                "   - **लिखित परीक्षा तिथि:** **अप्रैल 2026 के मध्य**।\n"
                "   - **SSB साक्षात्कार:** **जुलाई – अगस्त 2026**।\n\n"
                "2. **NDA एवं CDS (II) 2026 (द्वितीय सत्र):**\n"
                "   - **अधिसूचना व आवेदन:** **मई 2026**।\n"
                "   - **लिखित परीक्षा तिथि:** **सितंबर 2026**।\n\n"
                "3. **पात्रता:** NDA (16.5 से 19.5 वर्ष, 12वीं उत्तीर्ण, अविवाहित महिला व पुरुष); CDS (19 से 24/25 वर्ष, स्नातक)। भारत सरकार द्वारा पूर्ण सैन्य प्रशिक्षण एवं स्टाइपेंड।"
            ),
            "official_source": "Union Public Service Commission (https://upsc.gov.in)",
            "suggested_links": [
                {"label": "UPSC Official Portal", "url": "https://upsc.gov.in"},
                {"label": "Join Indian Army", "url": "https://joinindianarmy.nic.in"}
            ]
        }

    # 2.6 State Public Service Commissions (UPPSC, BPSC, MPSC, RPSC, etc.)
    if has_any(["psc", "uppsc", "mpsc", "bpsc", "kpsc", "tnpsc", "rpsc", "wbpsc", "state psc", "sdm", "dsp", "तहसीलदार", "डीएसपी", "राज्य लोक सेवा आयोग"], q):
        
        # 2.6.1 Duration & Shift Timings
        if aspect == "duration":
            return {
                "title": "State PSC (UPPSC, BPSC, MPSC) Exam Duration & Timings" if not is_hi else "राज्य लोक सेवा आयोग (UPPSC / BPSC): परीक्षा अवधि व शिफ्ट टाइमिंग",
                "answer": (
                    "**State Public Service Commissions (UPPSC / BPSC / MPSC) Examination Duration:**\n\n"
                    "1. **Preliminary Examination (Single Day - 2 Shifts):**\n"
                    "   - **Paper I (General Studies):** **2 Hours (120 Minutes)** (Morning shift: 9:30 AM to 11:30 AM).\n"
                    "   - **Paper II (CSAT / Aptitude):** **2 Hours (120 Minutes)** (Afternoon shift: 2:30 PM to 4:30 PM) - 33% qualifying.\n"
                    "   - **BPSC Note:** BPSC Preliminary Exam is conducted as a single composite paper of **2 Hours (120 Minutes)** with 150 questions.\n\n"
                    "2. **Main Examination (Descriptive):**\n"
                    "   - **Duration per paper:** **3 Hours (180 Minutes)**.\n"
                    "   - Conducted over 3 to 5 days across General Hindi, Essay, General Studies Papers, and Optional/State-specific papers."
                    if not is_hi else
                    "**राज्य लोक सेवा आयोग (UPPSC / BPSC आदि) परीक्षा अवधि व समय:**\n\n"
                    "1. **प्रारंभिक परीक्षा (Prelims):**\n"
                    "   - **पेपर I (सामान्य अध्ययन):** **2 घंटे (120 मिनट)** (सुबह 9:30 से 11:30 बजे)।\n"
                    "   - **पेपर II (CSAT क्वालीफाइंग):** **2 घंटे (120 मिनट)** (दोपहर 2:30 से 4:30 बजे)।\n"
                    "   - **BPSC विशेष:** बिहार लोक सेवा आयोग में 150 प्रश्नों का एकल पेपर 2 घंटे की अवधि का होता है।\n\n"
                    "2. **मुख्य परीक्षा (Mains):** प्रत्येक वर्णनात्मक प्रश्नपत्र हेतु **3 घंटे (180 मिनट)** का समय दिया जाता है।"
                ),
                "official_source": "Respective State Public Service Commissions",
                "suggested_links": [
                    {"label": "UPPSC Portal", "url": "https://uppsc.up.nic.in"},
                    {"label": "BPSC Portal", "url": "https://bpsc.bih.nic.in"},
                    {"label": "MPSC Portal", "url": "https://mpsc.gov.in"}
                ]
            }

        # 2.6.2 Marking Scheme & Negative Marking
        if aspect == "marking":
            return {
                "title": "State PSC Marking Scheme & Negative Marking Rules" if not is_hi else "राज्य लोक सेवा आयोग: मार्किंग स्कीम व नेगेटिव मार्किंग",
                "answer": (
                    "**State Public Service Commissions Marking Scheme & Negative Marking:**\n\n"
                    "1. **UPPSC PCS (Uttar Pradesh):**\n"
                    "   - **GS Paper I:** 150 Questions, 200 Marks (+1.33 marks per correct answer).\n"
                    "   - **Negative Marking:** **0.33 Marks (1/3rd deduction)** for every wrong response.\n"
                    "   - **CSAT Paper II:** 100 Questions, 200 Marks (+2.0 marks per correct, -0.66 per wrong). Minimum 33% (66 marks) required to qualify.\n\n"
                    "2. **BPSC CCE (Bihar):**\n"
                    "   - **Prelims:** 150 Questions, 150 Marks (+1 mark per correct answer).\n"
                    "   - **Negative Marking:** **-0.33 Marks (1/3rd negative marking)** implemented as per standard 4-option pattern.\n\n"
                    "3. **MPSC Rajyaseva (Maharashtra):**\n"
                    "   - **Negative Marking:** **1/4th (25%) deduction** per incorrect answer in objective papers."
                    if not is_hi else
                    "**राज्य लोक सेवा आयोग अंकन पद्धति व नेगेटिव मार्किंग:**\n\n"
                    "1. **UPPSC PCS (उत्तर प्रदेश):** सही उत्तर पर +1.33 अंक, प्रत्येक गलत उत्तर पर **1/3 (0.33 अंक) नेगेटिव मार्किंग**।\n"
                    "2. **BPSC (बिहार):** सही उत्तर पर +1 अंक, प्रत्येक गलत उत्तर पर **1/3 (-0.33 अंक) नेगेटिव मार्किंग**।\n"
                    "3. **MPSC (महाराष्ट्र):** प्रत्येक गलत उत्तर पर 1/4 (25%) अंक की कटौती।"
                ),
                "official_source": "Respective State Public Service Commissions",
                "suggested_links": [
                    {"label": "UPPSC Official Portal", "url": "https://uppsc.up.nic.in"},
                    {"label": "BPSC Official Portal", "url": "https://bpsc.bih.nic.in"}
                ]
            }

        # 2.6.3 Eligibility / Age Limits
        if aspect in ["eligibility", "pattern"]:
            return {
                "title": "State PSC Eligibility Criteria, Age Limits & Domicile Rules" if not is_hi else "राज्य लोक सेवा आयोग: पात्रता, आयु सीमा व डोमिसाइल नियम",
                "answer": (
                    "**State Public Service Commissions Eligibility & Age Limits:**\n\n"
                    "1. **Age Limits by State:**\n"
                    "   - **UPPSC (Uttar Pradesh):** **21 to 40 Years** (Relaxation up to 45 years for SC/ST/OBC of UP).\n"
                    "   - **BPSC (Bihar):** **20/21/22 to 37 Years** for General Male; **40 Years** for General Female & BC/EBC; **42 Years** for SC/ST.\n"
                    "   - **MPSC (Maharashtra):** **19 to 38 Years** for Open category; **43 Years** for Reserved categories.\n"
                    "   - **RPSC (Rajasthan):** **21 to 40 Years**.\n\n"
                    "2. **Educational Qualification:** Graduation Degree in any discipline from a recognized University (final year students eligible as per commission cut-off dates).\n\n"
                    "3. **Domicile & Reservation Rules:** Other state candidates can freely apply under Unreserved / General category. Reservation benefits apply strictly to state domicile residents."
                    if not is_hi else
                    "**राज्य लोक सेवा आयोग (State PSCs) पात्रता एवं आयु सीमा:**\n\n"
                    "1. **प्रमुख राज्यों में आयु सीमा:**\n"
                    "   - **UPPSC (उत्तर प्रदेश):** **21 से 40 वर्ष** (UP के आरक्षित वर्गों हेतु 45 वर्ष तक)।\n"
                    "   - **BPSC (बिहार):** **21 से 37 वर्ष** (अनारक्षित पुरुष); महिलाओं व BC/EBC हेतु **40 वर्ष**; SC/ST हेतु **42 वर्ष**।\n"
                    "   - **MPSC (महाराष्ट्र):** **19 से 38 वर्ष** (खुले वर्ग हेतु); आरक्षित वर्गों हेतु **43 वर्ष**।\n\n"
                    "2. **शैक्षणिक योग्यता:** किसी भी मान्यता प्राप्त विश्वविद्यालय से स्नातक (Graduation) की डिग्री।\n\n"
                    "3. **डोमिसाइल नियम:** अन्य राज्यों के अभ्यर्थी सामान्य श्रेणी (General/Unreserved) में आवेदन कर सकते हैं।"
                ),
                "official_source": "Respective State Public Service Commissions",
                "suggested_links": [
                    {"label": "State Directory Portal", "url": "/state-directory"},
                    {"label": "UPPSC Portal", "url": "https://uppsc.up.nic.in"},
                    {"label": "BPSC Portal", "url": "https://bpsc.bih.nic.in"}
                ]
            }

        # 2.6.4 Schedule / Dates / Default Overview
        return {
            "title": "State Civil Services (State PSCs 2026) Schedules & Rules" if not is_hi else "राज्य लोक सेवा आयोग (State PSCs 2026) परीक्षा तिथियां एवं गाइड",
            "answer": (
                "**State Public Service Commissions (UPPSC / BPSC / MPSC / RPSC 2026) Schedules:**\n\n"
                "1. **2026 State Exam Timelines:**\n"
                "   - **UPPSC PCS 2026 (Uttar Pradesh):** Prelims in **March / April 2026**, Mains in **July 2026**.\n"
                "   - **BPSC CCE 2026 (Bihar):** Fixed annual calendar with Prelims on **September 30, 2026**, Mains in **January 2027**.\n"
                "   - **MPSC Rajyaseva 2026 (Maharashtra):** Prelims in **April / May 2026**, Mains in **September 2026**.\n"
                "   - **RPSC RAS 2026 (Rajasthan):** Prelims in **June / July 2026**.\n\n"
                "2. **Key Administrative Posts:** Sub-Divisional Magistrate (SDM / Deputy Collector), Deputy Superintendent of Police (DSP), Block Development Officer (BDO), Naib Tehsildar, Commercial Tax Officer.\n\n"
                "3. **Age Limits:** Generally **21 to 40 Years** (UP, Bihar, MP, Rajasthan); **19 to 38 Years** in Maharashtra. State domicile reservation applies."
                if not is_hi else
                "**राज्य लोक सेवा आयोग (UPPSC / BPSC / MPSC आदि 2026) परीक्षा कार्यक्रम:**\n\n"
                "1. **वर्ष 2026 परीक्षा तिथियां:**\n"
                "   - **UPPSC PCS (उत्तर प्रदेश):** प्रारंभिक परीक्षा **मार्च/अप्रैल 2026**, मुख्य परीक्षा **जुलाई 2026**।\n"
                "   - **BPSC CCE (बिहार):** निश्चित कैलेंडर अनुसार प्रारंभिक परीक्षा **30 सितंबर 2026**, मुख्य परीक्षा **जनवरी 2027**।\n"
                "   - **MPSC राज्यसेवा (महाराष्ट्र):** प्रारंभिक परीक्षा **अप्रैल/मई 2026**, मुख्य परीक्षा **सितंबर 2026**।\n"
                "   - **RPSC RAS (राजस्थान):** प्रारंभिक परीक्षा **जून/जुलाई 2026**।\n\n"
                "2. **प्रमुख पद:** उप-जिलाधिकारी (SDM / डिप्टी कलेक्टर), पुलिस उपाधीक्षक (DSP), बीडीओ (BDO), नायब तहसीलदार।\n\n"
                "3. **आयु सीमा:** सामान्यतः **21 से 40 वर्ष** (UP, बिहार, राजस्थान); महाराष्ट्र में **19 से 38 वर्ष**।"
            ),
            "official_source": "Respective State Public Service Commissions",
            "suggested_links": [
                {"label": "Select State for State PSC Portal", "url": "/state-directory"},
                {"label": "UPPSC Portal", "url": "https://uppsc.up.nic.in"},
                {"label": "MPSC Portal", "url": "https://mpsc.gov.in"},
                {"label": "BPSC Portal", "url": "https://bpsc.bih.nic.in"}
            ]
        }

    # 2.7 General 2026 Competitive Exams Calendar Query
    if has_any(["competitive exam", "sarkari exam", "सरकारी नौकरी", "competitive exams", "sarkari exams", "exam calendar", "2026 exam", "2026 exams"], q) or (has_any(["exam", "exams", "परीक्षा"], q) and not has_any(["scholarship", "caste", "voter", "driving", "license", "birth", "kisan", "awas", "ayushman"], q)):
        return {
            "title": "National Competitive Examinations 2026 Official Calendar" if not is_hi else "प्रमुख राष्ट्रीय प्रतियोगी परीक्षाएं 2026 वार्षिक कैलेंडर",
            "answer": (
                "**Government of India Competitive Examinations 2026 Master Calendar:**\n\n"
                "1. ⚙️ **JEE Main 2026 (NTA):**\n"
                "   - Session 1: **January 22 – 31, 2026** (Registration: Nov-Dec 2025)\n"
                "   - Session 2: **April 1 – 15, 2026** (Registration: Feb-Mar 2026)\n"
                "   - JEE Advanced 2026: **May 2026** (Organized by IITs)\n\n"
                "2. 🩺 **NEET-UG 2026 (NTA):**\n"
                "   - Single national exam: **Sunday, May 3, 2026** (Registration: Feb-Mar 2026)\n\n"
                "3. 🏛️ **UPSC Civil Services CSE 2026:**\n"
                "   - Notification: **February 2026**\n"
                "   - Preliminary Exam: **Late May 2026 (May 24/31, 2026)**\n"
                "   - Mains Exam: **September 2026** (5-day written descriptive)\n\n"
                "4. 💼 **SSC CGL 2026:**\n"
                "   - Notification: **June 2026** | Tier-I Exam: **September – October 2026**\n\n"
                "5. 🎖️ **UPSC NDA & CDS 2026:**\n"
                "   - Cycle I Exam: **April 2026** | Cycle II Exam: **September 2026**\n\n"
                "6. 🏢 **State PSCs (UPPSC, BPSC, MPSC):** Prelims scheduled from **March to September 2026**.\n\n"
                "⚠️ *Complete fee exemption applies for Female, SC, ST, and PwD candidates across UPSC and SSC.*"
                if not is_hi else
                "**भारत सरकार की प्रमुख प्रतियोगी परीक्षाओं का 2026 वार्षिक कैलेंडर:**\n\n"
                "1. ⚙️ **जेईई मेन 2026 (NTA):**\n"
                "   - सत्र 1 परीक्षा: **22 से 31 जनवरी 2026** (पंजीकरण: नवं-दिसं 2025)\n"
                "   - सत्र 2 परीक्षा: **1 से 15 अप्रैल 2026** (पंजीकरण: फर-मार्च 2026)\n"
                "   - जेईई एडवांस्ड: **मई 2026**\n\n"
                "2. 🩺 **नीट-यूजी 2026 (NEET-UG):**\n"
                "   - परीक्षा तिथि: **रविवार, 3 मई 2026** (पंजीकरण: फरवरी-मार्च 2026)\n\n"
                "3. 🏛️ **UPSC सिविल सेवा (IAS/IPS 2026):**\n"
                "   - अधिसूचना: **फरवरी 2026**\n"
                "   - प्रारंभिक परीक्षा (Prelims): **मई 2026 के अंत में (24/31 मई 2026)**\n"
                "   - मुख्य परीक्षा (Mains): **सितंबर 2026**\n\n"
                "4. 💼 **SSC CGL 2026:**\n"
                "   - अधिसूचना: **जून 2026** | टियर-I परीक्षा: **सितंबर – अक्टूबर 2026**\n\n"
                "5. 🎖️ **NDA एवं CDS 2026:** प्रथम सत्र **अप्रैल 2026** | द्वितीय सत्र **सितंबर 2026**\n\n"
                "⚠️ *UPSC एवं SSC में महिला, SC, ST एवं दिव्यांग अभ्यर्थियों हेतु आवेदन शुल्क पूर्णतः शून्य है।*"
            ),
            "official_source": "UPSC, SSC, NTA Official Calendars",
            "suggested_links": [
                {"label": "UPSC Official Portal", "url": "https://upsc.gov.in"},
                {"label": "SSC Official Portal", "url": "https://ssc.gov.in"},
                {"label": "NTA Official Portal", "url": "https://nta.ac.in"}
            ]
        }

    # =========================================================================
    # 3. NATIONAL WELFARE SCHEMES INTENT (With 2026 Installments & Schedules)
    # =========================================================================
    
    # 3.1 PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)
    if has_any(["pm kisan", "pm-kisan", "pmkisan", "kisan samman", "किसान सम्मान निधि", "पीएम किसान", "kisan kist", "kisan installment"], q):
        return {
            "title": "PM-KISAN 2026 Installment Schedule & Payment Dates" if not is_hi else "पीएम-किसान (PM-KISAN 2026) किस्त जारी होने की तिथियां व कैलेंडर",
            "answer": (
                "**Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) - 2026 Release Schedule:**\n\n"
                "1. **Financial Benefit:** ₹6,000 per year directly transferred to farmer families in **3 equal installments of ₹2,000 every 4 months** via Aadhaar-DBT.\n\n"
                "2. **Official 2026 Installment Release Calendar:**\n"
                "   - 🌾 **Period 1 Installment (April – July 2026):** Released in **May / June 2026**.\n"
                "   - 🌾 **Period 2 Installment (August – November 2026):** Released in **October / November 2026**.\n"
                "   - 🌾 **Period 3 Installment (December 2026 – March 2027):** Released in **February / March 2027**.\n\n"
                "3. **3 Mandatory Requirements to Receive 2026 Installments:**\n"
                "   - **Aadhaar e-KYC:** Complete biometric/facial authentication on the PM-Kisan mobile app or `pmkisan.gov.in`.\n"
                "   - **Land Record Seeding:** Verification of agricultural landownership (Khatauni/Khasra/ROR) by the local Patwari/Tehsildar.\n"
                "   - **NPCI Aadhaar Mapping:** Active bank account must be mapped with Aadhaar in the NPCI server for Direct Benefit Transfer.\n\n"
                "4. **Beneficiary Status Check:** Visit `pmkisan.gov.in` -> **'Know Your Status'** and enter your Registration Number."
                if not is_hi else
                "**प्रधानमंत्री किसान सम्मान निधि (PM-KISAN) - वर्ष 2026 किस्त कार्यक्रम:**\n\n"
                "1. **योजना का लाभ:** प्रति वर्ष ₹6,000 की वित्तीय सहायता **₹2,000 की 3 समान किस्तों** में सीधे आधार लिंक बैंक खाते में DBT द्वारा।\n\n"
                "2. **वर्ष 2026 किस्त जारी होने का कैलेंडर:**\n"
                "   - 🌾 **प्रथम किस्त (अप्रैल – जुलाई 2026 अवधि):** **मई / जून 2026** में जारी।\n"
                "   - 🌾 **द्वितीय किस्त (अगस्त – नवंबर 2026 अवधि):** **अक्टूबर / नवंबर 2026** में जारी।\n"
                "   - 🌾 **तृतीय किस्त (दिसंबर 2026 – मार्च 2027 अवधि):** **फरवरी / मार्च 2027** में जारी।\n\n"
                "3. **किस्त राशि पाने हेतु 3 अनिवार्य शर्तें:**\n"
                "   - **आधार ई-केवाईसी (e-KYC):** पीएम-किसान पोर्टल या ऐप पर फेस/ओटीपी ऑथेंटिकेशन पूर्ण होना चाहिए।\n"
                "   - **भू-अभिलेख सत्यापन (Land Seeding):** जमीन के दस्तावेजों का स्थानीय पटवारी/तहसील से सत्यापन।\n"
                "   - **बैंक खाता NPCI मैपिंग:** बैंक खाता आधार से डीबीटी हेतु सक्रिय होना अनिवार्य है।\n\n"
                "4. **किस्त स्थिति देखें:** `pmkisan.gov.in` पर जाकर **'Know Your Status'** में अपना रजिस्ट्रेशन नंबर दर्ज करें।"
            ),
            "official_source": "Ministry of Agriculture and Farmers Welfare (https://pmkisan.gov.in)",
            "suggested_links": [
                {"label": "PM-Kisan Official Portal", "url": "https://pmkisan.gov.in"},
                {"label": "Check PM-Kisan Beneficiary Status", "url": "https://pmkisan.gov.in"}
            ]
        }

    # 3.2 Ayushman Bharat (PM-JAY & Ayushman Vay Vandana 70+)
    if has_any(["ayushman", "pmjay", "pm-jay", "golden card", "health card", "आयुष्मान", "वय वंदना", "vay vandana", "70+ health"], q):
        return {
            "title": "Ayushman Bharat PM-JAY & Vay Vandana 2026 Enrollment & Dates" if not is_hi else "आयुष्मान भारत PM-JAY एवं वय वंदना कार्ड 2026 आवेदन व तिथियां",
            "answer": (
                "**Ayushman Bharat PM-JAY & Senior Citizen (70+) Vay Vandana Card 2026:**\n\n"
                "1. **Application & Enrollment Dates:**\n"
                "   - **Open 24x7 / 365 Days Year-Round:** There is **NO closing date or deadline**. Eligible citizens can generate their golden Ayushman Card anytime throughout 2026.\n\n"
                "2. **Coverage & Free Hospital Benefits:**\n"
                "   - **₹5,00,000 Cashless Health Cover** per family per year for secondary and tertiary hospitalization across 27,000+ empaneled government and private hospitals across India.\n\n"
                "3. **Major 2024-2026 Expansion - Ayushman Vay Vandana (Age 70+):**\n"
                "   - **All Senior Citizens aged 70 and above** (regardless of income, caste, or economic status) are entitled to a dedicated **Ayushman Vay Vandana Card** with independent ₹5 Lakhs annual healthcare cover.\n\n"
                "4. **How to Generate Card Online in 2 Minutes:**\n"
                "   - Download the official **'Ayushman App'** from Google Play Store or visit `beneficiary.nha.gov.in`.\n"
                "   - Login via mobile OTP, search your family details via Aadhaar or Ration Card, complete Aadhaar Face e-KYC, and instantly download the digital card."
                if not is_hi else
                "**आयुष्मान भारत PM-JAY एवं 70+ वरिष्ठ नागरिक वय वंदना कार्ड 2026:**\n\n"
                "1. **आवेदन एवं रजिस्ट्रेशन तिथियां:**\n"
                "   - **वर्ष 2026 में 365 दिन 24x7 सतत खुला है:** कोई अंतिम तिथि नहीं है। पात्र नागरिक वर्ष भर कभी भी अपना कार्ड बनवा सकते हैं।\n\n"
                "2. **स्वास्थ्य बीमा कवरेज:**\n"
                "   - प्रति परिवार प्रति वर्ष **₹5,00,000 का पूर्णतः कैशलेस व मुफ्त इलाज** देश भर के 27,000+ सरकारी एवं निजी सूचीबद्ध अस्पतालों में।\n\n"
                "3. **70 वर्ष से अधिक आयु के वरिष्ठ नागरिकों हेतु विशेष लाभ (वय वंदना):**\n"
                "   - 70 वर्ष या उससे अधिक आयु के सभी नागरिकों को आय सीमा के बिना ₹5 लाख का अलग से वार्षिक स्वास्थ्य बीमा उपलब्ध है।\n\n"
                "4. **घर बैठे कार्ड बनाने की प्रक्रिया:**\n"
                "   - गूगल प्ले स्टोर से **'Ayushman App'** डाउनलोड करें अथवा `beneficiary.nha.gov.in` पर जाएं।\n"
                "   - आधार नंबर द्वारा सर्च कर आधार फेस ऑथेंटिकेशन पूर्ण करें और तुरंत डिजिटल कार्ड डाउनलोड करें।"
            ),
            "official_source": "National Health Authority (https://pmjay.gov.in / https://beneficiary.nha.gov.in)",
            "suggested_links": [
                {"label": "Ayushman Beneficiary Portal", "url": "https://beneficiary.nha.gov.in"},
                {"label": "PM-JAY Official Portal", "url": "https://pmjay.gov.in"}
            ]
        }

    # 3.3 PM Awas Yojana (PMAY Urban 2.0 & Gramin)
    if has_any(["pm awas", "pmay", "awas yojana", "pmay-g", "pmay-u", "आवास योजना", "प्रधानमंत्री आवास"], q):
        return {
            "title": "PM Awas Yojana (PMAY 2.0 Urban & Gramin) 2026 Schedule & Guidelines" if not is_hi else "प्रधानमंत्री आवास योजना (PMAY 2.0) 2026 आवेदन प्रक्रिया एवं तिथियां",
            "answer": (
                "**Pradhan Mantri Awas Yojana (PMAY 2.0 - Urban & Gramin) 2026:**\n\n"
                "1. **2026 Rollout & Expansion:**\n"
                "   - Union Cabinet approved **PMAY 2.0 (2024–2029)** to construct **3 Crore additional houses** (2 Crore under PMAY-Gramin, 1 Crore under PMAY-Urban).\n   - Applications and beneficiary surveys are actively running **throughout 2026**.\n\n"
                "2. **Financial Benefits & Subsidies:**\n"
                "   - **PMAY-Gramin:** Direct grant of **₹1,20,000** (plain areas) to **₹1,30,000** (hilly/NE states) directly via DBT, plus 90 days of MGNREGA wages (approx ₹25,000) and ₹12,000 for toilet construction.\n"
                "   - **PMAY-Urban 2.0:** Interest Subsidy Scheme (ISS) of up to **₹2,67,000** on home loans for EWS/LIG families, and ₹2.50 Lakhs for Beneficiary-Led Construction (BLC).\n\n"
                "3. **How to Apply in 2026:**\n"
                "   - **Rural:** Verified through Gram Sabha and Awas+ mobile app survey.\n"
                "   - **Urban:** Apply online via municipal ULB portals or `pmaymis.gov.in`."
                if not is_hi else
                "**प्रधानमंत्री आवास योजना (PMAY 2.0 शहरी एवं ग्रामीण) 2026 विवरण:**\n\n"
                "1. **वर्ष 2026 में योजना की स्थिति:**\n"
                "   - केंद्रीय मंत्रिमंडल द्वारा **3 करोड़ अतिरिक्त नए पक्के मकानों** (2 करोड़ ग्रामीण, 1 करोड़ शहरी) के निर्माण की स्वीकृति के साथ वर्ष 2026 में आवेदन व सर्वे निरंतर जारी है।\n\n"
                "2. **वित्तीय सहायता एवं सब्सिडी:**\n"
                "   - **PMAY-ग्रामीण:** **₹1,20,000 से ₹1,30,000** की प्रत्यक्ष बैंक सहायता + 90 दिन की मनरेगा मजदूरी (लगभग ₹25,000) + ₹12,000 शौचालय अनुदान।\n"
                "   - **PMAY-शहरी 2.0:** गृह ऋण पर **₹2,67,000 तक की ब्याज सब्सिडी (Interest Subsidy)** अथवा पक्का मकान बनाने हेतु ₹2.5 लाख अनुदान।\n\n"
                "3. **आवेदन प्रक्रिया:** ग्रामीण क्षेत्रों में ग्राम पंचायत/आवास+ सर्वे द्वारा तथा शहरी क्षेत्रों में `pmaymis.gov.in` एवं नगर पालिका द्वारा ऑनलाइन।"
            ),
            "official_source": "Ministry of Housing and Urban Affairs & MoRD (https://pmaymis.gov.in)",
            "suggested_links": [
                {"label": "PMAY Urban Portal", "url": "https://pmaymis.gov.in"},
                {"label": "PMAY Gramin Portal", "url": "https://pmayg.nic.in"}
            ]
        }

    # 3.4 PM Vishwakarma Scheme
    if has_any(["vishwakarma", "pm vishwakarma", "विश्वकर्मा", "artisan loan", "toolkit"], q):
        return {
            "title": "PM Vishwakarma Scheme 2026 Dates, Registration & Benefits" if not is_hi else "प्रधानमंत्री विश्वकर्मा योजना 2026 पंजीकरण, तिथियां एवं लाभ",
            "answer": (
                "**PM Vishwakarma Scheme (Support for Artisans & Craftspeople) 2026:**\n\n"
                "1. **2026 Enrollment Schedule:**\n"
                "   - Operational from 2023–24 through 2027–28. Registration is **continuously open 24x7 throughout 2026** at Common Service Centers (CSCs) and `pmvishwakarma.gov.in`.\n\n"
                "2. **Core Financial & Skill Benefits:**\n"
                "   - **PM Vishwakarma Certificate & Digital ID Card.**\n"
                "   - **₹15,000 Modern Toolkit Incentive** (credited directly via e-RUPI / DBT).\n"
                "   - **Skill Training:** 5-7 days Basic Training & 15+ days Advanced Training with **₹500/day stipend**.\n"
                "   - **Collateral-Free Enterprise Loans:** 1st tranche up to **₹1,00,000** (repayable in 18 months); 2nd tranche up to **₹2,00,000** (repayable in 30 months) at **concessional 5% interest rate**.\n\n"
                "3. **18 Eligible Trades:** Carpenters (Suthar), Blacksmiths (Lohar), Goldsmiths (Sonar), Potters (Kumhaar), Cobblers (Charmakar), Masons (Rajmistri), Tailors (Darzi), Barbers (Naai), Washermen (Dhobi), Fishermen, etc.\n\n"
                "4. **How to Apply:** Visit your nearest CSC (Common Service Center) with Aadhaar, Active Bank Passbook, and Trade Details."
                if not is_hi else
                "**प्रधानमंत्री विश्वकर्मा योजना 2026 पंजीकरण एवं लाभ विवरण:**\n\n"
                "1. **वर्ष 2026 में आवेदन की स्थिति:**\n"
                "   - यह योजना 2027–28 तक क्रियान्वित है। वर्ष 2026 में कॉमन सर्विस सेंटर्स (CSCs) पर **निःशुल्क पंजीकरण निरंतर खुला है**।\n\n"
                "2. **प्रमुख वित्तीय एवं प्रशिक्षण लाभ:**\n"
                "   - **विश्वकर्मा प्रमाण पत्र एवं पहचान पत्र।**\n"
                "   - **₹15,000 का आधुनिक टूलकिट अनुदान** (सीधे बैंक खाते में)।\n"
                "   - **कौशल प्रशिक्षण:** बुनियादी एवं उन्नत प्रशिक्षण के दौरान **₹500 प्रतिदिन स्टाइपेंड**।\n"
                "   - **सस्ता ऋण (Loan):** पहले चरण में **₹1,00,000** तथा दूसरे चरण में **₹2,00,000** का बिना गारंटी का ऋण मात्र **5% रियायती ब्याज दर** पर।\n\n"
                "3. **पात्र 18 पारंपरिक व्यवसाय:** बढ़ई, लोहार, सुनार, कुम्हार, मोची, राजमिस्त्री, दर्जी, नाई, धोबी, मूर्तिकार आदि।\n\n"
                "4. **आवेदन कैसे करें:** अपने नजदीकी CSC केंद्र पर आधार कार्ड व बैंक पासबुक ले जाकर निःशुल्क बायोमेट्रिक सत्यापन कराएं।"
            ),
            "official_source": "Ministry of MSME (https://pmvishwakarma.gov.in)",
            "suggested_links": [
                {"label": "PM Vishwakarma Official Portal", "url": "https://pmvishwakarma.gov.in"},
                {"label": "Find Nearest CSC Center", "url": "https://locator.csccloud.in"}
            ]
        }

    # 3.5 PM Ujjwala Yojana 2.0
    if has_any(["ujjwala", "pmuy", "lpg connection", "gas connection", "उज्ज्वला", "गैस कनेक्शन"], q):
        return {
            "title": "PM Ujjwala Yojana 2.0 (PMUY) 2026 Free LPG Connection" if not is_hi else "प्रधानमंत्री उज्ज्वला योजना 2.0 (PMUY) 2026 मुफ्त गैस कनेक्शन गाइड",
            "answer": (
                "**Pradhan Mantri Ujjwala Yojana 2.0 (PMUY 2.0) in 2026:**\n\n"
                "1. **Application Timeline:**\n"
                "   - Open year-round throughout 2026 across all authorized LPG distributors (Indane, Bharatgas, HP Gas) and online at `pmuy.gov.in`.\n\n"
                "2. **Benefits Provided:**\n"
                "   - **100% Deposit-Free LPG connection** in the name of an adult woman of the household.\n"
                "   - **First LPG cylinder refill + Gas stove (hotplate) completely FREE of cost.**\n"
                "   - **Targeted Subsidy:** Direct Benefit Transfer of **₹300 per 14.2 kg cylinder** (up to 12 refills per year) directly credited into the woman's bank account.\n\n"
                "3. **Eligibility & Documents:** Adult female member of poor households (BPL/SC/ST/Antyodaya). Requires Aadhaar of applicant & adult family members, Ration Card, and bank account details."
                if not is_hi else
                "**प्रधानमंत्री उज्ज्वला योजना 2.0 (PMUY) 2026 विवरण:**\n\n"
                "1. **आवेदन की समयसीमा:**\n"
                "   - वर्ष 2026 में सभी एलपीजी वितरकों (Indane, Bharatgas, HP Gas) एवं `pmuy.gov.in` पर आवेदन वर्ष भर खुले हैं।\n\n"
                "2. **योजना के लाभ:**\n"
                "   - परिवार की वयस्क महिला के नाम पर **पूर्णतः निःशुल्क गैस कनेक्शन**।\n"
                "   - **पहला सिलेंडर रीफिल एवं गैस चूल्हा बिल्कुल मुफ्त**।\n"
                "   - प्रति सिलेंडर **₹300 की लक्षित सब्सिडी** सीधे बैंक खाते में (प्रति वर्ष 12 सिलेंडर तक)।\n\n"
                "3. **पात्रता:** गरीब परिवारों (SC/ST/BPL/अंत्योदय) की 18+ आयु की महिला। आधार कार्ड, राशन कार्ड व बैंक खाता अनिवार्य।"
            ),
            "official_source": "Ministry of Petroleum and Natural Gas (https://pmuy.gov.in)",
            "suggested_links": [
                {"label": "PM Ujjwala Official Portal", "url": "https://pmuy.gov.in"}
            ]
        }

    # =========================================================================
    # 4. SCHOLARSHIPS INTENT (With 2026-27 Academic Calendar Dates)
    # =========================================================================
    if (has_any(["scholarship", "scholarships", "nsp", "छात्रवृत्ति", "yasasvi", "pragati", "saksham", "inspire", "dbt", "npci", "post matric", "pre matric", "csss", "mahadbt", "medhasoft", "ssp karnataka"], q) 
            or (has_word("scholarship", q) and has_any(["exam", "eligibility", "income", "form", "apply", "date", "dates", "schedule", "when"], q))):
        
        return {
            "title": "National Scholarships Portal (NSP 2026-27) Official Schedule & Schemes" if not is_hi else "राष्ट्रीय छात्रवृत्ति पोर्टल (NSP 2026-27) आधिकारिक तिथियां एवं योजनाएं",
            "answer": (
                "**National Scholarship Portal (NSP 2026-27 Academic Year) Schedule & Dates:**\n\n"
                "1. **Official Annual Timeline for Applications:**\n"
                "   - 📅 **Portal Opens for Fresh & Renewal Applications:** **July / August 2026** on `scholarships.gov.in`.\n"
                "   - 📅 **Closing Date for Student Online Submission:** **October 31 – November 30, 2026** (scheme-wise).\n"
                "   - 📅 **Institute Level Verification (L1):** By **December 15, 2026**.\n"
                "   - 📅 **State Nodal Officer Verification (L2):** By **December 31, 2026 – January 15, 2027**.\n"
                "   - 💰 **DBT Scholarship Disbursement to Bank:** Starts from **February to April 2027**.\n"
                "   - 📱 **NSP OTR (One Time Registration) via Face Auth:** **Open 24x7 / 365 Days continuously**!\n\n"
                "2. **Top Central Scholarship Schemes:**\n"
                "   - **Post-Matric Scholarships (SC/ST/OBC):** Up to 100% tuition reimbursement + maintenance allowance (< ₹2.5L income).\n"
                "   - **Central Sector CSSS (Class 12 Merit):** ₹12,000/yr (UG) & ₹20,000/yr (PG) (< ₹4.5L income).\n"
                "   - **AICTE Pragati for Girls:** ₹50,000/year for Technical Degree/Diploma students (< ₹8L income).\n"
                "   - **PM-YASASVI (OBC/EBC/DNT):** School & Top-Class college education grants.\n\n"
                "3. **Mandatory Action:** Link your bank account in the **NPCI mapper** with Aadhaar for seamless DBT credit."
                if not is_hi else
                "**राष्ट्रीय छात्रवृत्ति पोर्टल (NSP 2026-27 शैक्षणिक सत्र) आवेदन कैलेंडर व योजनाएं:**\n\n"
                "1. **आधिकारिक वार्षिक समय-सारणी:**\n"
                "   - 📅 **पोर्टल खुलने की तिथि:** **जुलाई / अगस्त 2026** (`scholarships.gov.in` पर)।\n"
                "   - 📅 **छात्रों हेतु आवेदन की अंतिम तिथि:** **31 अक्टूबर से 30 नवंबर 2026** (योजनानुसार)।\n"
                "   - 📅 **संस्थान स्तर (L1) सत्यापन:** **15 दिसंबर 2026** तक।\n"
                "   - 📅 **राज्य नोडल अधिकारी (L2) सत्यापन:** **जनवरी 2027** तक।\n"
                "   - 💰 **छात्रवृत्ति राशि का बैंक खाते में अंतरण (DBT):** **फरवरी से अप्रैल 2027** के मध्य।\n"
                "   - 📱 **NSP OTR (वन टाइम रजिस्ट्रेशन):** वर्ष भर 365 दिन सतत खुला है।\n\n"
                "2. **प्रमुख राष्ट्रीय छात्रवृत्तियां:**\n"
                "   - **पोस्ट-मैट्रिक छात्रवृत्ति (SC/ST/OBC):** पूर्ण शिक्षण शुल्क प्रतिपूर्ति + निर्वाह भत्ता (< ₹2.5 लाख आय)।\n"
                "   - **सेंट्रल सेक्टर CSSS (12वीं मेरिट):** स्नातक हेतु ₹12,000/वर्ष एवं स्नातकोत्तर हेतु ₹20,000/वर्ष (< ₹4.5 लाख आय)।\n"
                "   - **AICTE प्रगति (बालिकाओं हेतु):** तकनीकी शिक्षा हेतु ₹50,000 प्रति वर्ष।\n"
                "   - **पीएम-यशस्वी:** OBC/EBC/DNT छात्रों हेतु टॉप क्लास कॉलेज शिक्षा सहायता।\n\n"
                "3. **अनिवार्य शर्त:** छात्रवृत्ति राशि पाने हेतु अपने बैंक खाते को **NPCI मैपर (आधार सीडिंग)** से अवश्य लिंक रखें।"
            ),
            "official_source": "Ministry of Education & MoSJE (https://scholarships.gov.in)",
            "suggested_links": [
                {"label": "NSP Official Portal", "url": "https://scholarships.gov.in"},
                {"label": "Explore All Scholarships on CivicGuide AI", "url": "/scholarships"}
            ]
        }

    # =========================================================================
    # 5. CASTE CERTIFICATE INTENT
    # =========================================================================
    if has_any(["caste", "jati", "जाति", "obc", "sc", "st", "ews", "creamy layer", "non creamy", "क्रीमी लेयर", "non-creamy", "जाति प्रमाण"], q):
        if has_any(["obc", "creamy", "non-creamy", "ncl", "क्रीमी"], q):
            return {
                "title": "OBC Non-Creamy Layer (NCL) Certificate Guide" if not is_hi else "ओबीसी गैर-क्रीमी लेयर (OBC-NCL) प्रमाण पत्र गाइड",
                "answer": (
                    "**OBC-NCL Criteria & Rules (DoPT Guidelines):**\n\n"
                    "1. **Income Ceiling:** Gross annual parental income must be **strictly under ₹8,00,000** for the preceding 3 consecutive financial years (income from agriculture & salary excluded as per DoPT OM).\n"
                    "2. **Validity:** Valid for **1 Financial Year** (1 April to 31 March). For exams like UPSC/NEET/JEE 2026, certificates must be issued on or after April 1, 2025/2026.\n"
                    "3. **Creamy Layer Exclusions:** Children of Constitutional post holders, Group A/Class 1 officers, or Group B officers entered before age 40.\n"
                    "4. **Central vs State List:** For Central jobs/exams (UPSC, SSC, IITs, AIIMS), your caste must appear on the **Central OBC List** at `ncbc.nic.in` in Central Government Annexure format."
                    if not is_hi else
                    "**ओबीसी गैर-क्रीमी लेयर (OBC-NCL) नियम व मानदंड:**\n\n"
                    "1. **आय सीमा:** माता-पिता की पिछले 3 वित्तीय वर्षों में सकल वार्षिक आय **₹8,00,000 से कम** होनी चाहिए।\n"
                    "2. **वैधता अवधि:** केवल **1 वित्तीय वर्ष** (1 अप्रैल से 31 मार्च) हेतु मान्य। प्रतियोगी परीक्षाओं (UPSC/NEET/JEE 2026) हेतु 1 अप्रैल के बाद जारी प्रमाण पत्र आवश्यक होता है।\n"
                    "3. **क्रीमी लेयर अपवर्जन:** संवैधानिक पदों, ग्रुप A/क्लास 1 अधिकारियों या 40 वर्ष से पूर्व नियुक्त ग्रुप B अधिकारियों की संतानें अपात्र हैं।\n"
                    "4. **केंद्रीय सूची:** केंद्रीय नौकरियों (UPSC/SSC/IITs) हेतु जाति `ncbc.nic.in` की केंद्रीय सूची में होनी चाहिए।"
                ),
                "official_source": "NCBC & DoPT (https://ncbc.nic.in / https://dopt.gov.in)",
                "suggested_links": [
                    {"label": "Caste Certificate Full Guide", "url": "/caste-certificate"},
                    {"label": "Central OBC List (NCBC)", "url": "https://ncbc.nic.in"}
                ]
            }

        if has_any(["ews", "ईडब्ल्यूएस", "economically weaker"], q):
            return {
                "title": "EWS (Economically Weaker Section) Certificate Guide" if not is_hi else "ईडब्ल्यूएस (EWS) प्रमाण पत्र गाइड",
                "answer": (
                    "**EWS Certificate Criteria (103rd Constitutional Amendment):**\n\n"
                    "1. **Eligibility:** General/Unreserved category citizens not covered under SC/ST/OBC quotas.\n"
                    "2. **Income Limit:** Gross annual family income **below ₹8,00,000** from all sources for the financial year prior to application.\n"
                    "3. **Asset Disqualifications:**\n"
                    "   - Agricultural land of 5 acres or above.\n"
                    "   - Residential flat of 1,000 sq. ft. or above.\n"
                    "   - Residential plot of 100 sq. yards in notified municipalities (or 200 sq. yards in non-notified areas).\n"
                    "4. **Validity:** Valid for **1 Financial Year**."
                    if not is_hi else
                    "**ईडब्ल्यूएस (EWS) प्रमाण पत्र मानदंड (103वां संविधान संशोधन):**\n\n"
                    "1. **पात्रता:** सामान्य/अनारक्षित वर्ग के नागरिक जो SC/ST/OBC आरक्षण के दायरे में नहीं आते।\n"
                    "2. **आय सीमा:** परिवार की कुल वार्षिक आय **₹8,00,000 से कम**।\n"
                    "3. **संपत्ति सीमाएं (अपात्रता):**\n"
                    "   - 5 एकड़ या अधिक कृषि भूमि।\n"
                    "   - 1,000 वर्ग फुट या अधिक का आवासीय फ्लैट।\n"
                    "   - अधिसूचित नगरपालिकाओं में 100 वर्ग गज या अधिक का आवासीय प्लॉट।\n"
                    "4. **वैधता:** 1 वित्तीय वर्ष हेतु मान्य।"
                ),
                "official_source": "Ministry of Social Justice and Empowerment (https://socialjustice.gov.in)",
                "suggested_links": [
                    {"label": "Caste & EWS Guide", "url": "/caste-certificate"},
                    {"label": "Document Checklist Builder", "url": "/checklist-builder"}
                ]
            }

        return {
            "title": "Caste Certificate Application & Statutory Rules" if not is_hi else "जाति प्रमाण पत्र आवेदन एवं नियम",
            "answer": (
                "**Caste Certificate (Jati Praman Patra) Key Facts:**\n\n"
                "- **SC / ST Certificates:** Lifetime validity (Articles 341 & 342). Require proof of paternal ancestry (Pre-1950 land record or father's certificate).\n"
                "- **OBC-NCL & EWS:** Valid for 1 Financial Year. Dependent on income ceiling (< ₹8 Lakhs/year).\n"
                "- **Supreme Court Rule:** Caste is determined strictly by birth and paternal lineage, not by marriage.\n"
                "- **How to Apply:** Apply online on your state's **e-District Portal** (e.g. Aaple Sarkar, eDistrict UP, RTPS Bihar, Seva Sindhu) or at your local Tehsildar/SDM office."
                if not is_hi else
                "**जाति प्रमाण पत्र (SC/ST/OBC/EWS) महत्वपूर्ण नियम:**\n\n"
                "- **SC / ST प्रमाण पत्र:** आजीवन वैधता (अनुच्छेद 341 एवं 342)। पिता/पैतृक पूर्वजों का 1950 पूर्व का रिकॉर्ड आवश्यक।\n"
                "- **OBC-NCL एवं EWS:** 1 वित्तीय वर्ष हेतु मान्य। वार्षिक आय ₹8 लाख से कम होना अनिवार्य।\n"
                "- **सर्वोच्च न्यायालय का निर्णय:** जाति का निर्धारण जन्म एवं पैतृक वंश से होता है, विवाह से नहीं।\n"
                "- **आवेदन प्रक्रिया:** अपने राज्य के **e-District पोर्टल** (जैसे Aaple Sarkar, eDistrict UP, RTPS बिहार, Seva Sindhu) या तहसील कार्यालय से आवेदन करें।"
            ),
            "official_source": "DoPT & State Revenue Departments",
            "suggested_links": [
                {"label": "Read Caste Certificate Guide", "url": "/caste-certificate"},
                {"label": "Select State Portal", "url": "/state-directory"}
            ]
        }

    # =========================================================================
    # 6. VOTER SERVICES INTENT (With 2026 Qualifying Dates)
    # =========================================================================
    if has_any(["voter", "vote", "eci", "epic", "form 6", "form 8", "form 7", "form 6a", "मतदाता", "वोटर", "blo", "1950"], q):
        return {
            "title": "Election Commission of India (ECI) Voter Services & 2026 Calendar" if not is_hi else "भारत निर्वाचन आयोग (ECI) मतदाता सेवाएं एवं 2026 तिथियां",
            "answer": (
                "**ECI Voter Services & Electoral Registration Schedule 2026:**\n\n"
                "1. **Continuous Online Registration (Open Year-Round):**\n"
                "   - Any eligible citizen can submit **Form 6 (New Voter)** anytime on `voters.eci.gov.in` or the **ECI Voter Helpline App**.\n\n"
                "2. **4 Statutory Qualifying Dates for 18-Year-Olds in 2026:**\n"
                "   - Citizens turning 18 on or before: **1st January, 1st April, 1st July, or 1st October 2026** can register in advance!\n\n"
                "3. **Statutory Forms:**\n"
                "   - **Form 6:** New elector registration.\n"
                "   - **Form 8:** Correction of name, DOB, photo, shifting of address, or replacement EPIC.\n"
                "   - **Form 7:** Deletion of voter entry (in case of death or permanent relocation).\n\n"
                "4. **Instant e-EPIC Download:** Digital PDF Voter ID cards can be downloaded instantly via mobile OTP from `voters.eci.gov.in`.\n"
                "5. **Toll-Free National Helpline:** Call **1950** for Booth Level Officer (BLO) details."
                if not is_hi else
                "**भारत निर्वाचन आयोग (ECI) मतदाता सेवाएं एवं 2026 कैलेंडर:**\n\n"
                "1. **सतत ऑनलाइन पंजीकरण (वर्ष भर उपलब्ध):**\n"
                "   - कोई भी पात्र नागरिक `voters.eci.gov.in` या **Voter Helpline App** द्वारा वर्ष भर कभी भी **प्रारूप 6 (नया वोटर)** भर सकता है।\n\n"
                "2. **18 वर्ष की आयु पूर्ण करने वालों हेतु 2026 की 4 अर्हक तिथियां:**\n"
                "   - **1 जनवरी, 1 अप्रैल, 1 जुलाई एवं 1 अक्टूबर 2026** तक 18 वर्ष पूरे करने वाले युवा अग्रिम पंजीकरण करा सकते हैं।\n\n"
                "3. **प्रमुख प्रारूप (Forms):**\n"
                "   - **प्रारूप 6 (Form 6):** नए मतदाता पंजीकरण हेतु।\n"
                "   - **प्रारूप 8 (Form 8):** नाम, जन्मतिथि, पता सुधार अथवा डुप्लिकेट वोटर कार्ड हेतु।\n"
                "   - **प्रारूप 7 (Form 7):** नाम विलोपन या आपत्ति दर्ज करने हेतु।\n\n"
                "4. **e-EPIC डाउनलोड:** डिजिटल वोटर कार्ड पीडीएफ तुरंत मोबाइल ओटीपी द्वारा डाउनलोड करें।\n"
                "5. **हेल्पलाइन:** मतदाता सहायता हेतु टोल-फ्री **1950** पर कॉल करें।"
            ),
            "official_source": "Election Commission of India (https://voters.eci.gov.in)",
            "suggested_links": [
                {"label": "ECI Voter Services Hub", "url": "/voter-services"},
                {"label": "Download e-EPIC", "url": "https://voters.eci.gov.in"}
            ]
        }

    # =========================================================================
    # 7. CIVIC & TRANSPORT INTENT
    # =========================================================================
    if has_any(["driving", "license", "dl", "parivahan", "sarathi", "ड्राइविंग", "birth", "death", "crs", "जन्म", "मृत्यु", "domicile", "niwas", "निवास", "ration", "राशन"], q):
        if has_any(["driving", "license", "dl", "parivahan", "sarathi", "ड्राइविंग"], q):
            return {
                "title": "Parivahan Driving License (Sarathi) Guide" if not is_hi else "परिवहन ड्राइविंग लाइसेंस (Sarathi) गाइड",
                "answer": (
                    "**How to Get a Driving License via Parivahan Sewa (`parivahan.gov.in`):**\n\n"
                    "1. **Learner's License (LL):** Apply on `parivahan.gov.in` -> Sarathi. Complete Aadhaar authentication to take the **contactless online road safety test from home**.\n"
                    "2. **Validity of LL:** Valid for 6 months across India.\n"
                    "3. **Permanent Driving License (DL):** After 30 days of LL issuance, book a slot for the practical driving track test at your local RTO.\n"
                    "4. **Smart Card Dispatch:** Smart card DL is dispatched directly via Speed Post."
                    if not is_hi else
                    "**परिवहन सेवा (`parivahan.gov.in`) से ड्राइविंग लाइसेंस कैसे प्राप्त करें:**\n\n"
                    "1. **लर्निंग लाइसेंस (LL):** `parivahan.gov.in` पर आधार ऑथेंटिकेशन द्वारा घर बैठे ऑनलाइन लर्निंग टेस्ट दें।\n"
                    "2. **LL की वैधता:** पूरे भारत में 6 माह हेतु मान्य।\n"
                    "3. **स्थायी ड्राइविंग लाइसेंस (DL):** LL जारी होने के 30 दिन बाद RTO में प्रैक्टिकल ड्राइविंग टेस्ट स्लॉट बुक करें।\n"
                    "4. **स्मार्ट कार्ड प्राप्ति:** टेस्ट पास करने पर स्थायी स्मार्ट कार्ड DL स्पीड पोस्ट द्वारा भेजा जाता है।"
                ),
                "official_source": "Ministry of Road Transport and Highways (https://parivahan.gov.in)",
                "suggested_links": [
                    {"label": "Civic & Transport Hub", "url": "/civic-services"},
                    {"label": "Parivahan Official Portal", "url": "https://parivahan.gov.in"}
                ]
            }

        if has_any(["birth", "death", "जन्म", "मृत्यु", "crs"], q):
            return {
                "title": "Birth & Death Registration (RBD Act) Guide" if not is_hi else "जन्म एवं मृत्यु पंजीकरण (RBD एक्ट) गाइड",
                "answer": (
                    "**Registration of Births and Deaths (RBD Act 1969 & 2023 Amendment):**\n\n"
                    "1. **21-Day Rule:** Free of cost registration within 21 days on the CRS portal (`crsorgi.gov.in`) or local Municipal/Gram Panchayat office.\n"
                    "2. **Delayed Registration:** 21-30 days (nominal late fee); 30 days to 1 year (SDM order & affidavit); After 1 year (First Class Magistrate order).\n"
                    "3. **Conclusive Proof:** Under the 2023 Amendment, digital Birth Certificate serves as single proof for school admissions, voter ID, passports, and government jobs."
                    if not is_hi else
                    "**जन्म एवं मृत्यु पंजीकरण (RBD अधिनियम):**\n\n"
                    "1. **21 दिनों का नियम:** 21 दिनों के भीतर `crsorgi.gov.in` अथवा स्थानीय नगर निकाय/ग्राम पंचायत में पंजीकरण पूर्णतः मुफ्त है।\n"
                    "2. **विलंबित पंजीकरण:** 21-30 दिन (विलंब शुल्क); 30 दिन से 1 वर्ष (एसडीएम अनुमति); 1 वर्ष पश्चात (प्रथम श्रेणी मजिस्ट्रेट आदेश)।\n"
                    "3. **एकल प्रमाण:** 2023 संशोधन के तहत डिजिटल जन्म प्रमाण पत्र स्कूल प्रवेश, वोटर कार्ड व पासपोर्ट हेतु एकल प्रामाणिक दस्तावेज है।"
                ),
                "official_source": "Civil Registration System (https://crsorgi.gov.in)",
                "suggested_links": [
                    {"label": "Civic Services Guide", "url": "/civic-services"},
                    {"label": "CRS Official Portal", "url": "https://crsorgi.gov.in"}
                ]
            }

    # =========================================================================
    # 8. STATE SPECIFIC WELFARES & DATES INTENT
    # =========================================================================
    
    # 8.1 Special Handler for Popular State Schemes (e.g., Ladki Bahin in Maharashtra)
    if has_any(["ladki bahin", "लाड़की बहिन", "ladli behna", "majhi ladki bahin"], q):
        return {
            "title": "Mukhyamantri Majhi Ladki Bahin Yojana 2026 Schedule & Dates" if not is_hi else "मुख्यमंत्री माझी लाड़की बहिन योजना 2026 किस्त व तिथियां",
            "answer": (
                "**Mukhyamantri Majhi Ladki Bahin Yojana (Government of Maharashtra) 2026:**\n\n"
                "1. **Monthly Benefit:** **₹1,500 per month** directly credited via Aadhaar-DBT into the bank accounts of eligible women aged 21–65 years.\n\n"
                "2. **Monthly Installment Credit Dates:**\n"
                "   - Installments are disbursed monthly between the **10th and 15th of every calendar month** in 2026.\n\n"
                "3. **Key Eligibility:** Resident of Maharashtra, annual family income under **₹2,50,000**, with bank account mapped to Aadhaar (NPCI active)."
                if not is_hi else
                "**मुख्यमंत्री माझी लाड़की बहिन योजना (महाराष्ट्र सरकार) 2026:**\n\n"
                "1. **मासिक सहायता:** 21 से 65 वर्ष की पात्र महिलाओं को **₹1,500 प्रति माह** सीधे आधार-लिंक बैंक खाते में डीबीटी द्वारा।\n\n"
                "2. **मासिक किस्त की तारीख:**\n"
                "   - वर्ष 2026 में प्रत्येक माह की **10 से 15 तारीख के बीच** किस्त राशि बैंक खातों में जमा की जाती है।\n\n"
                "3. **पात्रता:** महाराष्ट्र की निवासी महिला, वार्षिक पारिवारिक आय **₹2.5 लाख से कम**, आधार लिंक सक्रिय बैंक खाता।"
            ),
            "official_source": "Government of Maharashtra (https://ladakibahin.maharashtra.gov.in)",
            "suggested_links": [
                {"label": "Ladki Bahin Official Portal", "url": "https://ladakibahin.maharashtra.gov.in"},
                {"label": "Aaple Sarkar Portal", "url": "https://aaplesarkar.mahaonline.gov.in"}
            ]
        }

    for st in STATE_PORTALS_DATA:
        if has_word(st["state_name"], q) or (st.get("state_name_hi") and st["state_name_hi"] in q) or has_word(st["id"], q):
            sch_list = ""
            if st.get("state_scholarships"):
                for ss in st["state_scholarships"]:
                    s_name = ss["name_hi"] if is_hi and "name_hi" in ss else ss["name"]
                    sch_list += f"\n- **{s_name}**: {ss['benefit']} (Income limit: {ss['income_limit']})"

            wel_list = ""
            if st.get("state_welfares"):
                for sw in st["state_welfares"]:
                    w_name = sw["name_hi"] if is_hi and "name_hi" in sw else sw["name"]
                    wel_list += f"\n- **{w_name}**: {sw['description']}"

            s_title = st["state_name_hi"] if is_hi and "state_name_hi" in st else st["state_name"]
            return {
                "title": f"Services, Welfare Schemes & 2026 Dates for {s_title}" if not is_hi else f"{s_title} की सरकारी योजनाएं, सेवाएं एवं 2026 कैलेंडर",
                "answer": (
                    f"**Official e-Governance Portal:** {st['portal_name']} ({st['portal_url']})\n\n"
                    f"**Key State Scholarships (2026 Cycle):**{sch_list}\n\n"
                    f"**State Flagship Welfare Programs:**{wel_list}\n\n"
                    f"**Key Online Services:** {', '.join(st['key_services'])}\n\n"
                    "*(Most state welfare schemes disburse financial aid on fixed monthly or seasonal tranches, and scholarship portals remain open from August to December annually.)*"
                ),
                "official_source": st.get("official_source", st["portal_url"]),
                "suggested_links": [
                    {"label": f"Visit {st['portal_name']}", "url": st["portal_url"]},
                    {"label": "Select State Directory", "url": "/state-directory"}
                ]
            }

    # =========================================================================
    # 9. GENERAL 2026 WELFARE SCHEMES SCHEDULE OVERVIEW
    # =========================================================================
    if has_any(["welfare scheme", "welfare schemes", "schemes 2026", "welfare schedule", "सरकारी योजना", "योजनाएं 2026"], q) or (has_any(["yojana", "scheme", "schemes", "योजना"], q) and is_time_query):
        return {
            "title": "National Flagship Welfare Schemes 2026 Schedules & Payment Cycles" if not is_hi else "प्रमुख राष्ट्रीय कल्याणकारी योजनाएं 2026 भुगतान एवं आवेदन कैलेंडर",
            "answer": (
                "**National Flagship Welfare Schemes 2026 Schedules & Payment Cycles:**\n\n"
                "1. 🌾 **PM-KISAN (Farmer Income Support):**\n"
                "   - ₹6,000 in 3 installments of ₹2,000 every 4 months (Released: **May/June 2026**, **October/November 2026**, and **February/March 2027**).\n\n"
                "2. 🏥 **Ayushman Bharat PM-JAY & Vay Vandana (70+):**\n"
                "   - **Open 24x7 / 365 Days Year-Round** for free ₹5 Lakhs hospital cover. Senior citizens aged 70+ can enroll anytime in 2026 on the Ayushman App.\n\n"
                "3. 🏠 **PM Awas Yojana (PMAY 2.0 Urban & Gramin):**\n"
                "   - 3 Crore additional homes rollout (2024–2029) actively registering beneficiaries throughout 2026.\n\n"
                "4. ⚒️ **PM Vishwakarma:**\n"
                "   - Continuous enrollment open throughout 2026 for 18 artisan trades with ₹15,000 toolkit vouchers and 5% interest enterprise loans.\n\n"
                "5. 🔥 **PM Ujjwala 2.0:**\n"
                "   - Open year-round for deposit-free LPG gas connections + ₹300 per cylinder subsidy.\n\n"
                "6. 🎓 **National Scholarships (NSP):**\n"
                "   - Academic year 2026–27 portal opens in **July/August 2026**; Application deadline **October/November 2026**."
                if not is_hi else
                "**प्रमुख राष्ट्रीय सरकारी कल्याणकारी योजनाएं 2026 कैलेंडर एवं भुगतान चक्र:**\n\n"
                "1. 🌾 **पीएम-किसान (PM-KISAN):**\n"
                "   - ₹6,000 की वार्षिक सहायता (किस्त 1: **मई/जून 2026**, किस्त 2: **अक्टूबर/नवंबर 2026**, किस्त 3: **फरवरी/मार्च 2027**)।\n\n"
                "2. 🏥 **आयुष्मान भारत PM-JAY एवं वय वंदना (70+):**\n"
                "   - ₹5 लाख का मुफ्त स्वास्थ्य कार्ड बनाने हेतु वर्ष 2026 में **365 दिन 24x7 सतत खुला है**।\n\n"
                "3. 🏠 **प्रधानमंत्री आवास योजना (PMAY 2.0):**\n"
                "   - 3 करोड़ नए पक्के मकानों हेतु वर्ष 2026 में ग्रामीण व शहरी पंजीकरण निरंतर जारी है।\n\n"
                "4. ⚒️ **पीएम विश्वकर्मा योजना:**\n"
                "   - 18 पारंपरिक शिल्पों हेतु ₹15,000 टूलकिट व सस्ते ऋण का पंजीकरण 2026 में सतत खुला है।\n\n"
                "5. 🔥 **उज्ज्वला योजना 2.0:**\n"
                "   - मुफ्त गैस कनेक्शन व ₹300 सब्सिडी हेतु वर्ष भर आवेदन खुले हैं।\n\n"
                "6. 🎓 **राष्ट्रीय छात्रवृत्ति (NSP):**\n"
                "   - 2026–27 सत्र हेतु पोर्टल **जुलाई/अगस्त 2026** में खुलेगा; आवेदन की अंतिम तिथि **अक्टूबर/नवंबर 2026**।"
            ),
            "official_source": "Government of India Citizen Portals (https://india.gov.in)",
            "suggested_links": [
                {"label": "PM-Kisan Portal", "url": "https://pmkisan.gov.in"},
                {"label": "Ayushman Beneficiary Portal", "url": "https://beneficiary.nha.gov.in"},
                {"label": "PMAY Urban Portal", "url": "https://pmaymis.gov.in"}
            ]
        }

    # =========================================================================
    # 10. DEFAULT FALLBACK
    # =========================================================================
    return {
        "title": "CivicGuide AI Assistant" if not is_hi else "सिविकगाइड AI सहायक",
        "answer": (
            "I can assist you with verified official information on:\n\n"
            "1. **Civil Services & Entrance Exams (2026 Dates & Rules):** JEE Main & Advanced 2026, NEET-UG 2026, UPSC CSE 2026 (Prelims in May, Mains in Sept), SSC CGL 2026, NDA/CDS.\n"
            "2. **Flagship Welfare Schemes (2026 Schedules):** PM-Kisan (₹6,000 in 3 installments), Ayushman Bharat PM-JAY (24x7 enrollment & 70+ Vay Vandana card), PMAY 2.0, PM Vishwakarma, PM Ujjwala 2.0.\n"
            "3. **Scholarships (NSP 2026-27):** Application window (July-Nov), Pre/Post-Matric, PM-YASASVI, AICTE Pragati, CSSS, NSP OTR Face Auth.\n"
            "4. **Caste Certificates:** SC/ST/OBC-NCL/EWS rules, income criteria (< ₹8 Lakhs), ancestry records.\n"
            "5. **Voter Services:** ECI Form 6 (New Voter), 4 Qualifying Dates in 2026 (Jan/Apr/Jul/Oct), e-EPIC download, Helpline 1950.\n"
            "6. **Civic & Transport:** Birth/Death (CRS 21-day timeline), Parivahan Driving License, Domicile, Ration Card (ONORC).\n"
            "7. **State Welfares:** Schemes & scholarships across all 28 Indian States & 8 UTs (e.g. Majhi Ladki Bahin ₹1,500 monthly date).\n\n"
            "Please ask a specific question (e.g., *'When does the JEE exam for year 2026 start?'*, *'When will the next PM-Kisan installment come in 2026?'* or *'What is the UPSC CSE 2026 schedule?'*)."
            if not is_hi else
            "मैं आपको निम्नलिखित सरकारी सेवाओं पर सटीक, आधिकारिक व 2026 कैलेंडर अनुसार जानकारी प्रदान कर सकता हूँ:\n\n"
            "1. **प्रतियोगी परीक्षाएं (2026 तिथियां व नियम):** जेईई मेन व एडवांस्ड 2026, नीट-यूजी (3 मई 2026), UPSC सिविल सेवा 2026 (प्रीलिम्स मई 2026), SSC CGL, NDA/CDS।\n"
            "2. **कल्याणकारी योजनाएं (2026 भुगतान चक्र):** पीएम-किसान (₹2,000 की 3 किस्तें), आयुष्मान भारत (24x7 खुला व 70+ वय वंदना कार्ड), पीएम आवास 2.0, पीएम विश्वकर्मा।\n"
            "3. **छात्रवृत्ति (NSP 2026-27):** पोर्टल खुलने की तिथि (जुलाई/अगस्त), पोस्ट-मैट्रिक, प्रगति, यशस्वी, NSP OTR फेस ऑथेंटिकेशन।\n"
            "4. **जाति प्रमाण पत्र:** SC/ST/OBC-NCL/EWS नियम, ₹8 लाख आय सीमा, 1 वित्तीय वर्ष वैधता।\n"
            "5. **मतदाता सेवाएं:** ECI प्रारूप 6, 2026 की 4 अर्हक तिथियां, e-EPIC डाउनलोड, हेल्पलाइन 1950।\n"
            "6. **नागरिक व परिवहन:** जन्म/मृत्यु (21 दिन), ड्राइविंग लाइसेंस, राशन कार्ड।\n"
            "7. **राज्य कल्याण योजनाएं:** 28 राज्यों व 8 केंद्र शासित प्रदेशों की योजनाएं (जैसे लाड़की बहिन योजना की मासिक तारीख)।\n\n"
            "कृपया अपना प्रश्न पूछें (जैसे: *'JEE 2026 परीक्षा कब शुरू होगी?'*, *'वर्ष 2026 में पीएम किसान की किस्त कब आएगी?'* या *'UPSC 2026 प्रीलिम्स की तारीख क्या है?'*)।"
        ),
        "official_source": "Government of India Citizen Portals (https://india.gov.in)",
        "suggested_links": [
            {"label": "Check Eligibility Wizard", "url": "#wizard"},
            {"label": "Select State Portals", "url": "/state-directory"}
        ]
    }
