from bs4 import BeautifulSoup
import string
import re

from bert_helper import *

def get_test_data(dir_name):
    sentence = ''
    target_index = []
    target_words = []
    target_gold_keys = []
    with open('../data/eval_data/{0}/{0}.data.xml'.format(dir_name)) as ef:
        soup = BeautifulSoup(ef, 'lxml')
        sentences = soup.find_all('sentence',{'id':'d000.s003'})
        
        for sent in sentences:
            for child in sent.children:
                sentence += child.string.strip()+ ' '
                if child.name == 'instance':
                    target_words.append(child.string.strip())
                    target_gold_keys.extend(child.get_attribute_list('id'))
            break   
          
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    
    sentence = re.sub(r'\b\s{2,}\b', ' ', sentence)
    
    sentence = sentence.strip()
    
    words = sentence.split(' ')
    for word in words:
        if word in target_words:
            target_index.append(words.index(word))
        else:
            target_index.append(-1)
            
    # print(sentence)
    # print(target_words)
    # print(target_index)
    # print(target_gold_keys)  
    
    test_data = {
        'sentence': sentence,
        'target_words': target_words,
        'target_index': target_index,
        'target_gold_keys': target_gold_keys
    }
    
    return test_data
    
def get_test_gold_key(target_gold_keys, dir_name):
            
    with open('../data/eval_data/{0}/{0}.gold.key.txt'.format(dir_name)) as f:
        lines = f.readlines()
        
        for line in lines:
            target_sense = line.split(' ')
            if target_sense[0] in target_gold_keys:
                print(target_sense[1:])
            
            
    
    
    
def main():
    model, tokenizer = load_bert()
    
    test_data = get_test_data('senseval2')
    
    for target_word in test_data['target_words']:
        target_word_index = test_data['target_index'][test_data['target_words'].index(target_word)]
        print(target_word, ':', target_word_index)
        
        # generate BERT vector for target_word
        tokenized, seg_ids = prepare_data(test_data['sentence'], tokenizer)
        bert_vec = get_feeaturs(tokenized, seg_ids, model, target_word_index).detach().cpu().numpy()
        print(bert_vec.shape)
        
        # generate BERT vectors for all synset with synset.name == target_word
        
        break
    
    
    # get_test_gold_key(test_data['target_gold_keys'], 'senseval2')
    
    
if __name__ == '__main__':
    main()