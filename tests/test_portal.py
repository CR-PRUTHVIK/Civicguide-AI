"""
Automated unit and integration tests for JanSeva Info Portal
Testing:
1. JanSeva AI Citizen Assistant Chatbot API (/api/chat)
2. Hindi & English Bilingual Guidance
3. Official Government Sources
4. Check Eligibility Wizard API
5. State-Wise Welfares, Scholarships & Select State Hub
6. Popular Exams & Welfare Schemes Datasets
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data.scholarships import SCHOLARSHIPS_DATA
from app.data.caste_certificate import CASTE_CERTIFICATE_DATA
from app.data.voter_services import VOTER_SERVICES_DATA
from app.data.civic_services import CIVIC_SERVICES_DATA
from app.data.state_portals import STATE_PORTALS_DATA
from app.data.exams import POPULAR_EXAMS_DATA
from app.data.welfare_schemes import NATIONAL_WELFARES_DATA
from app.data.faqs import FAQS_DATA, GRIEVANCE_DIRECTORY

client = TestClient(app)


def test_homepage_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "CivicGuide AI" in response.text
    assert "Scholarships" in response.text
    assert "UPSC" in response.text
    assert "PM-KISAN" in response.text


def test_ai_chatbot_api_upsc_exam():
    response = client.post("/api/chat", json={"message": "What is the age limit and number of attempts for UPSC IAS exam?", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "UPSC" in data["title"] or "Civil Services" in data["title"]
    assert "21 to 32 Years" in data["answer"]
    assert "6 Attempts" in data["answer"]
    assert "upsc.gov.in" in data["official_source"]


def test_ai_chatbot_api_ssc_cgl_exam():
    response = client.post("/api/chat", json={"message": "What are the posts and qualification for SSC CGL exam?", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "SSC" in data["title"]
    assert "Income Tax Inspector" in data["answer"] or "ASO" in data["answer"]
    assert "ssc.gov.in" in data["official_source"]


def test_ai_chatbot_api_neet_jee_exams():
    response = client.post("/api/chat", json={"message": "What is the eligibility and age limit for NEET UG exam?", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "NEET" in data["title"]
    assert "17 years" in data["answer"]


def test_ai_chatbot_api_scholarship():
    response = client.post("/api/chat", json={"message": "What is NSP OTR and how do I apply for post matric scholarship?", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "OTR" in data["title"] or "Scholarship" in data["title"]
    assert "scholarships.gov.in" in data["official_source"]


def test_ai_chatbot_api_caste_obc():
    response = client.post("/api/chat", json={"message": "What is the income limit for OBC non creamy layer?", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "8,00,000" in data["answer"] or "8 Lakh" in data["answer"]


def test_ai_chatbot_api_hindi():
    response = client.post("/api/chat", json={"message": "वोटर कार्ड फॉर्म 6 कैसे भरें?", "lang": "hi"})
    assert response.status_code == 200
    data = response.json()
    assert "प्रारूप 6" in data["answer"] or "Form 6" in data["answer"]


def test_scholarships_page_loads():
    response = client.get("/scholarships")
    assert response.status_code == 200
    assert "Post-Matric Scholarship" in response.text


def test_caste_certificate_page_loads():
    response = client.get("/caste-certificate")
    assert response.status_code == 200
    assert "Scheduled Caste" in response.text
    assert "Non-Creamy Layer" in response.text


def test_voter_services_page_loads():
    response = client.get("/voter-services")
    assert response.status_code == 200
    assert "Form 6" in response.text
    assert "Form 8" in response.text


def test_civic_services_page_loads():
    response = client.get("/civic-services")
    assert response.status_code == 200
    assert "Registration of Births and Deaths" in response.text
    assert "Parivahan" in response.text


def test_state_directory_page_loads():
    response = client.get("/state-directory")
    assert response.status_code == 200
    assert "Maharashtra" in response.text
    assert "Uttar Pradesh" in response.text


def test_checklist_builder_page_loads():
    response = client.get("/checklist-builder")
    assert response.status_code == 200
    assert "Document Checklist Builder" in response.text


def test_faqs_page_loads():
    response = client.get("/faqs")
    assert response.status_code == 200
    assert "Anti-Fraud Warning" in response.text


def test_api_search_returns_results():
    response = client.get("/api/search?q=upsc")
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] > 0
    assert len(data["results"]["exams"]) > 0


def test_api_full_eligibility_wizard():
    payload = {
        "age": "18-25",
        "education": "Graduation",
        "category": "SC",
        "income": 200000,
        "gender_status": "Female",
        "state": "maharashtra"
    }
    response = client.post("/api/check-full-eligibility", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["central_scholarships"]) > 0
    assert data["state_info"]["state_name"] == "Maharashtra"


def test_popular_exams_and_welfares_data():
    assert len(POPULAR_EXAMS_DATA) >= 5
    assert len(NATIONAL_WELFARES_DATA) >= 4
    for ex in POPULAR_EXAMS_DATA:
        assert "name" in ex
        assert "conducted_by" in ex
    for w in NATIONAL_WELFARES_DATA:
        assert "name" in w
        assert "ministry" in w


def test_ai_chatbot_jee_2026_schedule_query():
    # User's exact prompt test
    response = client.post("/api/chat", json={"message": "when does the JEE exam for year 2026 start", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "JEE Main & Advanced 2026" in data["title"]
    assert "Session 1" in data["answer"]
    assert "January 22 to January 31, 2026" in data["answer"]
    assert "Session 2" in data["answer"]
    assert "April 1 to April 15, 2026" in data["answer"]
    assert "jeemain.nta.nic.in" in data["official_source"]


def test_ai_chatbot_pm_kisan_2026_schedule_query():
    # Welfare scheme schedule query
    response = client.post("/api/chat", json={"message": "when does PM kisan 2026 installment come", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "PM-KISAN" in data["title"]
    assert "2026" in data["title"]
    assert "Period 1" in data["answer"] or "Installment" in data["answer"]
    assert "May / June 2026" in data["answer"]
    assert "pmkisan.gov.in" in data["official_source"]


def test_ai_chatbot_neet_2026_schedule_query():
    response = client.post("/api/chat", json={"message": "What is the NEET 2026 exam date and timing?", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "NEET-UG 2026" in data["title"]
    assert "Sunday, May 3, 2026" in data["answer"]
    assert "neet.nta.nic.in" in data["official_source"]


def test_ai_chatbot_ayushman_bharat_2026_schedule():
    response = client.post("/api/chat", json={"message": "when can I apply for Ayushman Bharat card in 2026?", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert "Ayushman Bharat" in data["title"]
    assert "Open 24x7 / 365 Days Year-Round" in data["answer"]
    assert "70" in data["answer"] or "Vay Vandana" in data["answer"]
    assert "beneficiary.nha.gov.in" in data["official_source"]


def test_state_welfare_schemes_expanded():
    assert len(STATE_PORTALS_DATA) >= 28
    for st in STATE_PORTALS_DATA:
        assert "state_welfares" in st
        assert len(st["state_welfares"]) >= 3
        for w in st["state_welfares"]:
            assert "name" in w
            assert "description" in w
            assert len(w["description"]) > 10

    # Test that flagship schemes exist for major states
    mh = next(s for s in STATE_PORTALS_DATA if s["id"] == "maharashtra")
    welfare_names_mh = [w["name"] for w in mh["state_welfares"]]
    assert any("Majhi Ladki Bahin" in name for name in welfare_names_mh)
    assert any("Mahatma Jyotirao Phule" in name for name in welfare_names_mh)

    ka = next(s for s in STATE_PORTALS_DATA if s["id"] == "karnataka")
    welfare_names_ka = [w["name"] for w in ka["state_welfares"]]
    assert any("Gruha Lakshmi" in name for name in welfare_names_ka)
    assert any("Shakti" in name for name in welfare_names_ka)
    assert any("Yuva Nidhi" in name for name in welfare_names_ka)


def test_ai_chatbot_specific_exam_aspects_jee():
    # 1. Duration / Time Allotted
    r1 = client.post("/api/chat", json={"message": "what is the exact time alloted for completion of JEE exam", "lang": "en"})
    assert r1.status_code == 200
    d1 = r1.json()
    assert "Duration" in d1["title"] or "Time Allotted" in d1["title"]
    assert "3 Hours (180 Minutes)" in d1["answer"]
    assert "9:00 AM to 12:00 PM" in d1["answer"]

    # 2. Marking Scheme & Negative Marking
    r2 = client.post("/api/chat", json={"message": "what is the negative marking in JEE main", "lang": "en"})
    assert r2.status_code == 200
    d2 = r2.json()
    assert "Marking Scheme" in d2["title"]
    assert "+4" in d2["answer"] and "-1" in d2["answer"]

    # 3. 75% Rule & Eligibility
    r3 = client.post("/api/chat", json={"message": "what is the 75 percent criteria in jee", "lang": "en"})
    assert r3.status_code == 200
    d3 = r3.json()
    assert "Eligibility" in d3["title"] or "75%" in d3["answer"]
    assert "75%" in d3["answer"]


def test_ai_chatbot_specific_exam_aspects_neet_upsc_nda():
    # NEET duration
    r_neet = client.post("/api/chat", json={"message": "what is the exact duration of NEET exam", "lang": "en"})
    assert r_neet.status_code == 200
    d_neet = r_neet.json()
    assert "200 Minutes" in d_neet["answer"] or "3 Hours" in d_neet["answer"]

    # UPSC negative marking
    r_upsc = client.post("/api/chat", json={"message": "what is the negative marking in UPSC CSE", "lang": "en"})
    assert r_upsc.status_code == 200
    d_upsc = r_upsc.json()
    assert "-0.66" in d_upsc["answer"] or "1/3" in d_upsc["answer"]

    # NDA age limit
    r_nda = client.post("/api/chat", json={"message": "what is the age limit for nda 2026", "lang": "en"})
    assert r_nda.status_code == 200
    d_nda = r_nda.json()
    assert "16.5 to 19.5" in d_nda["answer"]

