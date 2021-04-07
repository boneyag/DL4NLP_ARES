=================================================================================
                                 SyntagNet 1.0
                             http://syntagnet.org/

     Marco Maru, Federico Scozzafava, Federico Martelli and Roberto Navigli

                          Sapienza Università di Roma
                                 Babelscape srl
=================================================================================


SyntagNet is a manually-curated large-scale lexical-semantic combination database
which associates pairs of concepts with pairs of co-occurring words, 
hence capturing sense distinctions evoked by syntagmatic relations.

SyntagNet is licensed under the CC BY-NC-SA 4.0 License.


=================================================================================
PACKAGE CONTENTS
=================================================================================


* README.txt (this file);
* LICENSE.txt (terms and conditions of the CC BY-NC-SA 4.0 License);
* SYNTAGNET_1.0.txt (all the 88,019 semantic combinations available in SyntagNet). 


=================================================================================
FORMAT
=================================================================================


All the combinations in SYNTAGNET_1.0.txt are provided in plain text format.
Each entry is a tab-separated line terminated by a line feed character.
Each entry shows, in the following order:
	
1. WordNet 3.0 offset for the first argument of a combination;
2. WordNet 3.0 offset for the second argument of a combination;
3. First argument of a combination (lemma);
4. First argument of a combination (part of speech*);
5. Second argument of a combination (lemma);
6. Second argument of a combination (part of speech*).

* n stands for noun, while v stands for verb.

For example:

02150948v	06277280n	watch	v	television	n
01960911v	02512053n	swim	v	fish	n
02815950n	14802450n	beam	n	steel	n


=================================================================================
REFERENCE PAPER
=================================================================================


When using this resource, please refer to the following paper:

	Marco Maru, Federico Scozzafava, Federico Martelli and Roberto Navigli

	"SyntagNet: Challenging Supervised Word Sense Disambiguation 
	with Lexical-Semantic Combinations"

	In Proceedings of the 2019 Conference on Empirical Methods in Natural 
	Language Processing and the 9th International Joint Conference on 
	Natural Language Processing (EMNLP-IJCNLP),
	Hong Kong, China, November 3-7, 2019, pages 3532-3538.


=================================================================================
CONTACTS
=================================================================================


If you have any enquiries, please contact:

Marco Maru - Sapienza Università di Roma
(marco [dot] maru [at] uniroma1 [dot] it)

Federico Scozzafava - Sapienza Università di Roma
(scozzafava [at] di [dot] uniroma1 [dot] it)

Federico Martelli - Babelscape srl, Sapienza Università di Roma
(martelli [at] di [dot] uniroma1 [dot] it; martelli [at] babelscape [dot] com) 

Roberto Navigli - Sapienza Università di Roma
(navigli [at] di [dot] uniroma1 [dot] it)


