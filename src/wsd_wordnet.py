from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
import re
import csv

def wordnet_synset_from_pos_offset(pos, offset):
    # print(wn.synset_from_pos_and_offset(pos, offset))
    return wn.synset_from_pos_and_offset(pos, offset)
    
def wordnet_trial():
    
    for ss in wn.synsets('spring'):
        print(ss, ss.definition())
        print(ss.lemmas())
        print(ss.pos())
        # print(ss.examples())

def wsd_with_lesk():

    print(lesk('I went fishing for some sea bass'.split(), 'bass', 'n'))
    print(lesk('The bass line of the song is too weak'.split(), 'bass', 's'))
    print(lesk('Avishai Cohen is an Israeli jazz musician. He plays double bass and is also a composer'.split(), 'bass', pos='n'))

def main():

    cluster_senses = []
    extracted_synTag = []
    
    with open('../data/glass_ukb_output2w2w.txt') as f:
        lines = f.readlines()
        for line in lines:
            if line.split()[0] == '!!':
                continue
            elif re.match(r'^ctx_.+', line):
                wordnet_synset_offset = line.split()[2]
                offset_pos = wordnet_synset_offset.split('-')
                offset = int(offset_pos[0])
                pos = offset_pos[1]
                lemma = line.split()[4]
                # print('{}-{}'.format(offset, pos))
                if lemma == 'glass':
                    offset_str = str(offset)
                    if len(offset_str)<8:
                        offset_str = offset_str.zfill(8)
                    print('{}-{}'.format(offset_str, pos))
                    cluster_senses.append(offset_str+pos) #Creating the senses offset+pos list for our lemma


                    print(wordnet_synset_from_pos_offset(pos, offset).definition())
        

    #extracting the collocated pairs
    with open('../data/SyntagNet/SYNTAGNET.txt') as synTag:
        entries = synTag.readlines()

        for i in range(len(cluster_senses)):
            for e in entries:
                if e.split()[0] == '#':
                    continue
                elif e.split()[0] == cluster_senses[i]:
                    e = e.split()
                    extracted_synTag.append(e)
                elif e.split()[1] == cluster_senses[i]:
                    e = e.split()
                    extracted_synTag.append(e)

    print(extracted_synTag)

    #writing the colloacted pairs in a CSV file
    extracted_fields = ['code1', 'code2', 'w1', 'pos1', 'w2', 'pos2']
    with open('../data/synTag_extracts.csv', 'w') as w:
        write = csv.writer(w)
        write.writerows(extracted_synTag)
    

    
    

    
if __name__ == '__main__':
    main()