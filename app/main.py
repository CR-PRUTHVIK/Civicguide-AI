"""
CivicGuide AI Portal - Indian Civil Services Information Web Application
FastAPI Main Application
Features:
1. CivicGuide AI Citizen Assistant Chatbot API
2. Hindi & English Bilingual Guidance
3. Verified Official Government Links & Sources
4. Check Eligibility (Top Right Placement) & Step-by-Step Wizard
5. State-Wise Welfares, Scholarships & Select State Hub
6. Popular Civil Services Exams & Flagship Welfares
"""

import os
from typing import List, Optional
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.data.scholarships import SCHOLARSHIPS_DATA
from app.data.caste_certificate import CASTE_CERTIFICATE_DATA
from app.data.voter_services import VOTER_SERVICES_DATA
from app.data.civic_services import CIVIC_SERVICES_DATA
from app.data.state_portals import STATE_PORTALS_DATA
from app.data.exams import POPULAR_EXAMS_DATA
from app.data.welfare_schemes import NATIONAL_WELFARES_DATA
from app.data.faqs import FAQS_DATA, GRIEVANCE_DIRECTORY
from app.data.chatbot_engine import process_citizen_query

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="CivicGuide AI - Indian Civil Services Portal",
    description="Comprehensive, accurate guide to Indian Civil Services: Scholarships, Caste Certificates, Voter Services, Civic Services, Exams & Welfares",
    version="1.2.0"
)

# Disable browser caching in development so edits always appear immediately
@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Mount static files
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates_dir = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=templates_dir)


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "page_title": "Home - National Civil & Civic Services Portal",
            "scholarships_count": len(SCHOLARSHIPS_DATA),
            "states_count": len(STATE_PORTALS_DATA),
            "civic_services_count": len(CIVIC_SERVICES_DATA),
            "voter_forms_count": len(VOTER_SERVICES_DATA["forms"]),
            "states": STATE_PORTALS_DATA,
            "popular_exams": POPULAR_EXAMS_DATA,
            "national_welfares": NATIONAL_WELFARES_DATA,
            "popular_scholarships": SCHOLARSHIPS_DATA[:4]
        }
    )


@app.get("/scholarships", response_class=HTMLResponse)
async def scholarships_page(
    request: Request,
    category: Optional[str] = Query(None),
    education: Optional[str] = Query(None),
    max_income: Optional[int] = Query(None)
):
    filtered_scholarships = SCHOLARSHIPS_DATA
    if category and category != "all":
        filtered_scholarships = [
            s for s in filtered_scholarships
            if category.lower() in s["category"].lower() or "all" in s["category"].lower()
        ]
    if education and education != "all":
        filtered_scholarships = [
            s for s in filtered_scholarships
            if any(education.lower() in ed.lower() for ed in s["education_level"])
        ]
    if max_income:
        filtered_scholarships = [
            s for s in filtered_scholarships
            if s["max_income_inr"] >= max_income
        ]

    return templates.TemplateResponse(
        request=request,
        name="scholarships.html",
        context={
            "page_title": "National Scholarships Portal (NSP & State Schemes)",
            "scholarships": filtered_scholarships,
            "all_scholarships": SCHOLARSHIPS_DATA,
            "selected_category": category or "all",
            "selected_education": education or "all",
            "selected_income": max_income or "",
            "states": STATE_PORTALS_DATA
        }
    )


@app.get("/caste-certificate", response_class=HTMLResponse)
async def caste_certificate_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="caste_certificate.html",
        context={
            "page_title": "Caste Certificate (जाति प्रमाण पत्र) Complete Guide",
            "data": CASTE_CERTIFICATE_DATA,
            "states": STATE_PORTALS_DATA
        }
    )


@app.get("/voter-services", response_class=HTMLResponse)
async def voter_services_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="voter_services.html",
        context={
            "page_title": "ECI Voter Services & Electoral Registration Guide",
            "data": VOTER_SERVICES_DATA,
            "states": STATE_PORTALS_DATA
        }
    )


@app.get("/civic-services", response_class=HTMLResponse)
async def civic_services_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="civic_services.html",
        context={
            "page_title": "Civic & Municipal Services Guide",
            "civic_services": CIVIC_SERVICES_DATA,
            "states": STATE_PORTALS_DATA
        }
    )


@app.get("/state-directory", response_class=HTMLResponse)
async def state_directory_page(
    request: Request,
    filter_type: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    state_id: Optional[str] = Query(None)
):
    states = STATE_PORTALS_DATA
    selected_state_obj = None

    if state_id:
        for s in states:
            if s.get("id") == state_id or s["state_name"].lower() == state_id.lower():
                selected_state_obj = s
                break

    if filter_type and filter_type != "all":
        states = [s for s in states if s["type"].lower() == filter_type.lower()]
    if q:
        query_str = q.lower()
        states = [
            s for s in states
            if query_str in s["state_name"].lower() or any(query_str in srv.lower() for srv in s["key_services"])
        ]

    return templates.TemplateResponse(
        request=request,
        name="state_directory.html",
        context={
            "page_title": "Select State - 28 States & 8 UTs Citizen Services & Scholarships",
            "states": states,
            "all_states": STATE_PORTALS_DATA,
            "selected_filter": filter_type or "all",
            "search_query": q or "",
            "selected_state_obj": selected_state_obj
        }
    )


