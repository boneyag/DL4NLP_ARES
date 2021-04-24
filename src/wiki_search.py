from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser
from bs4 import BeautifulSoup
import re
from nltk.tokenize import sent_tokenize


def search_wiki_dump(lemmas):
    """
    Search sentences with input lemmas and write sentences to a file.
    """
    wiki_storage = FileStorage('../data/wiki_index')
    wiki_ix = wiki_storage.open_index(indexname='wiki')
    
    wiki_qparser = QueryParser('content', schema=wiki_ix.schema)
    
    # form a query string input from lemmas
    input = ''
    i = 0
    for lemma in lemmas:
        if i == 0:
            input += lemma
        else:
            input += ' OR ' + lemma 
        i +=1 
        
    my_query = wiki_qparser.parse(u"{}".format(input))
    
    
    # with open('../data/clusters/{}_all.txt'.format(lemmas[0]), 'w') as f:
    
    sentences = []
    with wiki_ix.searcher() as ws:
        results = ws.search(my_query, limit=3)
        
        print('done indexing')
        with open('../data/temp/all_sentences.txt', 'w') as f:
            for result in results:
                # print(result['path'])
                soup = BeautifulSoup(open(result['path']), 'xml')
                result_set = soup.find_all('doc')
                
                for item in result_set:
                    if len(item.string) > 0:
                        content = item.string
                        sentences = sent_tokenize(content)
                        for sent in sentences:
                            # print(sent)
                            for lemma in lemmas:
                                if re.search(rf'\b{lemma}\b', sent, re.IGNORECASE):
                                    f.write(sent + '\n')
                                       
    
    return 'all_sentences.txt'

def window_search_wiki_dump(input1, input2):
    """
    Search sentences with input lemmas and write sentences to a file.
    """
    wiki_storage = FileStorage('../data/wiki_index')
    wiki_ix = wiki_storage.open_index(indexname='wiki')
    
    wiki_qparser = QueryParser('content', schema=wiki_ix.schema)
    
    # form a query string input from lemmas
    input = input1 + ' AND ' + input2
        
    my_query = wiki_qparser.parse(u"{}".format(input))
    
    
    # with open('../data/clusters/{}_all.txt'.format(input), 'w') as f:
    
    with wiki_ix.searcher() as ws:
        results = ws.search(my_query, limit=3)
        
        with open('../data/clusters/context_all.txt', 'a') as f:
            for result in results:
                # print(result['path'])
                soup = BeautifulSoup(open(result['path']), 'xml')
                result_set = soup.find_all('doc')
                
                for item in result_set:
                    if len(item.string) > 0:
                        content = item.string
                        sentences = sent_tokenize(content)
                        for sent in sentences:
                            if re.search(rf'\b{input1}\W+(?:\w+\W+){{0,1}}?{input2}\b', sent) or re.search(rf'\b{input2}\W+(?:\w+\W+){{0,1}}?{input1}\b', sent):
                                f.write(sent + '\n')
    # end = time.perf_counter()
    # print('Time to search and write:{:.2f}'.format(end-start))                               
    return 'context_all.txt'