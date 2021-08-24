from cdapython import Q

pdc = Q('ResearchSubject.Specimen.identifier.system = "PDC"')
r = pdc.run(host="http://localhost:8080", async_call=True)
print(r)
