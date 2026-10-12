"""Loads REAL Sasthra product data (DRAFT) into MongoDB.

Run from the backend folder:
    python -m scripts.seed_real_products

Source: project owner's company overview + text from the Sasthra websites.
The company must review and approve this content before going live.
"""

from datetime import datetime, timezone

from app.db.mongodb import create_indexes, products_collection

OVERVIEW = (
    "Sasthra is an AI-powered education and learning platform that provides "
    "different products to support students, teachers, job seekers, and English "
    "learners. These platforms use digital technologies and AI to support learning, "
    "practice, feedback, assessments, and performance tracking, depending on their features."
)

REAL_PRODUCTS = [
    {
        "slug": "about-sasthra",
        "name": "About Sasthra (Company Overview)",
        "aliases": [],
        "category": "Company",
        "summary": OVERVIEW,
        "features": [
            "G-Sasthra (Intervu): interview preparation, resume improvement, and career guidance",
            "E-Sasthra: English language skills and IELTS and PTE exam preparation",
            "School of Sasthra (SOS): school education support through student learning, "
            "teacher support, parent monitoring, and administration",
            "SAI: NEET and JEE competitive exam preparation with AI-powered learning and teacher support",
        ],
        "services": [],
        "faqs": [
            {"question": "What is Sasthra?", "answer": OVERVIEW},
            {
                "question": "What products does Sasthra offer?",
                "answer": "Sasthra offers four main platforms: G-Sasthra (Intervu) for interview "
                "preparation, resume improvement, and career guidance; E-Sasthra for English "
                "language skills and IELTS and PTE preparation; School of Sasthra (SOS) for school "
                "education; and SAI for NEET and JEE preparation.",
            },
        ],
        "keywords": ["sasthra", "company", "about", "platforms", "products", "overview"],
    },
    {
        "slug": "g-sasthra-intervu",
        "name": "G-Sasthra (Intervu)",
        "aliases": ["Intervu", "G-Sasthra", "G Sasthra"],
        "category": "Career Guidance and Interview Preparation",
        "summary": "G-Sasthra, also called Intervu, is an AI-powered career readiness platform "
        "for interview preparation, resume building, and skill development. "
        "Website: https://g.sasthra.in",
        "features": [
            "Real-time AI interview practice (technical, HR, and behavioral rounds)",
            "ATS resume checker and optimizer",
            "AI-powered resume builder",
            "Career guidance and roadmap",
            "Aptitude and problem-solving tests",
            "Group discussion practice",
            "Visa interview preparation",
        ],
        "services": [],
        "faqs": [
            {
                "question": "What is Intervu (G-Sasthra)?",
                "answer": "Intervu is an AI-powered career readiness platform for interview "
                "preparation, resume building, and skill development.",
            },
            {
                "question": "What plans does Intervu have?",
                "answer": "Intervu has three plans. Personal (B2C): AI mock interviews, ATS checker, "
                "career guidance, aptitude tests, and group discussion practice. Academic (B2B): "
                "all Personal features plus campus placement preparation, bulk student management, "
                "a performance analytics dashboard, and visa interview preparation. Corporate (B2E): "
                "all Academic features plus custom interview templates, technical and HR modules, "
                "white-label solutions, and dedicated support with API access.",
            },
            {
                "question": "How does Intervu work?",
                "answer": "The journey has four steps: Assessment, Personalized Plan, "
                "Practice and Learn, and Get Hired.",
            },
        ],
        "keywords": [
            "intervu", "interview", "resume", "career", "ats", "job", "aptitude",
            "group discussion", "visa", "placement", "mock interview",
        ],
    },
    {
        "slug": "e-sasthra",
        "name": "E-Sasthra",
        "aliases": ["E Sasthra", "ESasthra"],
        "category": "English Learning",
        "summary": "E-Sasthra is an AI-powered English learning platform that helps users improve "
        "their English language skills and prepare for IELTS and PTE exams. "
        "Website: https://e.sasthra.in",
        "features": [
            "English language skills improvement",
            "IELTS exam preparation",
            "PTE exam preparation",
            "ESL learning",
            "Personalized learning",
            "Real-time evaluation, scoring, and feedback",
        ],
        "services": [],
        "faqs": [
            {
                "question": "What is E-Sasthra?",
                "answer": "E-Sasthra is an AI-powered English learning platform for improving "
                "English skills and preparing for IELTS and PTE exams.",
            },
            {
                "question": "Which exams does E-Sasthra help with?",
                "answer": "E-Sasthra helps users prepare for the IELTS and PTE exams.",
            },
        ],
        "keywords": ["e-sasthra", "english", "ielts", "pte", "esl", "language", "speaking", "exam"],
    },
    {
        "slug": "school-of-sasthra",
        "name": "School of Sasthra (SOS)",
        "aliases": ["School of Sasthra", "SOS", "Sasthra School"],
        "category": "School Education",
        "summary": "School of Sasthra (SOS) is an AI-powered education platform for students, "
        "teachers, and institutions. It supports school education through student learning, "
        "teacher support, parent monitoring, and administration. Website: https://sos.sasthra.in",
        "features": [
            "AI-powered personalized learning (adaptive algorithms, progress tracking, custom delivery)",
            "Teacher tools (analytics dashboard, learning-gap identification, instruction tools)",
            "Data-driven insights (real-time analytics, performance tracking, quality insights)",
            "Portal: Student Hub",
            "Portal: Parent Hub",
            "Portal: Classroom (faculty dashboard)",
            "Portal: Admin Console",
        ],
        "services": [],
        "faqs": [
            {
                "question": "What is School of Sasthra?",
                "answer": "School of Sasthra (SOS) is an AI-powered education platform that supports "
                "student learning, teacher support, parent monitoring, and school administration.",
            },
            {
                "question": "Which portals does School of Sasthra have?",
                "answer": "It has four portals: Student Hub, Parent Hub, Classroom (the faculty "
                "dashboard), and Admin Console.",
            },
        ],
        "keywords": [
            "sos", "school", "students", "teachers", "parents", "administration",
            "classroom", "analytics", "learning", "institution",
        ],
    },
    {
        "slug": "sai-neet-jee",
        "name": "SAI (NEET and JEE Preparation)",
        "aliases": ["SAI", "SAI Sasthra", "Sasthra SAI", "Sasthra NEET", "Sasthra JEE"],
        "category": "Competitive Exam Preparation",
        "summary": "SAI focuses on NEET and JEE competitive exam preparation with AI-powered "
        "learning and teacher support. Website: https://sai.sasthra.in",
        "features": [
            "NEET preparation",
            "JEE preparation",
            "AI-powered learning",
            "Teacher and mentor support",
            "Multilanguage live classes",
            "Smart learning tools",
            "Online mock tests",
        ],
        "services": [],
        "faqs": [
            {
                "question": "What is SAI?",
                "answer": "SAI is the Sasthra platform for NEET and JEE competitive exam "
                "preparation with AI-powered learning and teacher support.",
            },
        ],
        "keywords": ["sai", "neet", "jee", "coaching", "mock tests", "live classes", "exam", "medical", "engineering"],
    },
]


def seed() -> None:
    create_indexes()
    now = datetime.now(timezone.utc)

    for product in REAL_PRODUCTS:
        doc = {**product, "is_sample": False, "is_active": True, "updated_at": now}
        products_collection.update_one(
            {"slug": product["slug"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )

    print(f"Seeded {len(REAL_PRODUCTS)} REAL products (draft, pending company approval).")


if __name__ == "__main__":
    seed()