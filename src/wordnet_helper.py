from nltk.corpus import wordnet as wn
import re

def assign_cluster_wordnet_sense(file_name, input_lemma):
    """
    After UKB assign WN senses to top 5 words in each cluster find cluasters with the same sense.
    Creates a dictionary of where sense offset as the key and cluster numbers as values. 
    """
    
    similar_senses = {}
    
    with open('../data/clusters/{}'.format(file_name)) as f:
        lines = f.readlines()
        for line in lines:
            if line.split()[0] == '!!':
                continue
            elif re.match(r'^ctx_.+', line):
                line_content = line.split()
                wordnet_synset_offset = line_content[2]
                offset_pos = wordnet_synset_offset.split('-')
                offset = int(offset_pos[0])
                pos = offset_pos[1]
                lemma = line_content[4]
                # print('{}-{}'.format(offset, pos))
                if lemma == input_lemma:
                    # print('{}-{}'.format(offset, pos))
                    # print(wn.synset_from_pos_and_offset(pos, offset).definition())
                    synset = wn.synset_from_pos_and_offset(pos, offset)
                    if wordnet_synset_offset in similar_senses.keys():
                        similar_senses[wordnet_synset_offset].extend(line_content[0].split('_')[1])
                    else:
                        similar_senses[wordnet_synset_offset] = [line_content[0].split('_')[1]]

    return similar_senses                 