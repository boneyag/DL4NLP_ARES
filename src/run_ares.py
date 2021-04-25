from subprocess import run
from nltk.corpus import wordnet as wn
import subprocess
import os

from wiki_search import search_wiki_dump, window_search_wiki_dump
from bert_helper import *
from cluster import *
from ukb_helper import prepare_data_ukb, run_ukb
from wordnet_helper import *
from syntagnet_senses import get_collocated_senses
import time

def read_input_lemmas():
    with open('../data/input_lemmas.txt', 'r') as f:
        lines = f.readlines()
        
    return lines
    
def main():
    """
    Get wordnet synsets one by one. For each synset get the lexicalization as temp to find all synset with the same lixicalization.
    For example, if the current synset is spring.n.01 find all synsets with the lexicalization spring. Set the number of clusters 
    to the number of synsets for a given lexicalization. For each
    """
    # load bert and get vector representation of sentences
    model, tokenizer = load_bert()
    
    # read input lemmas and get iterable object
    input_lemmas = read_input_lemmas()
    
    processed_synsets = []
    
    for lemma in input_lemmas:
        print('\nCreating embedding for {}\n********************\n'.format(lemma))
        # i = 1
        for ss in wn.synsets(lemma.strip()):
            
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
            
            print('Search wiki')
            sent_file_name = search_wiki_dump(instance['lex'],)
            
            if os.stat('../data/temp/{}'.format(sent_file_name)).st_size == 0:
                continue
            
            df_sentences = read_data(sent_file_name)
            padded, attention_mask = prepare_data_bert(df_sentences[0], tokenizer)
            print("get bert vectors")
            features = get_features(padded, attention_mask, model)
            
            print("get clusters")
            labels = get_kmeans_clusters(features, k)
            # print(labels)
            df_sentences = df_sentences.assign(c=pd.Series(labels).values)
            
            print("write clusters")
            df_sentences.to_csv('../data/clusters/clusters.csv', index=False, header=False)
            
            print('Run UKB')
            prepare_data_ukb()
            run_ukb('temp_ukb_input.txt', 'temp_ukb_output.txt', 'ppr_w2w')
            
            similar_senses = assign_cluster_wordnet_sense('temp_ukb_output.txt', instance['lex'][0])
                
            print('Get collocated senses and containing sentences')
            
            
            # for each sense_offset find collocated senses in syntagnet
            for k, v in similar_senses.items():
                collocated_senses = get_collocated_senses(k)
                
                if len(collocated_senses) > 0:
                    for sense in collocated_senses:
                        window_search_wiki_dump(instance['lex'][0], sense[2])
                
                    print('Done searching for collocation sentences')    
                    with open('../data/temp/sent_cluster.txt', 'w') as fw, open('../data/temp/collocated_sents.txt', 'r') as fr:
                        lines = fr.readlines()
                        for line in lines:
                            fw.write(line)
                        # add lemma and gloss
                        fw.write(offsetpos_to_name_gloss(k) + '\n')

                        # add sentences in the same clusters
                        temp_sent_df = df_sentences[df_sentences.c.isin(v)]
                        for sent in temp_sent_df[0].tolist():
                            fw.write(sent + '\n')
                else:
                    print('No collocated senses')
                    with open('../data/temp/sent_cluster.txt', 'w') as fw:
                        # add lemma and gloss
                        fw.write(offsetpos_to_name_gloss(k) + '\n')

                        # add sentences in the same clusters
                        temp_sent_df = df_sentences[df_sentences.c.isin(v)]
                        for sent in temp_sent_df[0].tolist():
                            fw.write(sent + '\n')
                    
                
                # get BERT vectors for sense embeddings
                
                cluster_df = read_data('sent_cluster.txt')
            
                padded, attention_mask = prepare_data_bert(cluster_df[0], tokenizer)
                features = get_features(padded, attention_mask, model)    
                lex_id = offsetpos_to_lexid(k)
                sense_embeddings = get_sense_embedding(features)
                print(sense_embeddings.shape)
                with open('../data/embeddings/{}.txt'.format(k), 'w') as f:
                    f.write('%s \n' % lex_id)
                    for entry in sense_embeddings:
                        f.write('%d ' % entry)
            
                # remove older context sent file
                command = 'rm -f ../data/temp/collocated_sents.txt'
                subprocess.run(command, shell=True)

            # add processed senses to a list
            processed_synsets.append(ss.name())    
            
            # end time
            end_time = time.perf_counter()
            print('Time to process one sense: {}'.format(end_time-st_time))
            
            # For testing purposes. Don't want to run the entire WN synset.
            # i += 1
            # if i > 1:
            #     break
    
        
    

if __name__ == '__main__':
    main()