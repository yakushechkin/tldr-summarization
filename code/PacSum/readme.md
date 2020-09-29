# PacSum

## 1. Data Preprocessing

### Requirements
Dependencies:  Python 3.7, h5py, json, jsonlines, numpy, errno, argparse, os

For the data conversion, you will need `scitldr`.
Please clone [my fork](https://github.com/yakushechkin/scitldr) of the repo.

1. **[convertscitldr.py](/PacSum/convertscitldr.py)** :

The raw SciTLDR data is in JSONL format, while the PacSum can only work with H5DF data. The data schema is also different and we should take this into account. This script is for SciTLDR conversion with the required schema and format.

Example of use:
```bash
python3 convertscitldr.py --datadir path/to/SciTLDR-Data/ --task 'A'
```

where a path must be to the folder SciTLDR-Data: `../scitldr/SciTLDR-Data/`.

-------

2. **[SciTLDRforPacSum.ipynb](/PacSum/SciTLDRforPacSum.ipynb)** :

The same functions for converting JSONL SciTLDR data to PacSum H5DF data with the required schema and format but in Jupyter Notebook for the convenience of conducting experiments.

## 2. Run and evaluate the Model

### Requirements
Dependencies:  Python3.6, pytorch >= 1.0, numpy, gensim, pyrouge

### PyRouge Error Handling

Most likely, all errors will occur, so it is better to do all the steps described below in advance.

- *No such file or directory: 'XXX/.pyrouge/settings.ini'*: Basically you need to clone both of the pyrouge repos, in different folders, and then point to the pyrouge-1.5.5 in the tools folder. The solution is based on https://github.com/nlpyang/BertSum/issues/35.

```python
!pip install pyrouge --upgrade
!pip install https://github.com/bheinzerling/pyrouge/archive/master.zip
!pip install pyrouge
!pip show pyrouge
!git clone https://github.com/andersjo/pyrouge.git
from pyrouge import Rouge155
!pyrouge_set_rouge_path 'pyrouge/tools/ROUGE-1.5.5'
```

- *Cannot locate XML/Parser.pm*: The solution is to install libxml-parser-perl package by Advanced Package Tool. The solution is based on https://blog.csdn.net/qq_33220757/article/details/105692883.

```bash
sudo apt-get install libxml-parser-perl
```

- *Cannot open exception db file for reading: /home/pythonrouge/pythonrouge/RELEASE-1.5.5/data/WordNet-2.0.exc.db*: The problem was solved by building a new link to the WordNet-2.0.exc.db exception. The solution is based on https://github.com/tagucci/pythonrouge.

```bash
cd pyrouge/tools/ROUGE-1.5.5/data
rm WordNet-2.0.exc.db # only if exist
cd WordNet-2.0-Exceptions
rm WordNet-2.0.exc.db # only if exist

./buildExeptionDB.pl . exc WordNet-2.0.exc.db
cd ../
ln -s WordNet-2.0-Exceptions/WordNet-2.0.exc.db WordNet-2.0.exc.db
```
-------
1. **[PacSumModelCNN.ipynb](/PacSum/PacSumModelCNN.ipynb)** : [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1GbFKKjxZhsN6KgtzqldLrJS-j9ziA9Z4?usp=sharing)

This script is for running PacSum on CNN|DM. The Notebook contains necessary information, but it's also worth taking a look at the original [PacSum](https://github.com/mswellhao/PacSum) repository. You can also download the archive with the generated summaries by running the last cell.



2. **[PacSumModelSciTLDR.ipynb](/PacSum/PacSumModelSciTLDR.ipynb)** : [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1GzQ-2BL74bokUtBX3uAMyev_1PXUpZ6z?usp=sharing)

This script is for running PacSum on SciTLDR. The only thing you need to do is upload the files to Google Colab when it asks you to do so during the cell launch. The files must be, for example, for task `A` from `scitldr/SciTLDR-Data/SciTLDR-A/forPacSum` folder that appears as a result of the script convertscitldr.py. The files should have the following names: `tldr_train.h5df`, `tldr_test.h5df` and `tldr_dev.h5df`. You can also download the archive with the generated TLDRs by running the last cell.