@app.get("/checklist-builder", response_class=HTMLResponse)
async def checklist_builder_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="checklist_builder.html",
        context={
            "page_title": "Interactive Document Checklist Generator",
            "caste_data": CASTE_CERTIFICATE_DATA,
            "voter_data": VOTER_SERVICES_DATA,
            "civic_data": CIVIC_SERVICES_DATA,
            "scholarships_data": SCHOLARSHIPS_DATA,
            "states": STATE_PORTALS_DATA
        }
    )


@app.get("/faqs", response_class=HTMLResponse)
async def faqs_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="faqs.html",
        context={
            "page_title": "FAQs, Anti-Fraud Safety & Grievance Redressal",
            "faqs": FAQS_DATA,
            "grievance_directory": GRIEVANCE_DIRECTORY,
            "states": STATE_PORTALS_DATA
        }
    )


# ---------------- API ENDPOINTS ----------------

@app.post("/api/chat")
async def api_chat(request: Request):
    """
    JanSeva AI Citizen Assistant Chat Endpoint
    """
    body = await request.json()
    query = body.get("message", "")
    lang = body.get("lang", "en")
    
    if not query.strip():
        return JSONResponse({
            "title": "JanSeva AI",
            "answer": "Please enter your question regarding Indian civil services, scholarships, or certificates.",
            "official_source": "india.gov.in",
            "suggested_links": []
        })

    response_data = process_citizen_query(query, lang)
    return JSONResponse(response_data)


@app.get("/api/search")
async def api_search(q: str = Query(..., min_length=1)):
    query = q.lower().strip()
    results = {
        "scholarships": [],
        "caste_categories": [],
        "voter_forms": [],
        "civic_services": [],
        "state_portals": [],
        "exams": [],
        "welfares": []
    }

    # Search scholarships
    for item in SCHOLARSHIPS_DATA:
        if (
            query in item["title"].lower()
            or query in item.get("title_hi", "").lower()
            or query in item["description"].lower()
            or query in item["ministry"].lower()
            or query in item["category"].lower()
            or any(query in tag.lower() for tag in item.get("tags", []))
        ):
            results["scholarships"].append({
                "title": item["title"],
                "url": f"/scholarships#{item['id']}",
                "badge": item["category"],
                "description": item["description"][:120] + "..."
            })

    # Search exams
    for ex in POPULAR_EXAMS_DATA:
        if (
            query in ex["name"].lower()
            or query in ex.get("name_hi", "").lower()
            or query in ex["conducted_by"].lower()
            or any(query in svc.lower() for svc in ex["key_services"])
        ):
            results["exams"].append({
                "title": ex["name"],
                "url": "/#exams-section",
                "badge": ex["conducted_by"],
                "description": f"Age: {ex['eligibility_age']} | {ex['qualification']}"
            })

    # Search welfare schemes
    for wel in NATIONAL_WELFARES_DATA:
        if (
            query in wel["name"].lower()
            or query in wel.get("name_hi", "").lower()
            or query in wel["ministry"].lower()
        ):
            results["welfares"].append({
                "title": wel["name"],
                "url": "/#welfare-section",
                "badge": wel["ministry"],
                "description": wel["benefit"][:120] + "..."
            })

    # Search caste certificate categories
    for cat in CASTE_CERTIFICATE_DATA["categories"]:
        if query in cat["name"].lower() or query in cat["hindi_name"] or query in cat["constitutional_basis"].lower():
            results["caste_categories"].append({
                "title": f"Caste Certificate: {cat['name']} ({cat['hindi_name']})",
                "url": f"/caste-certificate#{cat['id']}",
                "badge": cat["id"].upper(),
                "description": f"Valid for {cat['validity']}. Cut-off date: {cat['cut_off_date']}"
            })

    # Search voter forms
    for form in VOTER_SERVICES_DATA["forms"]:
        if (
            query in form["form_number"].lower()
            or query in form["title"].lower()
            or query in form["purpose"].lower()
        ):
            results["voter_forms"].append({
                "title": f"{form['form_number']}: {form['title']}",
                "url": f"/voter-services#{form['form_number']}",
                "badge": form["form_number"],
                "description": form["purpose"][:120] + "..."
            })

    # Search civic services
    for srv in CIVIC_SERVICES_DATA:
        if (
            query in srv["category_title"].lower()
            or query in srv["overview"].lower()
            or query in srv["statutory_act"].lower()
        ):
            results["civic_services"].append({
                "title": srv["category_title"],
                "url": f"/civic-services#{srv['id']}",
                "badge": srv["issuing_portal"],
                "description": srv["overview"][:120] + "..."
            })

    # Search state portals, welfare schemes, and scholarships
    for st in STATE_PORTALS_DATA:
        matched_welfare = any(
            query in w["name"].lower() or query in w.get("description", "").lower() or (w.get("name_hi") and query in w["name_hi"].lower())
            for w in st.get("state_welfares", [])
        )
        matched_scholarship = any(
            query in s["name"].lower() or (s.get("name_hi") and query in s["name_hi"].lower())
            for s in st.get("state_scholarships", [])
        )
        if (
            query in st["state_name"].lower()
            or query in st.get("state_name_hi", "").lower()
            or query in st["portal_name"].lower()
            or any(query in srv.lower() for srv in st["key_services"])
            or matched_welfare
            or matched_scholarship
        ):
            results["state_portals"].append({
                "title": f"{st['state_name']} - {st['portal_name']}",
                "url": f"/state-directory?state_id={st['id']}",
                "badge": st["type"],
                "description": f"Welfares & Services: {', '.join(st['key_services'][:3])}"
            })

    total_count = sum(len(v) for v in results.values())
    return {
        "query": q,
        "total_results": total_count,
        "results": results
    }


