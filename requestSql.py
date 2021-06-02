import requests

def runAPIQuery(querystring, limit=None)-> dict:
    cdaURL = 'https://cda.cda-dev.broadinstitute.org/api/v1/sql-query/v3'
    #Using a limit:
    if limit is not None:
        cdaURL = "{}?limit={}".format(cdaURL, str(limit))

    headers = {'accept' : 'application/json', 'Content-Type' : 'text/plain'}
    request = requests.post(cdaURL, headers = headers, data = querystring)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception ("Query failed code {}. {}".format(request.status_code,querystring))

def getQueryID(queryID ):
    cdaURL = f'https://cda.cda-dev.broadinstitute.org/api/v1/query/{queryID}'
    print(cdaURL)

    headers = {'accept' : 'application/json', 'Content-Type' : 'text/plain'}
    request = requests.get(cdaURL, headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception ("Query failed code {}".format(request.status_code))

querystring = ''' select * from gdc-bq-sample.cda_mvp.v3
where id in
(SELECT distinct p.id FROM gdc-bq-sample.cda_mvp.v3 AS p,
UNNEST(ResearchSubject) AS _ResearchSubject,
UNNEST(_ResearchSubject.Diagnosis) AS _Diagnosis
WHERE (((_ResearchSubject.associated_project = 'TCGA-BRCA')
AND (_Diagnosis.tumor_stage = 'stage ii'))
) )'''
query_id,searchSubject = runAPIQuery(querystring).values()
getQueryID(query_id)

