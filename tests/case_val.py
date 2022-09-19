from cdapython import Q

for i in ["+", "-", "/", "*"]:
    print(Q(f"days_to_birth >= 50 {i} 365").to_json())
