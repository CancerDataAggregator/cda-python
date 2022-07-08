from cdapython import Q

try:
    q = Q.query_job_status("5f41221a-c4cc-4dc1-8b4d-aa0748133398")
    print(q)
except Exception as e:
    print(e)
