from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

def wordnet_trial():
    
    for ss in wn.synsets('man'):
        print(ss, ss.definition())
        print(ss.lemmas())
        # print(ss.examples())

def wsd_with_lesk():

    print(lesk('I went fishing for some sea bass'.split(), 'bass', 'n'))
    print(lesk('The bass line of the song is too weak'.split(), 'bass', 's'))
    print(lesk('Avishai Cohen is an Israeli jazz musician. He plays double bass and is also a composer'.split(), 'bass', pos='n'))

def main():
    wordnet_trial()

    # wsd_with_lesk()

if __name__ == '__main__':
    main()