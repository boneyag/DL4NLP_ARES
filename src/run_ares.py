from subprocess import run
from nltk.corpus import wordnet as wn
import subprocess
import os
import string
import csv

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
    
def get_word_position_in_sent(sent, lemma):
    words = sent.split(' ')
    if lemma in words:
        return words.index(lemma)
    else:
        return -1
    
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
        print('\nCreating embedding for {}\n'.format(lemma))
        # i = 1
        for ss in wn.synsets(lemma.strip()):
            
            # start time
            st_time = time.perf_counter()
            
            if ss.name() in processed_synsets:
                continue
            
            
            # get the lexicalization of synset, ex: spring.n.01 -> spring
            temp = ss.name().split('.')[0]
            
            # set number of clusters to number of synset/senses of temp
            num_clusters = len([s for s in wn.synsets(temp)])
                    
                
            gloss = ss.definition()
            lex = [l.name() for l in ss.lemmas()]
            instance = {'gloss': gloss,
                        'lex': lex}
            
            print('Search wiki')
            sent_file_name = search_wiki_dump(instance['lex'],)
            
            # if no sentences were found go to the next lemmas
            if os.stat('../data/temp/{}'.format(sent_file_name)).st_size == 0:
                continue
            
            token_vectors = []
            sent_list = []
            print('Get bert vectors')
            
            with open('../data/temp/{}'.format(sent_file_name), 'r') as f:
                lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    line = line.translate(str.maketrans('', '', string.punctuation))
                    
                    word_pos = get_word_position_in_sent(line, instance['lex'][0])
                    
                    if word_pos > -1:
                        sent_list.append(line)
                    
                        tokenized, seg_ids = prepare_data(line, tokenizer)
                        token_vectors.append(get_feeaturs(tokenized, seg_ids, model, word_pos).detach().cpu().numpy())
            
            if len(token_vectors) < 1:
                break
            
            print("get clusters")
            labels = get_kmeans_clusters(token_vectors, num_clusters)
            
            print("write clusters")
            with open('../data/clusters/clusters.csv', 'w') as cf:
                cl_writer = csv.writer(cf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                cl_writer.writerows(zip(sent_list, labels))

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
                            fw.write(line+'\n')
                        # add lemma and gloss
                        fw.write(offsetpos_to_name_gloss(k) + '\n')

                        # add sentences in the same clusters
                        with open('../data/clusters/clusters.csv', 'r') as cf:
                            cf_reader = csv.reader(cf)
                            
                            for row in cf_reader:
                                if row[1] in v:
                                    fw.write(row[0]+'\n')
                else:
                    print('No collocated senses')
                    with open('../data/temp/sent_cluster.txt', 'w') as fw:
                        # add lemma and gloss
                        fw.write(offsetpos_to_name_gloss(k) + '\n')

                        # add sentences in the same clusters
                        with open('../data/clusters/clusters.csv', 'r') as cf:
                            cf_reader = csv.reader(cf)
                            
                            for row in cf_reader:
                                if row[1] in v:
                                    fw.write(row[0]+'\n')
                    
                
                # get BERT vectors for sense embeddings
            
                token_vectors = []
                print('Get bert vectors')
                with open('../data/temp/sent_cluster.txt', 'r') as f:
                    lines = f.readlines()
                    
                    for line in lines:
                        line = line.strip()
                        line = line.translate(str.maketrans('', '', string.punctuation))
                        
                        word_pos = get_word_position_in_sent(line, instance['lex'][0])
                        
                        if word_pos > -1:
                            sent_list.append(line)
                        
                            tokenized, seg_ids = prepare_data(line, tokenizer)
                            token_vectors.append(get_feeaturs(tokenized, seg_ids, model, word_pos).detach().cpu().numpy())    
                        
                lex_id = offsetpos_to_lexid(k)
                sense_embeddings = get_sense_embedding(token_vectors)
                print(sense_embeddings.shape)
                with open('../data/embeddings/{}.txt'.format(k), 'w') as f:
                    f.write('%s \n' % lex_id)
                    for entry in sense_embeddings:
                        f.write('%f ' % entry)
            
                # remove older context sent file
                command = 'rm -f ../data/temp/collocated_sents.txt'
                subprocess.run(command, shell=True)

            # add processed senses to a list
            processed_synsets.append(ss.name())    
            
            # end time
            end_time = time.perf_counter()
            print('Time to process one sense: {}'.format(end_time-st_time))
            
            break
            # For testing purposes. Don't want to run the entire WN synset.
            # i += 1
            # if i > 1:
            #     break
    
        
    

if __name__ == '__main__':
    main()