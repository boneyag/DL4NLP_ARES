# DL4NLP_ARES
Replicate ARES (WSD model) [1]

### Directory structre

`data` contains sample input corpus, input file generated according to UKB accepted format, and UKB results files.
`src` contains four scripts that are required to run the experiments. 
`src/ukb` contains scripts required to run UKB. The tool is compiled and ready to run. You should compile the UKB before executing the scripts. Follow the steps in [here](https://github.com/asoroa/ukb/tree/master/src) to compile your own UKB tool. 

### Setup Wikipedia dump as the input corpus
1. Download a Wikipedia data dump (the authors used the 2019 July data dump). Data dumps are huge compressed files (~18GB). Therefore, downloading through [torrents](https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia) is a good option.
2. Use the command `bzip2 -dk <filename>.xml.bz2` to extract the XML file. Don't try to open this file as it's nearly ~75GB.
3. Use the [wikiextractor](https://github.com/attardi/wikiextractor) extract articles to readable size files. 
    3.1. I preferred to execute the script instead of installing the wikiextractor. Use the input parameter to specify the location of the XML file and the output parameter to specify the location for output files. It should take several minutes to complete the task. Once completed, there should be a set of directories like AA, AB, ..., and in each dir, there should be files like wiki_00, wiki_01.
    3.2. Each file contain several documents in the format of
    ```
    <doc id="..." ulr="..." title="...">
     ...
    </doc>
    ```
    Since there are no root level tags that enclose all <doc> tags, it is not possible to read the entire file using an XML reader in python. Therefore, we use the `add_root_tag` function to modify all files by adding the <articles> tags to each file.
4. Since there are over 144000 files, searching for sentences takes nearly 980s. Therefore, we use [Whoosh](https://whoosh.readthedocs.io/en/latest/quickstart.html) to index documents which speed up the search to 6.3s. Run the `wiki_dump_reader.py` script to modify the files and create an index. (We decided not to upload the index as the file size is too large)

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

* * *

## References
[1] Bianca Scarlini, Tommaso Pasini, and Roberto Navigli. 2020. With more contexts come better performance: Contextualized sense embedding for all round word sense disambiguation. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, ENNLP 2020, On-line, November 16-20, 2020, pages 3528-3539. Association for Computational Linguistics.