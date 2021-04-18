from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
import re
import csv


def main():
	#Extracting Sentences from Corpus for similar contexts
	with open('../data/synTag_extracts.csv') as f:
		reader = csv.reader(f);
		data = list(reader)

	#removing empty elements from list data
	res_data = [ele for ele in data if ele !=[]]

	#print(res_data[1][2])

	#s = 'I am glasses'
	#print('glass' in s)

	ext_sentences = []
	with open('../data/testCorpora_syntagExtraction.txt') as t:
		corpus = t.readlines()
		for c in corpus:
			#print(c)
			for ele in res_data:
				if ele[2] in c:
					if ele[4] in c:
						ext_sentences.append(c)
		t.close()

	ext_sentences = list(set(ext_sentences))					

	with open('../data/ext1.txt', 'w') as r:
		for line in ext_sentences:
			r.write(line)
		r.close()
		






if __name__ == '__main__':
    main()
