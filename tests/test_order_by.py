from cdapython import Q

def test_order_by():
  q1 = Q('sex = "male"')
  q1 = q1.ORDER_BY("ethnicity")

  q1_json = q1.to_dict()
  print(q1.to_json())

  assert q1_json['node_type'] == 'ORDERBY'
  assert q1_json['l']['node_type'] == 'ORDERBYVALUES'


  q2 = q1.ORDER_BY("race:-1 sex:1")

  q2_json = q2.to_dict()
  print(q2.to_json())

  assert q2_json['l']['value'] == 'race DESC,sex ASC'
