from cdapython.utility import single_operator_parser

qc2 = single_operator_parser(
    'ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" < ResearchSubject.Diagnosis.tumor_stage = "Stage IV" '
)

print(qc2.run())
