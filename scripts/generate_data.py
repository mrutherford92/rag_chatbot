"""
Script Name:  generate_data.py
Description:  Generates synthetic medical case study PDFs for testing the RAG system.
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

from app.core.config import DATA_DIR
os.makedirs(DATA_DIR, exist_ok=True)

CASES = [
    {
        "filename": "cardiology_case.pdf",
        "title": "Medical Report: Cardiology Follow-up",
        "content": """
        Patient: Sarah Connor. Age: 58. Date: 2023-11-12.
        Chief Complaint: Intermittent chest tightness and palpitations.
        History: HTN. Episodes of racing heart 2-3x/week.
        Vitals: BP 135/85, HR 78 (irregular).
        Assessment: Suspected Atrial Fibrillation paroxysms.
        Plan: Holter monitor 48h. Echocardiogram. Continue Lisinopril 10mg.
        """
    },
    {
        "filename": "endocrinology_case.pdf",
        "title": "Medical Report: Diabetes Management",
        "content": """
        Patient: Kyle Reese. Age: 32. Date: 2023-11-15.
        Chief Complaint: Polydipsia and frequent urination.
        History: Weight loss 5kg. Family hx Type 1 DM.
        Labs: Glucose 280 mg/dL. HbA1c 9.2%.
        Assessment: New-onset Type 1 Diabetes Mellitus.
        Plan: Insulin Glargine 10u HS. Insulin Aspart sliding scale. Carb counting info.
        """
    },
    {
        "filename": "neurology_case.pdf",
        "title": "Medical Report: Migraine Assessment",
        "content": """
        Patient: Ellen Ripley. Age: 40. Date: 2023-11-18.
        Chief Complaint: Severe unilateral headaches with visual aura.
        History: Throbbing pain 8/10, photophobia.
        Neuro Exam: Normal.
        Assessment: Migraine with Aura.
        Plan: Sumatriptan 50mg PO PRN. MRI Brain to rule out secondary causes.
        """
    },
    {
        "filename": "pediatric_case.pdf",
        "title": "Medical Report: Pediatric Checkup",
        "content": """
        Patient: Newt J. Age: 6. Date: 2023-11-20.
        Chief Complaint: Left ear pain.
        History: Rhinorrhea, fever.
        Exam: Left TM bulging, erythematous.
        Assessment: Acute Otitis Media (Left).
        Plan: Amoxicillin 400mg/5mL - 5mL BID x7d. Acetaminophen.
        """
    },
    {
        "filename": "orthopedic_case.pdf",
        "title": "Medical Report: Knee Injury",
        "content": """
        Patient: T. Stark. Age: 45. Date: 2023-11-22.
        Chief Complaint: Right knee pain after skiing.
        History: Twisted knee, heard "pop".
        Exam: Moderate effusion. Lachman +ve.
        Assessment: Suspected ACL tear.
        Plan: RICE. MRI Right Knee. Ortho referral. Crutches.
        """
    },
    {
        "filename": "pulmonology_case.pdf",
        "title": "Medical Report: Asthma Exacerbation",
        "content": """
        Patient: Bruce Wayne. Age: 35. Date: 2023-11-25.
        Chief Complaint: Shortness of breath and wheezing.
        History: History of childhood asthma. Exposure to dust in old manor.
        Exam: Diffuse expiratory wheezes bilateral. O2 Sat 94%.
        Assessment: Mild Asthma Exacerbation.
        Plan: Albuterol neb. Prednisone 40mg x 5 days. Review inhaler technique.
        """
    },
    {
        "filename": "gastro_case.pdf",
        "title": "Medical Report: GERD",
        "content": """
        Patient: Clark Kent. Age: 38. Date: 2023-11-26.
        Chief Complaint: Heartburn and acid regurgitation.
        History: Worse after spicy food or lying down.
        Assessment: Gastroesophageal Reflux Disease (GERD).
        Plan: Omeprazole 20mg daily. Lifestyle changes (elevate head of bed).
        """
    },
    {
        "filename": "dermatology_case.pdf",
        "title": "Medical Report: Skin Lesion",
        "content": """
        Patient: Peter Parker. Age: 18. Date: 2023-11-27.
        Chief Complaint: Itchy red patches on elbows.
        Exam: Erythematous plaques with silvery scale.
        Assessment: Psoriasis Vulgaris.
        Plan: Triamcinolone 0.1% cream BID. Moisturize frequently.
        """
    },
    {
        "filename": "psychiatry_case.pdf",
        "title": "Medical Report: Mental Health Consult",
        "content": """
        Patient: Diana Prince. Age: 300. Date: 2023-11-28.
        Chief Complaint: Low mood and loss of interest.
        History: Feeling isolated. difficulty sleeping.
        MSE: Affect restricted. Mood depressed. No SI/HI.
        Assessment: Major Depressive Disorder, single episode, moderate.
        Plan: Start Sertraline 50mg. Referral for CBT.
        """
    },
    {
        "filename": "obgyn_case.pdf",
        "title": "Medical Report: Prenatal Visit",
        "content": """
        Patient: Padme Amidala. Age: 27. Date: 2023-11-29.
        Chief Complaint: Routine prenatal check up (24 weeks).
        Vitals: BP 110/70. Fetal Heart Rate 145 bpm.
        Assessment: Intrauterine Pregnancy at 24 weeks. Normal growth.
        Plan: Glucose tolerance test next visit. Tdap vaccine today.
        """
    },
    {
        "filename": "urology_case.pdf",
        "title": "Medical Report: Flank Pain",
        "content": """
        Patient: Logan H. Age: 150. Date: 2023-11-30.
        Chief Complaint: Sudden onset right flank pain radiating to groin.
        History: 10/10 colicky pain. Nausea.
        Urinalysis: Microscopic hematuria.
        Assessment: Ureterolithiasis (Kidney Stone), likely passing.
        Plan: CT KUB. Tamsulosin 0.4mg. Pain control with NSAIDs. Hydration.
        """
    },
    {
        "filename": "hematology_case.pdf",
        "title": "Medical Report: Fatigue Assessment",
        "content": """
        Patient: Steve Rogers. Age: 105. Date: 2023-12-01.
        Chief Complaint: Feeling tired despite rest.
        Labs: Hgb 10.5 g/dL. MCV 72 (low). Ferritin low.
        Assessment: Iron Deficiency Anemia.
        Plan: Ferrous Sulfate 325mg daily with Vitamin C. dietary counseling.
        """
    },
    {
        "filename": "ophthalmology_case.pdf",
        "title": "Medical Report: Eye Check",
        "content": """
        Patient: Nick Fury. Age: 60. Date: 2023-12-02.
        Chief Complaint: Blurry vision in remaining eye.
        Exam: Clouding of the lens observed on slit lamp.
        Assessment: Age-related Cataract.
        Plan: Referral for cataract surgery evaluation. Updated prescription glasses.
        """
    },
    {
        "filename": "rheumatology_case.pdf",
        "title": "Medical Report: Joint Pain",
        "content": """
        Patient: Bucky Barnes. Age: 35. Date: 2023-12-03.
        Chief Complaint: Morning stiffness in hands lasting >1 hour.
        Exam: Swelling in MCP joints bilaterally.
        Labs: RF Positive. Anti-CCP Positive.
        Assessment: Rheumatoid Arthritis.
        Plan: Start Methotrexate. Folic acid supplement. Refer to infusion center.
        """
    },
    {
        "filename": "infectious_case.pdf",
        "title": "Medical Report: Fever Consult",
        "content": """
        Patient: Barry Allen. Age: 28. Date: 2023-12-04.
        Chief Complaint: High fever, chills, myalgia.
        History: Rapid onset.
        Exam: Temp 39.5 C. Rhinorrhea.
        Test: Influenza A Positive.
        Assessment: Seasonal Influenza.
        Plan: Oseltamivir 75mg BID x5d. Isolation. Hydration.
        """
    },
    {
        "filename": "geriatrics_case.pdf",
        "title": "Medical Report: Memory Evaluation",
        "content": """
        Patient: Charles Xavier. Age: 75. Date: 2023-12-05.
        Chief Complaint: Short term memory loss.
        History: Getting lost in familiar places.
        Cognitive: MMSE 22/30. Difficulty with recall.
        Assessment: Mild Cognitive Impairment / Early Alzheimers.
        Plan: MRI Brain. Start Donepezil 5mg. Neuropsych testing.
        """
    },
    {
        "filename": "emergency_case.pdf",
        "title": "Medical Report: Abdominal Pain",
        "content": """
        Patient: Arthur Curry. Age: 33. Date: 2023-12-06.
        Chief Complaint: RLQ Abdominal pain.
        Exam: Rebound tenderness at McBurney's point.
        Labs: WBC 14,000 (Elevated).
        Assessment: Acute Appendicitis.
        Plan: NPO. IV Antibiotics. Surgical Consult for Appendectomy.
        """
    },
    {
        "filename": "nephrology_case.pdf",
        "title": "Medical Report: Renal Function",
        "content": """
        Patient: Lex Luthor. Age: 45. Date: 2023-12-07.
        Chief Complaint: Follow up for Hypertension.
        Labs: Creatinine 1.4. eGFR 55. Proteinuria 1+.
        Assessment: Chronic Kidney Disease Stage 3a.
        Plan: BP control < 130/80. Switch to ARB (Losartan). Low salt diet.
        """
    },
    {
        "filename": "ent_case.pdf",
        "title": "Medical Report: Throat Pain",
        "content": """
        Patient: Hal Jordan. Age: 32. Date: 2023-12-08.
        Chief Complaint: Severe sore throat and trouble swallowing.
        Exam: Enlarged tonsils with exudate. Anterior cervical lymphadenopathy.
        Centor Score: 4.
        Assessment: Streptococcal Pharyngitis (Strep Throat).
        Plan: Penicillin VK 500mg BID x10d.
        """
    },
    {
        "filename": "allergy_case.pdf",
        "title": "Medical Report: Allergic Reaction",
        "content": """
        Patient: Miles Morales. Age: 16. Date: 2023-12-09.
        Chief Complaint: Hives and lip swelling after eating a cookie.
        Exam: Urticaria on face/neck. Wheezing mild.
        Assessment: Anaphylaxis (Early stage) / Acute Food Allergy.
        Plan: Epinephrine 0.3mg IM given immediately. Observe 4 hours. Prescribe EpiPen.
        """
    }
]

def create_pdf(case: dict[str, Any]) -> None:
    """
    Generates a single PDF page for a given medical case.
    
    Args:
        case (dict): Dictionary containing filename, title, and content content.
    """
    path = os.path.join(DATA_DIR, case["filename"])
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, case["title"])
    
    # Content Body
    c.setFont("Helvetica", 12)
    y = height - 100
    
    for line in case["content"].strip().split('\n'):
        clean_line = line.strip()
        if not clean_line:
            y -= 10
            continue
            
        c.drawString(72, y, clean_line)
        y -= 20
        
        # Simple pagination check (though cases are single-page by design)
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 72
            
    c.save()
    print(f"Generated: {case['filename']}")

if __name__ == "__main__":
    print(f"Generating {len(CASES)} cases...")
    for case in CASES:
        create_pdf(case)
