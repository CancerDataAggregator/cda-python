from cdapython import Q
from cdapython.Result import Result
import sys


q: Result = Q.bulk_download(limit=200, host="http://localhost:8080")

print(sys.getsizeof(q))

box = q[::-1]

print(len(box))

while q.has_next_page:
    print(q[0])
