from cdapython import Q

r = Q.bulk_download(limit=500)


r.to_csv("big.tsv", "\t")
