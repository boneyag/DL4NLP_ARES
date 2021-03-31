# DL4NLP_ARES
Replicate ARES (WSD model) 

Note: Currently this repo does not contain anything useful.

### How to run UKB on a custom input file (just a command, more details need to be included)
`./ukb/src/ukb_wsd --ppr -K ukb/scripts/wn30g.bin -D ukb/scripts/wn30_dict.txt ../data/glass_ukb_input2.txt > ../data/glass_ukb_output2.txt`

Individual branches contain different models that we tried out before merging them towards the main brach.

Final outcome should be the ARES word sense disambiguation (WSD) model as originally presented in [EMNLP 2020](https://www.aclweb.org/anthology/2020.emnlp-main.285.pdf)

Branch naming convension: 
`<author>-<too>-<tag>`, for example, `ag-BERT-trial` means Akalanka's branch on using/configuring BERT for a trial run.

Merging policy:
Both contributor will agree before a branch merge to a production ready branch (usually `main`).

Contributors:
Akalanka Galappaththi
Sakib Hasan
