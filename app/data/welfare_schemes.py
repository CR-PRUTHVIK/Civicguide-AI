"""
National Flagship Welfare Schemes & Social Security Programs
Sources: pmkisan.gov.in, pmjay.gov.in, pmaymis.gov.in, myscheme.gov.in, pmvishwakarma.gov.in
Updated with complete 2026 Installment Dates, Release Cycles & Application Schedules
"""

NATIONAL_WELFARES_DATA = [
    {
        "id": "pm-kisan",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "name_hi": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "official_url": "https://pmkisan.gov.in",
        "official_source": "pmkisan.gov.in (Official Govt of India Portal)",
        "benefit": "₹6,000 per year in 3 equal installments of ₹2,000 directly transferred via DBT into farmers' Aadhaar-seeded bank accounts.",
        "benefit_hi": "प्रति वर्ष ₹6,000 की वित्तीय सहायता (₹2,000 की 3 समान किस्तों में) सीधे आधार लिंक बैंक खाते में डीबीटी द्वारा।",
        "schedule_2026": "Period 1 (April-July): Released May/June 2026. Period 2 (Aug-Nov): Released Oct/Nov 2026. Period 3 (Dec-Mar): Released Feb/Mar 2027.",
        "schedule_2026_hi": "किस्त 1 (अप्रैल-जुलाई): मई/जून 2026 में जारी। किस्त 2 (अगस्त-नवंबर): अक्टूबर/नवंबर 2026 में जारी। किस्त 3 (दिसंबर-मार्च): फरवरी/मार्च 2027 में जारी।",
        "installment_calendar_2026": {
            "period_1_april_july": "May / June 2026 (₹2,000 DBT credit)",
            "period_2_aug_nov": "October / November 2026 (₹2,000 DBT credit)",
            "period_3_dec_mar": "February / March 2027 (₹2,000 DBT credit)",
            "mandatory_compliance": "Aadhaar e-KYC, Land Seeding (Khatauni), and NPCI bank account mapping"
        },
        "target": "All landholding farmer families in India (subject to exclusion criteria like institutional landholders/income tax payees).",
        "key_requirements": ["Aadhaar Card", "Landholding Records (Khatauni/Khasra/Patta)", "Aadhaar-seeded Active Bank Account", "e-KYC on PM-Kisan Portal"]
    },
    {
        "id": "pm-jay-ayushman",
        "name": "Ayushman Bharat PM-JAY (Pradhan Mantri Jan Arogya Yojana)",
        "name_hi": "आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना (PM-JAY)",
        "ministry": "National Health Authority (NHA) / Ministry of Health",
        "official_url": "https://pmjay.gov.in",
        "official_source": "pmjay.gov.in / nha.gov.in",
        "benefit": "Cashless health cover up to ₹5,00,000 per family per year for secondary and tertiary care hospitalization across 27,000+ empanelled hospitals.",
        "benefit_hi": "प्रति परिवार प्रति वर्ष ₹5,00,000 तक का मुफ्त कैशलेस स्वास्थ्य बीमा एवं अस्पताल में भर्ती उपचार।",
        "schedule_2026": "Open 24x7 / 365 days continuously. Card generation & enrollment active year-round in 2026 via Ayushman App & beneficiary.nha.gov.in.",
        "schedule_2026_hi": "वर्ष 2026 में 365 दिन 24x7 सतत खुला है। आयुष्मान ऐप व beneficiary.nha.gov.in पर कभी भी ई-केवाईसी कर कार्ड बनाएं।",
        "target": "Bottom 40% vulnerable and poor families identified via SECC database + Senior Citizens aged 70+ (All income brackets under Ayushman Vay Vandana).",
        "key_requirements": ["Aadhaar Card", "Ration Card (NFSA/BPL) or Family ID", "Mobile verification for Ayushman Card generation"]
    },
    {
        "id": "pm-awas-yojana",
        "name": "PM Awas Yojana (PMAY - Urban 2.0 & Gramin 2026)",
        "name_hi": "प्रधानमंत्री आवास योजना (PMAY - शहरी 2.0 एवं ग्रामीण)",
        "ministry": "Ministry of Housing and Urban Affairs & Ministry of Rural Development",
        "official_url": "https://pmaymis.gov.in",
        "official_source": "pmaymis.gov.in / pmayg.nic.in",
        "benefit": "Direct financial subsidy of ₹1.20 Lakhs (Plain areas) to ₹1.30 Lakhs (Hilly areas) in PMAY-Gramin; Credit-Linked Interest Subsidy (CLSS) up to ₹2.67 Lakhs in PMAY-Urban 2.0.",
        "benefit_hi": "पक्का मकान निर्माण हेतु ₹1.20 लाख से ₹1.30 लाख तक की प्रत्यक्ष वित्तीय सहायता अथवा गृह ऋण ब्याज सब्सिडी।",
        "schedule_2026": "PMAY 2.0 (2024-2029) 3-crore housing rollout. Rural surveys and urban online registrations active throughout 2026.",
        "schedule_2026_hi": "PMAY 2.0 (2024-2029) के तहत 3 करोड़ अतिरिक्त मकानों का निर्माण। ग्रामीण सर्वे एवं शहरी पोर्टल 2026 में सतत खुले हैं।",
        "target": "Homeless families and households living in kutcha/dilapidated houses (EWS, LIG, SC/ST, Women heads).",
        "key_requirements": ["Aadhaar Card", "Bank Account Details", "Land/House ownership document or declaration of no pucca house anywhere in India", "Income Certificate"]
    },
    {
        "id": "pm-vishwakarma",
        "name": "PM Vishwakarma Scheme (Support for Traditional Artisans)",
        "name_hi": "प्रधानमंत्री विश्वकर्मा योजना (पारंपरिक कारीगर व शिल्पकार)",
        "ministry": "Ministry of Micro, Small and Medium Enterprises (MSME)",
        "official_url": "https://pmvishwakarma.gov.in",
        "official_source": "pmvishwakarma.gov.in (Official MSME Portal)",
        "benefit": "PM Vishwakarma Certificate & ID Card + ₹15,000 Toolkit Incentive + Basic & Advanced Skill Training with ₹500/day stipend + Collateral-free enterprise loans up to ₹3 Lakhs at 5% interest.",
        "benefit_hi": "कारीगर प्रमाण पत्र + ₹15,00,0 का टूलकिट अनुदान + ₹500/दिन प्रशिक्षण स्टाइपेंड + ₹3 लाख तक का 5% रियायती ब्याज पर ऋण।",
        "schedule_2026": "Active enrollment open across all Common Service Centers (CSCs) and pmvishwakarma.gov.in throughout 2026.",
        "schedule_2026_hi": "वर्ष 2026 में सभी कॉमन सर्विस सेंटर्स (CSCs) एवं आधिकारिक पोर्टल पर सतत निःशुल्क पंजीकरण खुला है।",
        "target": "Traditional artisans and craftspeople working with hands and tools across 18 trades (Carpenters, Blacksmiths, Potters, Cobblers, Tailors, Masons, etc.).",
        "key_requirements": ["Aadhaar Card", "Active Mobile Number", "Bank Account Details", "Trade Self-Declaration verified by Gram Panchayat / Urban ULB"]
    },
    {
        "id": "pm-ujjwala-2",
        "name": "Pradhan Mantri Ujjwala Yojana (PMUY 2.0)",
        "name_hi": "प्रधानमंत्री उज्ज्वला योजना 2.0 (मुफ्त एलपीजी गैस कनेक्शन)",
        "ministry": "Ministry of Petroleum and Natural Gas",
        "official_url": "https://pmuy.gov.in",
        "official_source": "pmuy.gov.in",
        "benefit": "Deposit-free LPG connection along with first refill and gas stove (hotplate) free of cost + Targeted cooking gas subsidy of ₹300 per cylinder.",
        "benefit_hi": "मुफ्त गैस चूल्हा, पहला सिलेंडर रीफिल तथा सिलेंडर पर ₹300 की लक्षित सब्सिडी।",
        "schedule_2026": "Applications open year-round in 2026 at authorized LPG gas agencies (Indane, Bharatgas, HP Gas) and pmuy.gov.in.",
        "schedule_2026_hi": "वर्ष 2026 में सभी अधिकृत गैस एजेंसियों एवं pmuy.gov.in पर सतत नए गैस कनेक्शन हेतु आवेदन जारी हैं।",
        "target": "Adult woman from poor households (SC/ST/PMAY beneficiaries/Antyodaya/Forest dwellers/Most Backward Classes).",
        "key_requirements": ["Aadhaar of female applicant & adult family members", "Ration card", "Bank passbook for DBT subsidy"]
    }
]
