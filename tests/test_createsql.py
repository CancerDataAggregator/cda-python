import pytest
from cdapython import Q


def test_sql_actions():
    with pytest.raises(Exception) as excinfo:
        Q.sql(
            """
            CREATE TABLE test (id int) 
        """
        )

        Q.sql(
            """
            DROP TABLE test (id int) 
        """
        )

        Q.sql(
            """
            DELETE TABLE test (id int) 
        """
        )
    assert str(excinfo.value) == "Those actions are not available in Q.sql"
