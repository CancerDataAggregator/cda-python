from cdapython import Q

Q.sql("""
    CREATE TABLE test (id int) 
""")

Q.sql("""
    DROP TABLE test (id int) 
""")

Q.sql("""
    DELETE TABLE test (id int) 
""")
