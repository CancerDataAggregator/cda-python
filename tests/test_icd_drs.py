from cdapython import Q

r1 = Q.sql(
    """
SELECT
*
FROM gdc-bq-sample.cda_mvp.v2, UNNEST(ResearchSubject) AS _ResearchSubject
WHERE (_ResearchSubject.primary_disease_type = 'Adenomas and Adenocarcinomas')
"""
)
