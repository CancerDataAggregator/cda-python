"""
cdapython is a library used to interact with the machine generated CDA Python Client and offers some syntactic sugar to make it more pleasant to query the CDA.
"""
from __future__ import print_function
from typing import Any, Dict
from typing_extensions import Literal
from cdapython._get_unnest_clause import _get_unnest_clause
from cdapython.constant_variables import Constants
from cdapython.Q import Q
from cdapython.factories.count import Count
from rich import print
from cdapython.utils.utility import columns, query, unique_terms

from cdapython.factories import (
    COUNT,
    DIAGNOSIS,
    DIAGNOSIS_COUNT,
    FILE,
    FILE_COUNT,
    RESEARCH_SUBJECT,
    RESEARCH_SUBJECT_COUNT,
    RESEARCH_SUBJECT_FILE,
    RESEARCH_SUBJECT_FILE_COUNT,
    SPECIMEN,
    SPECIMEN_COUNT,
    SPECIMEN_FILE,
    SPECIMEN_FILE_COUNT,
    SUBJECT,
    SUBJECT_COUNT,
    SUBJECT_FILE,
    SUBJECT_FILE_COUNT,
    TREATMENT,
    TREATMENT_COUNT,
    QFactory,
)
from cdapython.factories.q_factory import QFactory
from cdapython.factories.subject import (
    Subject,
    SubjectCount,
    SubjectFiles,
    SubjectFileCount,
)

from cdapython.factories.research_subject import (
    ResearchSubject,
    ResearchSubjectCount,
    ResearchSubjectFiles,
    ResearchSubjectFileCount,
)

from cdapython.factories.specimen import (
    Specimen,
    SpecimenCount,
    SpecimenFiles,
    SpecimenFileCount,
)

from cdapython.factories.diagnosis import Diagnosis, DiagnosisCount

from cdapython.factories.treatment import Treatment, TreatmentCount

from cdapython.factories.file import File
from cdapython.factories.file_count import FileCount

__name__: Literal["cdapython"] = "cdapython"
__version__: str = Constants._VERSION
__about__: str = f"Q {__version__}"


try:
    # python2
    import __builtin__
except ImportError:
    # python3
    import builtins as __builtin__


def console_print(*args: Any, **kwargs: Any) -> None:
    from rich.console import Console

    console: Console = Console()
    console.print(*args, **kwargs)


__builtin__.print = console_print


def __repr__() -> str:
    return __version__


QFactory.add_factory(FILE, File.Factory)
QFactory.add_factory(FILE_COUNT, FileCount.Factory)
QFactory.add_factory(COUNT, Count.Factory)
QFactory.add_factory(SUBJECT, Subject.Factory)
QFactory.add_factory(SUBJECT_FILE, SubjectFiles.Factory)
QFactory.add_factory(SUBJECT_COUNT, SubjectCount.Factory)
QFactory.add_factory(SUBJECT_FILE_COUNT, SubjectFileCount.Factory)
QFactory.add_factory(RESEARCH_SUBJECT, ResearchSubject.Factory)
QFactory.add_factory(RESEARCH_SUBJECT_FILE, ResearchSubjectFiles.Factory)
QFactory.add_factory(RESEARCH_SUBJECT_COUNT, ResearchSubjectCount.Factory)
QFactory.add_factory(RESEARCH_SUBJECT_FILE_COUNT, ResearchSubjectFileCount.Factory)
QFactory.add_factory(SPECIMEN, Specimen.Factory)
QFactory.add_factory(SPECIMEN_FILE, SpecimenFiles.Factory)
QFactory.add_factory(SPECIMEN_COUNT, SpecimenCount.Factory)
QFactory.add_factory(SPECIMEN_FILE_COUNT, SpecimenFileCount.Factory)
QFactory.add_factory(DIAGNOSIS, Diagnosis.Factory)
QFactory.add_factory(DIAGNOSIS_COUNT, DiagnosisCount.Factory)
QFactory.add_factory(TREATMENT, Treatment.Factory)
QFactory.add_factory(TREATMENT_COUNT, TreatmentCount.Factory)
