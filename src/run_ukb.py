import csv
import string

import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
eng_stopwords = stopwords.words('english')

def prepare_data():
    
    lines = []
    with open('../data/sample_sentences_clusters_glass.csv', 'r') as f:
        csv_reader =csv.reader(f, delimiter=',')
        for row in csv_reader:
            sent = row[0].translate(str.maketrans(' ', ' ', string.punctuation))
            tokens = sent.lower().split()
            
            tokens = [token for token in tokens if token not in eng_stopwords]
     
            lemmatized_tokens = []
            i = 1
            for token, pos in pos_tag(tokens):
                lemmatized_tokens.append('{}#{}#w{}#1'.format(lemmatizer.lemmatize(token, get_wordnet_pos(pos)), get_wordnet_type(pos), i))
                i += 1
            lines.append(lemmatized_tokens)
            
    print(lines)
    
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
    
def main():
    prepare_data()
    
if __name__ == '__main__':
    main()