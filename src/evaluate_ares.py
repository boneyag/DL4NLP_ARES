from bs4 import BeautifulSoup
from scipy.spatial.distance import cosine
import string
import re
import os
import numpy as np

from bert_helper import *
from wordnet_helper import *

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
    for tw in target_words:
        if tw in words:
            target_index.append(words.index(tw))
        else:
            target_index.append(-1)
            
    print(sentence)
    print(target_words)
    # print(target_index)
    # print(target_gold_keys)  
    
    test_data = {
        'sentence': sentence,
        'target_words': target_words,
        'target_index': target_index,
        'target_gold_keys': target_gold_keys
    }
    
    return test_data
    
def get_test_gold_key(target_gold_key, dir_name):
            
    with open('../data/eval_data/{0}/{0}.gold.key.txt'.format(dir_name)) as f:
        lines = f.readlines()
        
        for line in lines:
            target_sense = line.split(' ')
            if target_sense[0] == target_gold_key:
                return target_sense[1:][0].strip()
            
def find_candidate_embedding(target_word):
    all_synset_lex_ids = []
    candidate_embeddings = []
    for ss in wn.synsets(target_word):
        for lemma in ss.lemmas():
            all_synset_lex_ids.append(lemma.key())
            
    for root, dirs, files in os.walk('../data/embeddings'):
        for file in files:
            if offsetpos_to_lexid(file.split('.')[0]) in all_synset_lex_ids:
                candidate_embeddings.append(file)           
    
    return candidate_embeddings

def find_most_similar_embedding(candidate_embedding, target_embedding):
    max_sim = -1
    most_sim = ''
    for curr_embedding in candidate_embedding:
        with open('../data/embeddings/{}'.format(curr_embedding)) as f:
            temp_vec = np.loadtxt(f, skiprows=1)
            diff_sense = 1 - cosine(temp_vec, target_embedding)
            print(offsetpos_to_lexid(curr_embedding.split('.')[0]))
            if diff_sense > max_sim:
                max_sim = diff_sense
                most_sim = curr_embedding
                
    return most_sim.split('.')[0]
    
def main():
    model, tokenizer = load_bert()
    
    test_data = get_test_data('senseval2')
    
    # current_target = 'sound'
    for target_word in test_data['target_words']:
        # if target_word != current_target:
        #     continue
        
        target_word_index = test_data['target_words'].index(target_word)
        target_word_sent_pos = test_data['target_index'][test_data['target_words'].index(target_word)]
        print(target_word)
        
        # generate BERT vector for target_word
        tokenized, seg_ids = prepare_data(test_data['sentence'], tokenizer)
        bert_vec = get_feeaturs(tokenized, seg_ids, model, target_word_sent_pos).detach().cpu().numpy()
        
        # generate BERT vectors for all synset with synset.name == target_word
        candidate_embeddings = find_candidate_embedding(target_word)
        most_sim = find_most_similar_embedding(candidate_embeddings, bert_vec)
        
        if len(most_sim) > 0:
            print('Predicted sense:lex_id: ',offsetpos_to_lexid(most_sim))
            print('Gold sense:lex_id:', get_test_gold_key(test_data['target_gold_keys'][target_word_index], 'senseval2'))
        
    
    
    
    
if __name__ == '__main__':
    main()