from typing import Dict

"""
This dictionary is made for updating name changes in the schema this is a way to keep backwards compatibility for the user and hopefully inform them to use the new names
"""
CONVERSIONMAP: Dict[str, str] = {
    "ResearchSubject.associated_project": "ResearchSubject.member_of_research_project",
    "ResearchSubject.primary_disease_type": "ResearchSubject.primary_diagnosis_condition",
    "ResearchSubject.primary_disease_site": "ResearchSubject.primary_diagnosis_site",
    "ResearchSubject.Diagnosis.tumor_stage": "ResearchSubject.Diagnosis.stage",
    "ResearchSubject.Diagnosis.tumor_grade": "ResearchSubject.Diagnosis.grade",
    "ResearchSubject.Diagnosis.Treatment.type": "ResearchSubject.Diagnosis.Treatment.treatment_type",
    "ResearchSubject.Diagnosis.Treatment.outcome": "ResearchSubject.Diagnosis.Treatment.treatment_outcome",
}
