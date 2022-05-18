import json

from cdapython import Q

querystring = """ select * from gdc-bq-sample.cda_mvp.v3
where id in
(SELECT distinct p.id FROM gdc-bq-sample.cda_mvp.v3 AS p,
UNNEST(ResearchSubject) AS _ResearchSubject,
UNNEST(_ResearchSubject.Diagnosis) AS _Diagnosis
WHERE (((_ResearchSubject.associated_project = 'TCGA-BRCA')
AND (_Diagnosis.tumor_stage = 'stage ii'))
) )"""

result = Q.sql(querystring)

for res in result:
    for su in res["ResearchSubject"]:
        with open("data.json", "a+") as f:
            f.write(json.dumps(su, indent=4) + "\n")
