# DL4NLP_ARES
Replicate ARES (WSD model) 

### Directory structre

`data` contains sample input corpus, input file generated according to UKB accepted format, UKB results files.
`src` contains four scripts that are required to run the experiments according to the progress report II. 
`src\ukb` contains script required to run UKB. The tool is compiled and ready to run. However, you should use your own platform dependent version before use. Follow the steps in [here](https://github.com/asoroa/ukb/tree/master/src) to compile your own UKB tool. 

### Clustering sentences
Change the directory to `src` and run `python3 bert_wsd.py` to create two clusters. To run this script you need to have `numpy`, `pandas`, `torch`, `transformers`, and `sklearn` packages installed in your virtual environment. You need Python 3+ as well. The script expect `sample_sentences.txt` in data directory. This can be changed to actual corpus when running the full replication in future. If the execution is successful, there will be `sample_sentences_clusters_glass.csv` in the data directory. 

### Running UKB on each cluster to apply sense embedding
Run `python3 run_ukb.py` to create bag of words for each cluster. Then the script tranform raw words to UKB acceptable input format (an example is provided below). If successful there will be a `glass_ukb_input2.txt` in the data directory. 

```
ctx_01
man#n#w1#1 kill#v#w2#1 cat#n#w3#1 hammer#n#w4#1
```
To run UKB on the input file, run the follwoing command.
`./ukb/src/ukb_wsd --ppr_w2w -K ukb/scripts/wn30g.bin -D ukb/scripts/wn30_dict.txt ../data/glass_ukb_input2.txt > ../data/glass_ukb_output2w2.txt`

If successful, the script will create `glass_ukb_output2w2w.txt` file. The output file contain the WordNet sense offset and lemma (an example is provided).
```
ctx_1 w15  03438257-n !! glass
ctx_2 w19  14881303-n !! glass
```

### Find the sense and description from WordNet
Run `python3 wsd_wordnet.py` to find the sense and sense description from the sense offset. 

### Using Wikipedia dump as the input corpus

Download the wikipedia dump to your local machine. This is large bz file. You will get the XML file once you extract the file.

Don't try to open the file because it is very large file (over 70 GB). Fortunately I found this python script that read the file and 
split into smaller readable size files (100 MB). Follow the instructions in this [GitHub repository](https://github.com/attardi/wikiextractor) to convert the large XML file to small readable files. Those files contain content wrapped in <doc> ... </doc> tags. Since a file contain multiple docs Python libraries will only read the first doc. Therefore, we need to add root level tags that encloses all doc tags in each file.

The `wiki_dump_reader.py` script provide this functionality. However, you need to change the input and output file paths accordingly before running the script.

***

Individual branches contain different models that we tried out before merging them towards the main brach.

Final outcome should be the ARES word sense disambiguation (WSD) model as originally presented in [EMNLP 2020](https://www.aclweb.org/anthology/2020.emnlp-main.285.pdf)

Branch naming convension: 
`<author>-<tool>-<tag>`, for example, `ag-BERT-trial` means Akalanka's branch on using/configuring BERT for a trial run.

Merging policy:
Both contributor will agree before a branch merge to a production ready branch (usually `main`).

Contributors:
Akalanka Galappaththi
Sakib Hasan
