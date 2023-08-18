

from cdapython import Q,unique_terms,columns
import requests, json
from deepdiff import DeepDiff
from datetime import datetime



postgres_url="https://cancerdata.ah-cda6.bee.envs-terra.bio/api/v1/"
postgres_params={'dryRun':'false','includeCount':'false','offset':0,'limit':100}
headers={'accept':'application/json','Content-Type': 'application/json'}

         
def get_postgres_results(json_query, endpoint):
    return requests.post(postgres_url + endpoint, params=postgres_params, headers=headers, json=json_query)

def do_comparison(qquery, failures_file, endpoint = 'boolean-query'):
    has_error = False
    
    bq_response_obj = qquery.run(verbose = False)
    if (bq_response_obj is None):
        has_error = True

    pg_response = get_postgres_results(qquery.to_dict(), endpoint)
    if (not pg_response.ok):
        has_error = True
        
    if (not has_error):
        bq_response = bq_response_obj._api_response
        bq_count = bq_response.total_row_count
        bq_sql = bq_response.query_sql
        bq_results_json = bq_response.result

        pg_sql = pg_response.json()['query_sql']
        pg_results_json = pg_response.json()['result']

        diffs = DeepDiff(bq_results_json, pg_results_json,  ignore_order=True)

        if (len(diffs) > 0):
            print("Failure")
            failures_file.write(qquery.to_json())
            failures_file.write(str(diffs))
            failures_file.write("\n------------------------------------------------------\n")
            # print(bq_sql)
            # print(pg_sql)
        else:
            print("Success!!!")


def main():
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    failures_file = open("failures" + current_time + ".txt", "w")
    do_comparison(Q('primary_diagnosis_site = "brain"').SELECT("subject_id,ethnicity").ORDER_BY("subject_id"), failures_file = failures_file)
    # do_comparison(Q( "symbol LIKE 'TP53%'"), failures_file = failures_file, 'researchsubjects')
    do_comparison(Q('primary_diagnosis_site = "brain" AND subject_id LIKE "CPTAC%"').SELECT("subject_id").ORDER_BY("subject_id:-1"), failures_file = failures_file)
    do_comparison(Q("primary_disease_type = 'Lung%'").SELECT("specimen_id,sex").ORDER_BY("specimen_id"), failures_file = failures_file)
    do_comparison(Q('(stage = "IIA" OR stage = "IIB") AND primary_diagnosis_site = "Lung"').ORDER_BY("subject_id"), failures_file = failures_file)

    failures_file.close()

if __name__ == '__main__':
    main()