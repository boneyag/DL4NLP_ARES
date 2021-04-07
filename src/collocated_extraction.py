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

		with open('../data/ext1.txt', 'w') as r:

			for c in corpus:
				print(c)
				for ele in res_data:
					if ele[2] in c:
						if ele[4] in c:
							r.write(c)
			r.close()
		t.close()




if __name__ == '__main__':
    main()
