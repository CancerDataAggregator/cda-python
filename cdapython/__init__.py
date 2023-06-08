"""
cdapython is a library used to interact with the machine generated CDA Python Client and offers some
syntactic sugar to make it more pleasant to query the CDA.
"""

from typing import Any

from typeguard import install_import_hook
from typing_extensions import Literal

from cdapython.constant_variables import Constants
from cdapython.factories import (
    COUNT,
    DIAGNOSIS,
    DIAGNOSIS_COUNT,
    FILE,
    FILE_COUNT,
    MUTATIONS,
    MUTATIONS_COUNT,
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
)
from cdapython.factories.count import Count
from cdapython.factories.diagnosis import Diagnosis, DiagnosisCount
from cdapython.factories.file import File
from cdapython.factories.file_count import FileCount
from cdapython.factories.mutations import Mutations, MutationsCount
from cdapython.factories.q_factory import QFactory
from cdapython.factories.research_subject import (
    ResearchSubject,
    ResearchSubjectCount,
    ResearchSubjectFileCount,
    ResearchSubjectFiles,
)
from cdapython.factories.specimen import (
    Specimen,
    SpecimenCount,
    SpecimenFileCount,
    SpecimenFiles,
)
from cdapython.factories.subject import (
    Subject,
    SubjectCount,
    SubjectFileCount,
    SubjectFiles,
)
from cdapython.factories.treatment import Treatment, TreatmentCount
from cdapython.Q import Q
from cdapython.utils.utility import (
    columns,
    get_default_project_dataset,
    get_host_url,
    get_query_result,
    get_table_version,
    set_default_project_dataset,
    set_host_url,
    set_table_version,
    unique_terms,
)

install_import_hook("cdapython")
__version__: str = Constants.version()
__about__: str = f"Q {__version__}"

__all__ = [
    "__name__",
    "__version__",
    "__about__",
    "Constants",
    "Q",
    "columns",
    "get_default_project_dataset",
    "get_host_url",
    "get_query_result",
    "get_table_version",
    "set_default_project_dataset",
    "set_host_url",
    "set_table_version",
    "unique_terms",
    "Subject",
    "SubjectCount",
    "SubjectFileCount",
    "SubjectFiles",
    "Treatment",
    "TreatmentCount",
    "Specimen",
    "SpecimenCount",
    "SpecimenFileCount",
    "SpecimenFiles",
    "ResearchSubject",
    "ResearchSubjectCount",
    "ResearchSubjectFileCount",
    "ResearchSubjectFiles",
    "QFactory",
]
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
QFactory.add_factory(MUTATIONS, Mutations.Factory)
QFactory.add_factory(MUTATIONS_COUNT, MutationsCount.Factory)
