from cdapython import Q


def checking_test():
    q1 = Q('ResearchSubject.id IN ["c5421e34-e5c7-4ba5-aed9-146a5575fd8d"]')
    r = q1.run(limit=2,host="http://localhost:8080") 
    print(r)
    subject2 = r[0]['ResearchSubject'][1]
    for s2 in subject2['Specimen']:        
        if s2['specimen_type'] == 'sample':
            for k, v in s2.items():
                if isinstance(v,list):
                    if len(v) < 2:
                        print(k, v)
                    else:
                        if k == 'File':
                            print("-"*80)
                            print("File")
                            print("-"*80)
                            for f in v:
                                print(f['label'])
                        else:    
                            print ('{} has {} items'.format(k, len(v)))
                else:
                    print ('{} : {}'.format(k, v))

            print('_'*80)

checking_test()