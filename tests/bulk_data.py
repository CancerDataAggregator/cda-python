from cdapython import Q


r = Q.bulk_download(host="http://localhost:8080")
print(len(r))
# for count, value in enumerate(Q.bulk_download(host="http://localhost:8080").stream()):
#     print(
#         count,
#     )


# print(sys.getsizeof(q))
#
# box = q[::-1]
#
# print(len(box))
#
# while q.has_next_page:
#     print(q[0])