@app.post("/api/check-full-eligibility")
async def check_full_eligibility(request: Request):
    body = await request.json()
    age = body.get("age", "")
    education = body.get("education", "")
    category = body.get("category", "")
    try:
        income = float(body.get("income", 250000))
    except Exception:
        income = 250000.0
    gender_status = body.get("gender_status", "")
    state_id = body.get("state", "").lower()

    # Match central scholarships
    matched_scholarships = []
    for s in SCHOLARSHIPS_DATA:
        match = True
        cat_lower = s["category"].lower()

        # Check gender / PwD
        if "female" in cat_lower and gender_status != "Female":
            match = False
        elif ("pwd" in cat_lower or "disabilit" in cat_lower) and gender_status != "PwD":
            match = False
        elif "all" not in cat_lower:
            if category:
                if category == "General" and ("sc" in cat_lower or "st" in cat_lower or "obc" in cat_lower or "minority" in cat_lower):
                    match = False
                elif category == "OBC" and ("sc" in cat_lower or "st" in cat_lower or "minority" in cat_lower):
                    match = False
                elif category == "SC" and ("st" in cat_lower or "minority" in cat_lower or ("obc" in cat_lower and "sc" not in cat_lower)):
                    match = False
                elif category == "ST" and ("sc" in cat_lower or "minority" in cat_lower or ("obc" in cat_lower and "st" not in cat_lower)):
                    match = False

        if education and match and education != "Non-Student":
            ed_matched = any(education.lower() in ed.lower() for ed in s["education_level"])
            if not ed_matched:
                match = False

        if income and match:
            if income > s["max_income_inr"]:
                match = False

        if match:
            matched_scholarships.append(s)

    # Find State Info
    matched_state = None
    for st in STATE_PORTALS_DATA:
        if st.get("id") == state_id or st["state_name"].lower().replace(" ", "-") in state_id or state_id in st["state_name"].lower():
            matched_state = st
            break
    
    if not matched_state and len(STATE_PORTALS_DATA) > 0:
        matched_state = STATE_PORTALS_DATA[0]

    # Voter Status
    if age in ["18-25", "26-40", "above-40"]:
        voter_msg = "Eligible to Register as Voter (Form 6) / Update Details (Form 8) on voters.eci.gov.in"
    else:
        voter_msg = "Advance registration open for youths turning 18 on upcoming qualifying dates (1 Jan, 1 Apr, 1 Jul, 1 Oct)"

    # Category Status
    cat_names = {
        "SC": {"name": "Scheduled Caste (SC) - Lifetime Validity (Article 341)", "url": "/caste-certificate#sc"},
        "ST": {"name": "Scheduled Tribe (ST) - Lifetime Validity (Article 342)", "url": "/caste-certificate#st"},
        "OBC": {"name": "OBC Non-Creamy Layer - 1 Year Validity (Income < ₹8L)", "url": "/caste-certificate#obc-ncl"},
        "EWS": {"name": "EWS Certificate - 1 Year Validity (Income < ₹8L & Asset Rules)", "url": "/caste-certificate#ews"},
        "General": {"name": "General / Unreserved - Eligible for EWS (if income < ₹8L) & Merit Schemes", "url": "/caste-certificate#ews"},
        "Minority": {"name": "Notified Minority Community - Eligible for MoMA Schemes", "url": "/scholarships"}
    }

    return {
        "central_scholarships": matched_scholarships,
        "state_info": matched_state,
        "voter_status": voter_msg,
        "category_status": cat_names.get(category, {"name": category, "url": "/caste-certificate"})
    }
