# query = ('ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" OR  ResearchSubject.Diagnosis.tumor_stage = "Stage IV" ')
# filterValues = ["AND","OR","SUBQUERY","NOT"]
# number = list(filter((lambda x: str(x).find(query) != -1),filterValuest))
# print(number)







import re
query = ('ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" OR  ResearchSubject.Diagnosis.tumor_stage = "Stage IV" AND ResearchSubject.Diagnosis.tumor_stage = "Stage IV"')




def SqlTermFilter(query="") -> list[dict]:
    """
    This function is used to filter Key SQL Terms pass a query String as a parameter 
    """
    strReturn = []
    filterValues = ["AND","OR","SUBQUERY","NOT"]
    token = ''
    print(token.find(" "))


tes = SqlTermFilter(query)

# for i in tes:
#     print(i)

    



# urrentStrInLoop = queryWords.upper()
#         for values in filterValues:
#             if(currentStrInLoop in filterValues):
#                 if(currentStrInLoop == values):
#                     print(currentStrInLoop)
#                     print(values,values in currentStrInLoop,currentStrInLoop)
#                     strReturn.append({values :re.split(fr"\b{values.lower()}|{values.upper()}",query)})




