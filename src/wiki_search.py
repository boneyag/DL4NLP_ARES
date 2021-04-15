from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser

from bs4 import BeautifulSoup

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
    
    with open('../data/clusters/all_{}.txt'.format(lemmas[0]), 'w') as f:
    
        with wiki_ix.searcher() as ws:
            results = ws.search(my_query, limit=5)
            
            for result in results:
                soup = BeautifulSoup(open(result['path']), 'xml')
                result_set = soup.find_all('doc')
                
                for item in result_set:
                    if len(item.string.strip()) > 0:
                        content=item.string.strip()
                        sentences = content.split('.')
                        for sent in sentences:
                            for lemma in lemmas:
                                if lemma in sent:
                                    f.write(sent)