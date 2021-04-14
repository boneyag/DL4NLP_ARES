from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
import re

def wordnet_synset_from_pos_offset(pos, offset):
    # print(wn.synset_from_pos_and_offset(pos, offset))
    return wn.synset_from_pos_and_offset(pos, offset)
    
def wordnet_trial():
    
    # how to get lexicalization(or lemmas) for a given sense
    for ss in wn.synsets('spring'):
        print(ss, ss.definition())
        # print(ss.lemmas())
        for lex in ss.lemmas():
            print('{}.{}'.format(lex.synset(), lex.name()))
        # print(ss.pos())
        # print(ss.examples())
    
    # how to get lexicalizations (or lemmas) for all senses in WordNet
    # the loop stops after 10 iterations for simiplicity
    # change the condition if you need to print more
    # i=1
    # for ss in wn.all_synsets():
    #     print(ss, ss.definition())
    #     print(ss.lemmas())
    #     i += 1
        
    #     if i > 10:
    #         break
    
def wsd_with_lesk():

    print(lesk('I went fishing for some sea bass'.split(), 'bass', 'n'))
    print(lesk('The bass line of the song is too weak'.split(), 'bass', 's'))
    print(lesk('Avishai Cohen is an Israeli jazz musician. He plays double bass and is also a composer'.split(), 'bass', pos='n'))

def main():
    wordnet_trial()

    # wsd_with_lesk()
    
    # synset_dict = {}
    
    # with open('../data/glass_ukb_output2w2w.txt') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         if line.split()[0] == '!!':
    #             continue
    #         elif re.match(r'^ctx_.+', line):
    #             wordnet_synset_offset = line.split()[2]
    #             offset_pos = wordnet_synset_offset.split('-')
    #             offset = int(offset_pos[0])
    #             pos = offset_pos[1]
    #             lemma = line.split()[4]
    #             # print('{}-{}'.format(offset, pos))
    #             if lemma == 'glass':
    #                 print('{}-{}'.format(offset, pos))
    #                 print(wordnet_synset_from_pos_offset(pos, offset).definition())
                #     synset = wordnet_synset_from_pos_offset(pos, offset)
                #     if synset in synset_dict.keys():
                #         synset_dict[synset] += 1
                #     else:
                #         synset_dict[synset] = 1
                        
    # print(synset_dict)
    
if __name__ == '__main__':
    main()