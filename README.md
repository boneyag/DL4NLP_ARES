# DL4NLP_ARES
Replicate ARES (WSD model) [1]

To use this code first clone the repository to a desired location.
`git clone https://github.com/boneyag/DL4NLP_ARES.git` 

Once the repository is cloned to the local machine create following directories in the data directory:
`clusters`, `embeddings`, `temp`, `wiki_dump`, and `wiki_index`.

### Install requirements 
Use the requirements file to install the dependencies.
`pip3 install -r requirements.txt`

### Directory structre

`data` contains sample input corpus, input file generated according to UKB accepted format, and UKB results files.
`src` contains four scripts that are required to run the experiments. 
`src/ukb` contains scripts required to run UKB. The tool is compiled and ready to run. You should compile the UKB before executing the scripts. Follow the steps in [here](https://github.com/asoroa/ukb/tree/master/src) to compile your own UKB tool. 

### Setup Wikipedia dump as the input corpus
1. Download a Wikipedia data dump (the authors used the 2019 July data dump). Data dumps are huge compressed files (~18GB). Therefore, downloading through [torrents](https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia) is a good option.
2. Use the command `bzip2 -dk <filename>.xml.bz2` to extract the XML file. Don't try to open this file as it's nearly ~75GB.
3. Use the [wikiextractor](https://github.com/attardi/wikiextractor) extract articles to readable size files. 
    3.1. I preferred to execute the script instead of installing the wikiextractor. Use the input parameter to specify the location of the XML file and the output parameter to specify the location for output files. It should take several minutes to complete the task. Once completed, there should be a set of directories like AA, AB, ..., and in each dir, there should be files like wiki_00, wiki_01. Use following parameter settings to make the files small as possible (200Kb) and use 8 worker threads. Make sure to replace `<?>` accordingly.
    `python -m <path to>/wikiextractor.WikiExtractor -o <output location> -b 200K --no-template --processes <8> <Wikipedia dump file>`

    3.2. Each file contain several documents in the format of
    ```
    <doc id="..." ulr="..." title="...">
     ...
    </doc>
    ```
    Since there are no root level tags that enclose all <doc> tags, it is not possible to read the entire file using an XML reader in python. Therefore, we use the `add_root_tag` function to modify all files by adding the <articles> tags to each file.

4. Since there are over 144000 files, searching for sentences takes nearly 980s. Therefore, we use [Whoosh](https://whoosh.readthedocs.io/en/latest/quickstart.html) to index documents which speed up the search to 6.3s. Run the `prepare_input_corpus.py` script to modify the files and create an index. (We decided not to upload the index as the file size is too large). Before running the script, modify the input_path in `add_root_tag` function. Also, create a dir `data/wiki_dump` to have a valid out_put path.

### Runnig ARES
Run `src/run_ares.py` to generate embedding for a list of lemmas in `input_lemmas.txt` in data directory. This will take a lot of time to complete. If you planning to test for a few lemmas replace the input_lemmas file content with less number of words. Current file contain over 1000 entries. 

### Running evaluation
Run `src/evaluate_ares.py` to generate embeddings for target words in hard-corded sentence id from Senseval-2. The results will print on the terminal. The results contain the target lemma, Wordnet lexid of extracted senses, predicted sense lexid, and gold key lexid.

*Currently the model is not performing well. Required further improvements to generate more senses.*

***
### Repository contributors and branch naming conventions

Individual branches contain different models that we tried out before merging them towards the main brach.

Final outcome should be the ARES word sense disambiguation (WSD) model as originally presented in the reference paper [1].

Branch naming convension: 
`<author>-<tool>-<tag>`, for example, `ag-BERT-trial` means Akalanka's branch on using/configuring BERT for a trial run.

Merging policy:
Both contributor will agree before a branch merge to a production ready branch (usually `main`).

Contributors:
Akalanka Galappaththi and Sakib Hasan

* * *

## References
[1](https://www.aclweb.org/anthology/2020.emnlp-main.285.pdf) Bianca Scarlini, Tommaso Pasini, and Roberto Navigli. 2020. With more contexts come better performance: Contextualized sense embedding for all round word sense disambiguation. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, ENNLP 2020, On-line, November 16-20, 2020, pages 3528-3539. Association for Computational Linguistics.
