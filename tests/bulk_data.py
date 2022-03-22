from cdapython import Q


r = Q.bulk_download(host="http://localhost:8080",limit=500)

r.to_csv("big.tsv", "\t")
