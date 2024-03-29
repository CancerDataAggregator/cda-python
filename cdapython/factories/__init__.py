from cdapython.factories.q_factory import QFactory

FILE: str = "File"
COUNT: str = "Count"
FILE_COUNT: str = f"{FILE}.{COUNT}"
SUBJECT: str = "Subject"
SUBJECT_FILE: str = f"{SUBJECT}.{FILE}"
SUBJECT_FILE_COUNT: str = f"{SUBJECT}.{FILE_COUNT}"
SUBJECT_COUNT: str = f"{SUBJECT}.{COUNT}"
RESEARCH_SUBJECT: str = "ResearchSubject"
RESEARCH_SUBJECT_FILE: str = f"{RESEARCH_SUBJECT}.{FILE}"
RESEARCH_SUBJECT_FILE_COUNT: str = f"{RESEARCH_SUBJECT}.{FILE_COUNT}"
RESEARCH_SUBJECT_COUNT: str = f"{RESEARCH_SUBJECT}.{COUNT}"
SPECIMEN: str = "Specimen"
SPECIMEN_FILE: str = f"{SPECIMEN}.{FILE}"
SPECIMEN_FILE_COUNT: str = f"{SPECIMEN}.{FILE_COUNT}"
SPECIMEN_COUNT: str = f"{SPECIMEN}.{COUNT}"
DIAGNOSIS: str = "Diagnosis"
DIAGNOSIS_COUNT: str = f"{DIAGNOSIS}.{COUNT}"
TREATMENT: str = "Treatment"
TREATMENT_COUNT: str = f"{TREATMENT}.{COUNT}"
MUTATIONS: str = "Mutations"
MUTATIONS_COUNT: str = f"{MUTATIONS}.{COUNT}"


__all__ = [
    "QFactory",
    "FILE",
    "COUNT",
    "FILE_COUNT",
    "SUBJECT",
    "SUBJECT_FILE",
    "SUBJECT_FILE_COUNT",
]
