from bs4 import BeautifulSoup
import os

from whoosh.filedb.filestore import FileStorage
from whoosh.fields import *

# from time import perf_counter, process_time


def add_root_tag():
    """
    To process with BeautifulSoup add root tags (<article></article>) 
    to enclose all doc tags in each file.
    """
    
    # change input_path based on output path of wikiextracter
    input_path = '../../WikipediaDump/output'
    output_path = '../data/wiki_dump'
    
 
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.startswith('wiki'):
                cur_dir = str(os.path.basename(os.path.join(root)))
                os.makedirs(os.path.join(output_path, cur_dir), exist_ok=True)
                with open(os.path.join(root, file), 'r') as in_file, open('{}/{}/{}'.format(output_path, cur_dir, file), 'w') as out_file:
                    out_file.write('<articles>\n')
                    for line in in_file.readlines():
                        out_file.write(line)
                    out_file.write('</articles>')
        
def create_index():
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
                file_content = file_content + item.string
                
            ix_writer.add_document(title=name, path=os.path.join(root,name), content=file_content)
                    
    ix_writer.commit()
                  

def main():
    
    if not os.listdir('../data/wiki_dump'):
        add_root_tag()
    

    if not os.listdir('../data/wiki_index'):
        create_index()
    

if __name__ == '__main__':
    main()
