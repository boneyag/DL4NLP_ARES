from subprocess import run
from nltk.corpus import wordnet as wn

from wiki_search import search_wiki_dump
from bert_helper import *
from cluster import *
from ukb_helper import prepare_data_ukb, run_ukb
from wordnet_helper import assign_cluster_wordnet_sense
import time

def main():
    """
    Get wordnet synsets one by one. For each synset get the lexicalization as temp to find all synset with the same lixicalization.
    For example, if the current synset is spring.n.01 find all synsets with the lexicalization spring. Set the number of clusters 
    to the number of synsets for a given lexicalization. For each
    """
    # load bert and get vector representation of sentences
    model, tokenizer = load_bert()
    
    processed_synsets = []
    i = 1
    for ss in wn.all_synsets():
        
        # start time
        st_time = time.perf_counter()
        
        if ss.name() in processed_synsets:
            continue
        
        
        # get the lexicalization of synset, ex: spring.n.01 -> spring
        temp = ss.name().split('.')[0]
        
        # set number of clusters to number of synset/senses of temp
        k = len([s for s in wn.synsets(temp)])
                 
            
        gloss = ss.definition()
        lex = [l.name() for l in ss.lemmas()]
        instance = {'gloss': gloss,
                    'lex': lex}
        
        
        sent_file_name = search_wiki_dump(instance['lex'],)
        
        df_sentences = read_data(sent_file_name)
        padded, attention_mask = prepare_data_bert(df_sentences[0], tokenizer)
        print("get bert vectors")
        features = get_features(padded, attention_mask, model)
        
        print("get clusters")
        labels = get_kmeans_clusters(features, k)
        print(labels)
        df_sentences = df_sentences.assign(c=pd.Series(labels).values)
        
        print("write clusters")
        df_sentences.to_csv('../data/clusters/{}_clusters.csv'.format(instance['lex'][0]), index=False, header=False)
        
        print('Run UKB')
        prepare_data_ukb('{}_clusters.csv'.format(instance['lex'][0]))
        run_ukb('temp_ukb_input.txt', 'temp_ukb_output.txt', 'ppr_w2w')
        
        similar_senses = assign_cluster_wordnet_sense('temp_ukb_output.txt', instance['lex'][0])
            
        merge_clusters(instance['lex'][0], similar_senses)
        
        processed_synsets.append(ss.name())    
        
        # end time
        end_time = time.perf_counter()
        print('Time to process one sense: {}'.format(end_time-st_time))
        
        # For testing purposes. Don't want to run the entire WN synset.
        i += 1
        if i > 1:
            break
    
        
    

if __name__ == '__main__':
    main()