from cdapython import Q

Q(
    "subject_id IN ?, ?",
    Q("sex = 'male'").SELECT("subject_id"),
    Q("sex = 'male'").SELECT("subject_id"),
).to_json()
