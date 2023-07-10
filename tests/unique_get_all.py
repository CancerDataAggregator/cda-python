from cdapython import unique_terms

all_entrez = unique_terms("Entrez_Gene_Id", page_size=100).get_all()
