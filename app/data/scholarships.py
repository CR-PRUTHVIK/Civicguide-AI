"""
Comprehensive database of Indian Government Scholarships
With verified official sources, Hindi translations & statutory guidelines
Source: National Scholarship Portal (scholarships.gov.in), Ministry of Education, MoSJE, MoMA, AICTE, DST
"""

SCHOLARSHIPS_DATA = [
    {
        "id": "nsp-post-matric-sc",
        "title": "Post-Matric Scholarship for SC Students",
        "title_hi": "अनुसूचित जाति (SC) छात्रों के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
        "ministry": "Ministry of Social Justice and Empowerment",
        "ministry_hi": "सामाजिक न्याय और अधिकारिता मंत्रालय",
        "official_source": "Ministry of Social Justice & Empowerment, Govt of India",
        "official_source_url": "https://socialjustice.gov.in / https://scholarships.gov.in",
        "category": "Scheduled Caste (SC)",
        "category_hi": "अनुसूचित जाति (SC)",
        "education_level": ["Class 11-12", "Graduation", "Post-Graduation", "Diploma", "Professional"],
        "max_income_inr": 250000,
        "benefits": "100% tuition fee waiver + Monthly maintenance allowance (up to ₹13,500/yr for hostellers and ₹7,000/yr for day scholars) + study tour allowance.",
        "benefits_hi": "100% ट्यूशन शुल्क प्रतिपूर्ति + मासिक रखरखाव भत्ता (हॉस्टलर्स हेतु ₹13,500/वर्ष तक तथा डे-स्कॉलर्स हेतु ₹7,000/वर्ष तक) + अध्ययन भ्रमण भत्ता।",
        "portal_name": "National Scholarship Portal (NSP)",
        "portal_url": "https://scholarships.gov.in",
        "description": "Centrally sponsored scheme to provide financial assistance to Scheduled Caste students studying at post-matriculation or post-secondary stage to enable them to complete their education.",
        "description_hi": "कक्षा 10वीं के बाद उच्च शिक्षा (कक्षा 11 से पीएचडी तक) प्राप्त कर रहे अनुसूचित जाति के मेधावी छात्र-छात्राओं हेतु केंद्र सरकार द्वारा प्रायोजित वित्तीय सहायता योजना।",
        "eligibility_criteria": [
            "Applicant must belong to Scheduled Caste (SC) category.",
            "Must be a permanent resident/citizen of India.",
            "Total annual family income from all sources must not exceed ₹2,50,000 per annum.",
            "Must be enrolled in a recognized post-matric course (Class 11 to PhD)."
        ],
        "eligibility_criteria_hi": [
            "आवेदक अनिवार्य रूप से अनुसूचित जाति (SC) वर्ग से संबंधित होना चाहिए।",
            "भारत का स्थायी नागरिक होना आवश्यक है।",
            "परिवार की समस्त स्रोतों से कुल वार्षिक आय ₹2,50,000 से अधिक नहीं होनी चाहिए।",
            "मान्यता प्राप्त उच्च शिक्षण संस्थान में नियमित नामांकित होना चाहिए।"
        ],
        "documents_required": [
            "Aadhaar Card (linked to Bank Account / NPCI mapped)",
            "Valid Caste Certificate issued by competent Revenue Authority",
            "Latest Family Income Certificate (issued by Tehsildar/SDM)",
            "Previous Year Mark Sheet / Passing Certificate",
            "Current Year Fee Receipt and Admission Letter",
            "Student Bank Account Passbook (Aadhaar Seeded)",
            "Passport Size Photograph"
        ],
        "documents_required_hi": [
            "आधार कार्ड (बैंक खाते से एनपीसीआई/डीबीटी मैप किया हुआ)",
            "सक्षम राजस्व अधिकारी (तहसीलदार/एसडीएम) द्वारा जारी वैध जाति प्रमाण पत्र",
            "चालू वित्तीय वर्ष का वैध आय प्रमाण पत्र",
            "पिछली कक्षा की अंकतालिका / उत्तीर्ण प्रमाण पत्र",
            "कॉलेज प्रवेश पत्र एवं शुल्क रसीद (Bonafide Certificate)",
            "पासपोर्ट आकार का रंगीन फोटो"
        ],
        "application_steps": [
            "Visit National Scholarship Portal (scholarships.gov.in) and download the NSP OTR App for Aadhaar Face Authentication.",
            "Complete One Time Registration (OTR) to obtain a unique 14-digit OTR Number.",
            "Log in to NSP with OTR number and password.",
            "Select 'Department of Social Justice and Empowerment' -> 'Post Matric Scholarship for SC'.",
            "Fill in academic details, course fee structure, and upload required documents.",
            "Submit application and note Application Reference ID.",
            "Submit physical hard copy with documents to your College/Institute Nodal Officer (INO) for verification."
        ],
        "application_steps_hi": [
            "राष्ट्रीय छात्रवृत्ति पोर्टल (scholarships.gov.in) पर जाएं एवं NSP OTR ऐप द्वारा आधार फेस ऑथेंटिकेशन पूर्ण करें।",
            "14 अंकों का स्थायी OTR (One Time Registration) नंबर प्राप्त करें।",
            "पोर्टल पर लॉगिन कर 'Post Matric Scholarship for SC' योजना चुनें।",
            "शैक्षणिक विवरण, फीस संरचना भरें एवं आवश्यक दस्तावेज अपलोड करें।",
            "ऑनलाइन आवेदन सबमिट कर संस्थान के नोडल अधिकारी (INO) को सत्यापन हेतु हार्ड कॉपी जमा करें।"
        ],
        "tags": ["SC", "Post-Matric", "Central", "NSP", "College"]
    },
    {
        "id": "nsp-post-matric-st",
        "title": "Post-Matric Scholarship for ST Students",
        "title_hi": "अनुसूचित जनजाति (ST) छात्रों के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
        "ministry": "Ministry of Tribal Affairs",
        "ministry_hi": "जनजातीय कार्य मंत्रालय",
        "official_source": "Ministry of Tribal Affairs, Govt of India",
        "official_source_url": "https://tribal.nic.in / https://scholarships.gov.in",
        "category": "Scheduled Tribe (ST)",
        "category_hi": "अनुसूचित जनजाति (ST)",
        "education_level": ["Class 11-12", "Graduation", "Post-Graduation", "Diploma", "Professional"],
        "max_income_inr": 250000,
        "benefits": "Compulsory non-refundable fees reimbursement + Maintenance allowance ranging from ₹2,300 to ₹12,000 per annum depending on course group.",
        "benefits_hi": "गैर-वापसी योग्य अनिवार्य कॉलेज फीस की पूर्ण प्रतिपूर्ति + ₹2,300 से ₹12,000 प्रति वर्ष तक मासिक निर्वाह भत्ता।",
        "portal_name": "National Scholarship Portal (NSP)",
        "portal_url": "https://scholarships.gov.in",
        "description": "Financial aid for Scheduled Tribe students pursuing higher education after Class 10 to reduce dropout rates and improve tribal literacy.",
        "description_hi": "जनजातीय वर्ग के विद्यार्थियों को 10वीं के बाद उच्च व तकनीकी शिक्षा पूरी करने हेतु आर्थिक संबल प्रदान करने वाली प्रमुख केंद्रीय योजना।",
        "eligibility_criteria": [
            "Applicant must belong to Scheduled Tribe (ST) community.",
            "Must have passed Matriculation (Class 10) or higher examination from a recognized Board/University.",
            "Annual family income must not exceed ₹2.5 Lakhs.",
            "Should not be holding any other government scholarship simultaneously."
        ],
        "eligibility_criteria_hi": [
            "आवेदक अनुसूचित जनजाति (ST) वर्ग का होना चाहिए।",
            "कक्षा 10वीं या समकक्ष परीक्षा उत्तीर्ण होना आवश्यक है।",
            "पारिवारिक वार्षिक आय ₹2.50 लाख से कम होनी चाहिए।",
            "एक समय में केवल एक ही सरकारी छात्रवृत्ति का लाभ लिया जा सकता है।"
        ],
        "documents_required": [
            "Aadhaar Card (Aadhaar-seeded bank account)",
            "ST Community Certificate issued by SDO/Tehsildar",
            "Income Certificate issued by Revenue Authority",
            "Marksheets of previous qualifying exams",
            "College Bonafide Certificate & Fee Structure",
            "Bank Passbook copy"
        ],
        "documents_required_hi": [
            "आधार कार्ड (डीबीटी बैंक खाते से लिंक)",
            "सक्षम राजस्व अधिकारी द्वारा जारी एसटी जाति प्रमाण पत्र",
            "आय प्रमाण पत्र एवं पिछली कक्षा की अंकतालिका",
            "कॉलेज बोनाफाइड प्रमाण पत्र व फीस रसीद"
        ],
        "application_steps": [
            "Generate OTR on NSP Portal using Aadhaar OTP / Face Auth.",
            "Select Ministry of Tribal Affairs -> Post Matric Scholarship Scheme for ST Students.",
            "Upload caste, income, and academic documents.",
            "Submit online and track verification status through District Nodal Officer (DNO)."
        ],
        "application_steps_hi": [
            "NSP पोर्टल पर OTR जनरेट करें।",
            "जनजातीय कार्य मंत्रालय के अंतर्गत एसटी पोस्ट-मैट्रिक योजना चुनें।",
            "दस्तावेज अपलोड कर आवेदन सबमिट करें और संस्थान द्वारा सत्यापित करवाएं।"
        ],
        "tags": ["ST", "Post-Matric", "Tribal", "NSP", "Higher Education"]
    },
    {
        "id": "nsp-post-matric-obc-ebc-dnt",
        "title": "PM-YASASVI Post-Matric Scholarship for OBC, EBC & DNT",
        "title_hi": "पीएम-यशस्वी (PM-YASASVI) पोस्ट-मैट्रिक छात्रवृत्ति (OBC/EBC/DNT)",
        "ministry": "Ministry of Social Justice and Empowerment",
        "ministry_hi": "सामाजिक न्याय और अधिकारिता मंत्रालय",
        "official_source": "Department of Social Justice and Empowerment, Govt of India",
        "official_source_url": "https://socialjustice.gov.in / https://scholarships.gov.in",
        "category": "OBC / EBC / DNT",
        "category_hi": "अन्य पिछड़ा वर्ग / ईबीसी / डीएनटी",
        "education_level": ["Class 11-12", "Graduation", "Post-Graduation", "Diploma"],
        "max_income_inr": 250000,
        "benefits": "Academic allowance up to ₹20,000/year depending on course tier + Non-refundable compulsory fee reimbursement.",
        "benefits_hi": "अनिवार्य शिक्षण शुल्क प्रतिपूर्ति + कोर्स स्तर के आधार पर ₹20,000 प्रति वर्ष तक शैक्षणिक भत्ता।",
        "portal_name": "National Scholarship Portal (NSP)",
        "portal_url": "https://scholarships.gov.in",
        "description": "Pradhan Mantri Young Achievers Scholarship Award Scheme for Vibrant India (PM-YASASVI) offering post-matric support to Other Backward Classes, Economically Backward Classes, and De-notified Nomadic Tribes.",
        "description_hi": "ओबीसी, ईबीसी एवं विमुक्त घुमंतू जनजातियों के मेधावी छात्र-छात्राओं को उच्च शिक्षा में प्रोत्साहन देने हेतु प्रमुख राष्ट्रीय छात्रवृत्ति योजना।",
        "eligibility_criteria": [
            "Belong to OBC, EBC, or DNT category with valid State/Central list entry.",
            "Annual family income should not exceed ₹2,50,000.",
            "Studying in Class 11, 12 or at undergraduate/postgraduate level in a recognized institution."
        ],
        "eligibility_criteria_hi": [
            "ओबीसी (गैर-क्रीमी लेयर), ईबीसी अथवा डीएनटी वर्ग से संबंधित होना आवश्यक।",
            "परिवार की कुल वार्षिक आय ₹2.50 लाख से अधिक न हो।",
            "कक्षा 11, 12 अथवा स्नातक/डिप्लोमा स्तर पर अध्ययनरत होना चाहिए।"
        ],
        "documents_required": [
            "OBC / EBC / DNT Caste Certificate (Non-Creamy Layer for OBC)",
            "Income Certificate for the current financial year",
            "Aadhaar Card",
            "Previous Class Marksheet",
            "Fee Receipt and Bonafide Certificate"
        ],
        "documents_required_hi": [
            "ओबीसी गैर-क्रीमी लेयर / ईबीसी / डीएनटी जाति प्रमाण पत्र",
            "चालू वर्ष का आय प्रमाण पत्र",
            "आधार कार्ड एवं पिछली कक्षा की अंकतालिका",
            "संस्थान की फीस रसीद व बोनाफाइड सर्टिफिकेट"
        ],
        "application_steps": [
            "Complete OTR registration on NSP portal.",
            "Search for PM-YASASVI Post-Matric Scheme in state or central pool.",
            "Fill academic and socio-economic details, attach documents, and submit."
        ],
        "application_steps_hi": [
            "NSP पोर्टल पर OTR रजिस्ट्रेशन पूरा करें।",
            "PM-YASASVI पोस्ट-मैट्रिक स्कीम का चयन कर विवरण भरें और सबमिट करें।"
        ],
        "tags": ["OBC", "EBC", "DNT", "PM-YASASVI", "Post-Matric"]
    },
    {
        "id": "nsp-central-sector-csss",
        "title": "Central Sector Scheme of Scholarship for College and University Students (CSSS)",
        "title_hi": "कॉलेज एवं विश्वविद्यालय छात्रों के लिए केंद्रीय क्षेत्र छात्रवृत्ति योजना (CSSS)",
        "ministry": "Department of Higher Education (Ministry of Education)",
        "ministry_hi": "उच्च शिक्षा विभाग (शिक्षा मंत्रालय)",
        "official_source": "Department of Higher Education, Ministry of Education, Govt of India",
        "official_source_url": "https://www.education.gov.in / https://scholarships.gov.in",
        "category": "All (General / OBC / SC / ST / EWS)",
        "category_hi": "सभी वर्ग (सामान्य / ओबीसी / एससी / एसटी / ईडब्ल्यूएस)",
        "education_level": ["Graduation", "Post-Graduation", "Professional"],
        "max_income_inr": 450000,
        "benefits": "₹12,000 per annum at Graduation level for first 3 years; ₹20,000 per annum at Post-Graduation level.",
        "benefits_hi": "स्नातक स्तर पर प्रथम 3 वर्षों तक ₹12,000 प्रति वर्ष; स्नातकोत्तर स्तर पर ₹20,000 प्रति वर्ष।",
        "portal_name": "National Scholarship Portal (NSP)",
        "portal_url": "https://scholarships.gov.in",
        "description": "Merit-cum-means scholarship aimed at supporting outstanding students from lower-income families who score above the 80th percentile in Class 12 board examinations.",
        "description_hi": "कक्षा 12वीं बोर्ड परीक्षा में संबंधित विषय वर्ग में 80वें परसेंटाइल से अधिक अंक प्राप्त करने वाले मेधावी छात्र-छात्राओं हेतु मेरिट-कम-मीन्स छात्रवृत्ति।",
        "eligibility_criteria": [
            "Scored above 80th percentile in relevant stream in Class 12 Board Examination.",
            "Pursuing regular (non-correspondence) degree/diploma courses in recognized Colleges/Universities.",
            "Annual parental/family income up to ₹4,50,000.",
            "Not availing any other national or state scholarship benefit."
        ],
        "eligibility_criteria_hi": [
            "12वीं बोर्ड परीक्षा में 80वें परसेंटाइल (शीर्ष 20%) से अधिक अंक।",
            "मान्यता प्राप्त संस्थान में नियमित स्नातक/इंजीनियरिंग/मेडिकल कोर्स में नामांकित।",
            "पारिवारिक वार्षिक आय ₹4.50 लाख से कम।",
            "किसी अन्य सरकारी छात्रवृत्ति का लाभ न ले रहे हों।"
        ],
        "documents_required": [
            "Class 12th Board Marksheet showing merit rank / percentile",
            "Aadhaar Card with biometric verification",
            "Income Certificate issued by Revenue Authority (below ₹4.5 Lakhs)",
            "Admission confirmation / Bonafide certificate from recognized College",
            "Bank account details (NPCI mapped)"
        ],
        "documents_required_hi": [
            "12वीं बोर्ड अंकतालिका एवं बोर्ड एडवाइजरी सूची",
            "आधार कार्ड एवं डीबीटी मैप बैंक खाता",
            "सक्षम अधिकारी द्वारा जारी आय प्रमाण पत्र (< ₹4.5 लाख)",
            "कॉलेज बोनाफाइड प्रमाण पत्र"
        ],
        "application_steps": [
            "Obtain OTR ID on scholarships.gov.in.",
            "Apply under 'Department of Higher Education' -> 'Central Sector Scheme'.",
            "Provide Class 12 Roll Number, Board Name, Year of Passing to auto-validate board merit list.",
            "Submit online and institute verifies online via AISHE code."
        ],
        "application_steps_hi": [
            "scholarships.gov.in पर OTR प्राप्त करें।",
            "उच्च शिक्षा विभाग -> Central Sector Scheme चुनें।",
            "12वीं रोल नंबर व बोर्ड नाम दर्ज कर ऑनलाइन सत्यापन करें।"
        ],
        "tags": ["Merit", "Class 12", "Graduation", "General", "All Categories"]
    },
    {
        "id": "aicte-pragati-girls",
        "title": "AICTE Pragati Scholarship Scheme for Girl Students",
        "title_hi": "एआईसीटीई प्रगति छात्रवृत्ति योजना (बालिकाओं हेतु)",
        "ministry": "All India Council for Technical Education (AICTE)",
        "ministry_hi": "अखिल भारतीय तकनीकी शिक्षा परिषद (AICTE)",
        "official_source": "AICTE, Ministry of Education, Govt of India",
        "official_source_url": "https://www.aicte-india.org / https://scholarships.gov.in",
        "category": "Female (All Social Categories)",
        "category_hi": "केवल छात्राएं (सभी सामाजिक वर्ग)",
        "education_level": ["Diploma", "Graduation"],
        "max_income_inr": 800000,
        "benefits": "₹50,000 per annum for every year of study towards tuition fee, computer purchase, books, and competitive exam preparation.",
        "benefits_hi": "₹50,000 प्रति वर्ष (ट्यूशन फीस, लैपटॉप/कंप्यूटर क्रय, पुस्तकें एवं प्रतियोगी परीक्षा तैयारी हेतु)।",
        "portal_name": "NSP / AICTE Portal",
        "portal_url": "https://scholarships.gov.in",
        "description": "Scheme to empower young women with technical education by providing financial assistance to up to two girl children per family admitted to AICTE approved technical degree/diploma programs.",
        "description_hi": "तकनीकी शिक्षा (इंजीनियरिंग एवं डिप्लोमा) में बालिकाओं की भागीदारी बढ़ाने हेतु प्रति परिवार अधिकतम दो पुत्रियों को ₹50,000 वार्षिक सहायता।",
        "eligibility_criteria": [
            "Female student admitted to 1st year of Degree/Diploma course OR 2nd year via Lateral Entry in an AICTE-approved institution.",
            "Maximum 2 girls per family eligible.",
            "Family income should not exceed ₹8,00,000 per annum.",
            "Admission must be through centralized admission process of State/Central Govt."
        ],
        "eligibility_criteria_hi": [
            "AICTE से मान्यता प्राप्त संस्थान में डिग्री अथवा डिप्लोमा के प्रथम वर्ष (या लेटरल एंट्री द्वितीय वर्ष) में प्रवेशित छात्रा।",
            "प्रति परिवार अधिकतम 2 बालिकाएं पात्र।",
            "पारिवारिक वार्षिक आय ₹8,00,000 से कम।",
            "केंद्रीकृत काउंसलिंग (JEE/CET आदि) के माध्यम से प्रवेश होना अनिवार्य।"
        ],
        "documents_required": [
            "Class 10th and 12th Marksheet",
            "Allotment letter issued by Centralized Admission Authority (State CET/JEE/Polytechnic)",
            "Parental Income Certificate (<= ₹8 Lakhs)",
            "Family declaration stating candidate is one of maximum two eligible daughters",
            "Aadhaar card & Bank details",
            "Tuition fee receipt"
        ],
        "documents_required_hi": [
            "10वीं एवं 12वीं की अंकतालिका",
            "केंद्रीकृत प्रवेश आवंटन पत्र (Seat Allotment Letter)",
            "सक्षम प्राधिकारी द्वारा जारी आय प्रमाण पत्र (अधिकतम ₹8 लाख)",
            "पारिवारिक स्व-घोषणा पत्र (अधिकतम 2 पुत्रियों हेतु)",
            "आधार कार्ड एवं बैंक पासबुक"
        ],
        "application_steps": [
            "Register on NSP portal with OTR.",
            "Choose 'AICTE Schemes' -> 'Pragati Scholarship Scheme (Degree or Diploma)'.",
            "Provide AICTE Institute Permanent ID and admission allotment details.",
            "Upload family declaration and income certificate and submit."
        ],
        "application_steps_hi": [
            "NSP पर OTR के साथ आवेदन करें।",
            "AICTE Schemes -> Pragati Scholarship चुनें।",
            "संस्थान का AICTE ID एवं आवंटन पत्र अपलोड कर सबमिट करें।"
        ],
        "tags": ["Girls", "Technical", "Engineering", "Diploma", "AICTE"]
    }
]
