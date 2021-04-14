from bs4 import BeautifulSoup
import os

from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.filedb.filestore import FileStorage
from whoosh.fields import *
from whoosh.qparser import QueryParser

# from time import perf_counter, process_time


def add_root_tag():
    """
    To process with BeautifulSoup add root tags (<article></article>) 
    to enclose all doc tags in each file.
    """
    print('adding root tags to each file')
    
    input_path = '../../WikipediaDump/output'
    output_path = '../data/wiki_dump'
    
 
    
    i = 1
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.startswith('wiki'):
                cur_dir = str(os.path.basename(os.path.join(root)))
                # print(cur_dir)
                # print(os.path.join(output_path, cur_dir, file))
                os.makedirs(os.path.join(output_path, cur_dir), exist_ok=True)
                with open(os.path.join(root, file), 'r') as in_file, open('{}/{}/{}'.format(output_path, cur_dir, file), 'w') as out_file:
                    out_file.write('<articles>\n')
                    for line in in_file.readlines():
                        out_file.write(line)
                    out_file.write('</articles>')
        
def index_wiki_dump():
    """
    Index wiki files for faster content search.
    """
    
    # create a schema
    wiki_schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    
    # create index
    if not os.path.exists('../data/wiki_index'):
        os.makedirs('../data/wiki_index', exist_ok=True)
    
    
    wiki_storage = FileStorage('../data/wiki_index')
    wiki_ix = wiki_storage.create_index(wiki_schema, indexname='wiki')
    
    ix_writer = wiki_ix.writer(limitmb=256, procs=4, multisegment=True)
     
    # index documents
    for root, dirs, files in os.walk('../data/wiki_dump'):
        for name in files:
            soup = BeautifulSoup(open(os.path.join(root, name)), 'xml') 
            all_text = soup.find_all('doc')
            file_content = ' '
            for item in all_text:
                # print(item['title'])
                # print(len(item.string))
                file_content = file_content + item.string
                
            ix_writer.add_document(title=name, path=os.path.join(root,name), content=file_content)
                    
    ix_writer.commit()
    
    
def search_wiki_dump(input):
    """
    This is only a test. A proper search will be done later once integrated with WSD results.
    """
    wiki_storage = FileStorage('../data/wiki_index')
    wiki_ix = wiki_storage.open_index(indexname='wiki')
    
    wiki_qparser = QueryParser('content', schema=wiki_ix.schema)
    
    my_query = wiki_qparser.parse(u"{}".format(input))
    
    # t_start = process_time()
    
    with open('../data/all_{}.txt'.format(input), 'w') as f:
    
        with wiki_ix.searcher() as ws:
            results = ws.search(my_query, limit=5)
            
            for result in results:
                print(result['path'])
                soup = BeautifulSoup(open(result['path']), 'xml')
                result_set = soup.find_all('doc')
                
                for item in result_set:
                    # print(item['title'])
                    # print(len(item.string))
                    if len(item.string.strip()) > 0:
                        content=item.string.strip()
                        sentences = content.split('.')
                        for sent in sentences:
                            if input in sent:
                                # print(sent)
                                f.write(sent)
                            
    # t_end = process_time()
    
    # print('Time taken {:.2f}'.format(t_end-t_start)) 
    
def search_without_index():
    
    # t_start = process_time()
    
    for root, dir, files in os.walk('../data/wiki_dump'):
        for name in files:         
            soup = BeautifulSoup(open(os.path.join(root, name)), 'xml') 
            all_text = soup.find_all('doc')
            for item in all_text:
                # print(item['title'])
                # print(len(item.string))
                if len(item.string.strip()) > 0:
                    content=item.string.strip()
                    sentences = content.split('.')
                    for sent in sentences:
                        if 'glass' in sent:
                            print(sent)
    # t_end = process_time()
    
    # print('Time taken {:.2f}'.format(t_end-t_start))   
                 

def main():
    # call only if wiki_data is empty
    if not os.listdir('../data/wiki_dump'):
        add_root_tag()
    

    if not os.listdir('../data/wiki_index'):
        index_wiki_dump()
    
    search_wiki_dump('glass')
    
    # this is too slow ~980 seconds for a search. Will taka over 3 years to search for WodNet synsets
    # search_without_index()

    
if __name__ == '__main__':
    main()
