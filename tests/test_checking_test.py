from cdapython import Q


def checking_test():
    q1 = Q('''
    ResearchSubject.id IN [
        "4da7abaf-ac7a-41c0-8033-5780a398545c",
        "010df72d-63d9-11e8-bcf1-0a2705229b82"
        ]
    ''')
    r = q1.run(host="http://localhost:8080") 
    print(r)
    # subject2 = r[0]['ResearchSubject'][1]
    # for s2 in subject2['Specimen']:        
    #     if s2['specimen_type'] == 'sample':
    #         for k, v in s2.items():
    #             if isinstance(v,list):
    #                 if len(v) < 2:
    #                     print(k, v)
    #                 else:
    #                     if k == 'File':
    #                         print("-"*80)
    #                         print("File")
    #                         print("-"*80)
    #                         for f in v:
    #                             print(f['label'])
    #                     else:    
    #                         print ('{} has {} items'.format(k, len(v)))
    #             else:
    #                 print ('{} : {}'.format(k, v))

    #         print('_'*80)

checking_test()