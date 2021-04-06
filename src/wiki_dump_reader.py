from bs4 import BeautifulSoup
import os

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
        
    
def clean_wiki_dump():
    """
    Not going to use right now.
    """
    
    with open('../data/wiki_text.txt', 'w') as wiki_f:
        with open('../../WikipediaDump/output/AA/wiki_00') as fp:
            soup = BeautifulSoup(fp, 'xml') 
            all_text = soup.find_all('doc')
            print(len(all_text))
            for text in all_text:
                wiki_f.write(text.string)
        
def main():
    # call only if wiki_data is empty
    if not os.listdir('../data/wiki_dump'):
        add_root_tag()
    
    # clean_wiki_dump()
    
if __name__ == '__main__':
    main()
