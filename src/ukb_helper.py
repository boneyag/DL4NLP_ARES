import csv
import string
import subprocess
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from collections import Counter

lemmatizer = WordNetLemmatizer()
eng_stopwords = stopwords.words('english')

def run_ukb(input, output, algorithm):
    command = './ukb/src/ukb_wsd --{} -K ukb/scripts/wn30g.bin -D ukb/scripts/wn30_dict.txt ../data/temp/{} > ../data/temp/{}'.format(algorithm, input, output)
    subprocess.run(command, shell=True)
    
def prepare_data_ukb():
    
    cluster_bow = {}
    
    with open('../data/clusters/clusters.csv', 'r') as f:
        csv_reader =csv.reader(f, delimiter=',')
        for row in csv_reader:
            
            sent = row[0].translate(str.maketrans(' ', ' ', string.punctuation))
            tokens = sent.lower().split()
            
            tokens = [token for token in tokens if token not in eng_stopwords]
        
            lemmatized_tokens = []
            
            for token, pos in pos_tag(tokens):
                # lemmatized_tokens.append('{}#{}#w{}#1'.format(lemmatizer.lemmatize(token, get_wordnet_pos(pos)), get_wordnet_type(pos), i))
                lemmatized_tokens.append(lemmatizer.lemmatize(token, get_wordnet_pos(pos)))
                
                
            # create a dict entry for each cluster/class then add words
            class_id = row[1]
            if class_id not in cluster_bow.keys():
                cluster_bow[class_id] = lemmatized_tokens
            elif class_id in cluster_bow.keys():
                cluster_bow[class_id].extend(lemmatized_tokens)
        
        # create a bag of word for each cluster with top 5 words
        for k, v in cluster_bow.items():
            word_counter = Counter(v)
            cluster_bow[k] = [tup[0] for tup in word_counter.most_common(5)]
            temp = []
            i = 1
            for word, pos in pos_tag(cluster_bow[k]):
                temp.append('{}#{}#w{}#1'.format(word, get_wordnet_type(pos), i))
                i += 1
            cluster_bow[k] = temp
            
        # print(cluster_bow)
        with open('../data/temp/temp_ukb_input.txt', 'w') as f:    
            
            for key in cluster_bow.keys():
                f.write('ctx_{}\n'.format(key))
                for item in cluster_bow[key]:
                    f.write('%s ' % item)
                f.write('\n')
            
    
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    if treebank_tag.startswith('N'):
        return wordnet.NOUN
    if treebank_tag.startswith('V'):
        return wordnet.VERB
    if treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
       
def get_wordnet_type(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'
    if treebank_tag.startswith('N'):
        return 'n'
    if treebank_tag.startswith('V'):
        return 'v'
    if treebank_tag.startswith('R'):
        return 'r'
    else:
        return 'n'