from bs4 import BeautifulSoup

def get_instances_eval_file(dirname, file_name):
    
    instances = []
    
    soup = BeautifulSoup(open('../data/eval_data/{}/{}'.format(dirname, file_name)), 'xml')
    result_set = soup.find_all('instance')
    
    for instance in result_set:
        instances.append(instance.get('lemma'))
        
    instances = list(set(instances))
    
    with open('../data/input_lemmas.txt', 'w') as f:
        for lemma in instances:
            f.write('%s\n' % lemma)
        
        

        