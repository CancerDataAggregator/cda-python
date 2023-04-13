import pytest

from cdapython import Q
from cdapython.exceptions.custom_exception import QSyntaxError

with pytest.raises(QSyntaxError):
    Q(
        """
      
      
      'has and leg' 
      from
      """
    )
