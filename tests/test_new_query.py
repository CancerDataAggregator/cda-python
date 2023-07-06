from cdapython import Q

a = (
    Q(
        """
    primary_disease_type = 'Lung%' 
    AND sex = 'male' OR sex = '%U' 
    OR sex = 'female' AND 
    subject_id IN ['TCGA-A5-A0G2', 'TCGA-EO-A22U', 'TCGA-FI-A2D5'] 
    """
    )
    .SELECT("id,sex")
    .ORDER_BY("id")
    .to_json()
)

print(a)
