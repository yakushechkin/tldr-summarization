# BART

## 1. Fine-tune BART

### Requirements

- Python 3.7

To run the script, you can use Google Colab, which already has all the necessary actions to start the fine-tuning process.

But I will still describe the necessary actions here, since later I switched to using a remote machine provided by the University of Passau due to the problem of  disk storage limitation in Google Colab for saving checkpoints.

1. You need `scitldr`'s requirements.txt, BUT please clone [my fork](https://github.com/yakushechkin/scitldr) of the repo:

```bash
git clone https://github.com/yakushechkin/scitldr.git
```

Install necessary modules:
```bash
pip install -r scitldr/requirements.txt
```

2. Download the pre-trained version of BART from: https://dl.fbaipublicfiles.com/fairseq/models/bart.large.tar.gz and unzip the archive.
You can use the following snippet for it (or adapt it for bash usage):

```python
filename = f'bart.large.tar.gz'
url = f'https://dl.fbaipublicfiles.com/fairseq/models/bart.large.tar.gz'
!wget -q {url}
!tar -xf {filename} && rm -f {filename}
```

3. Clone the original Fairseq repo:

```bash
git clone https://github.com/pytorch/fairseq.git
```

4. Run the Data preprocessing script using the internal SciTLDR's module. You can use the following script:

```bash
cd scitldr/SciTLDR-Data
export TASK=SciTLDR-A # Choose from {A, AIC, FullText}
chmod +x make_datafiles.sh
./make_datafiles.sh # BPE preprocess
```

5. Fine-tune the model. Our solution is based on the hyperparameters from the SciTLDR paper and on https://github.com/pytorch/fairseq/blob/master/examples/bart/README.summarization.md.

We used the following snippet for fune-tunning the model on the remote machine.

```bash
TOTAL_NUM_UPDATES=500  
WARMUP_UPDATES=100      
LR=3e-05
MAX_TOKENS=1024
UPDATE_FREQ=1
BART_PATH=/bart.large/model.pt

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 fairseq-train scitldr/SciTLDR-Data/SciTLDR-A/ctrl-bin \
    --restore-file $BART_PATH \
    --max-tokens $MAX_TOKENS \
    --task translation \
    --source-lang source --target-lang target \
    --truncate-source \
    --layernorm-embedding \
    --share-all-embeddings \
    --share-decoder-input-output-embed \
    --reset-optimizer --reset-dataloader --reset-meters \
    --required-batch-size-multiple 1 \
    --arch bart_large \
    --criterion label_smoothed_cross_entropy \
    --label-smoothing 0.1 \
    --dropout 0.1 --attention-dropout 0.1 \
    --weight-decay 0.01 --optimizer adam --adam-betas "(0.9, 0.999)" --adam-eps 1e-08 \
    --clip-norm 0.1 \
    --lr-scheduler polynomial_decay --lr $LR --total-num-update $TOTAL_NUM_UPDATES --warmup-updates $WARMUP_UPDATES \
    --update-freq $UPDATE_FREQ \
    --skip-invalid-size-inputs-valid-test \
    --find-unused-parameters;
```

6. Save the checkpoint file with the best results for evaluation. The name would be `checkpoint_best.pt`

The Notebook: **[finetuneBART.ipynb]()** : [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1IVY5vRcFTvuZWPvF9h_FfBFlr1kY-54u?usp=sharing)


## 2. Evaluate the Model

### Requirements

- Python 3.7

To run the script, you can use Google Colab, which already has all the necessary actions to start the evaluation process.

But again, I will describe the necessary actions here.

1. You need `scitldr`'s requirements.txt, BUT please clone [my fork](https://github.com/yakushechkin/scitldr) of the repo:

```bash
git clone https://github.com/yakushechkin/scitldr.git
```

Install necessary modules:
```bash
pip install -r scitldr/requirements.txt
```

2. Install prerequisites for PyRouge:

```bash
pip install -U git+https://github.com/pltrdy/pyrouge
```

3. Clone the repo, setup the module and ROUGE

```bash
git clone https://github.com/isabelcachola/files2rouge.git     
cd files2rouge
python setup_rouge.py
python setup.py install
```

4. Install libxml-parser-perl, because of error: *Cannot locate XML/Parser.pm: The solution is to install libxml-parser-perl package by Advanced Package Tool*. The solution is based on https://blog.csdn.net/qq_33220757/article/details/105692883.

```bash
sudo apt-get install libxml-parser-perl
```

5. Run the Data preprocessing script using the internal SciTLDR's module. You can use the following script:

```bash
cd scitldr/SciTLDR-Data
export TASK=SciTLDR-A # Choose from {A, AIC, FullText}
chmod +x make_datafiles.sh
./make_datafiles.sh # BPE preprocess
```

6. Evaluate the BART model on SciTLDR test data:

This code takes in a `test.source` file, in which each line is an input and outputs a `test.hypo` file with the predictions. It imports a `test.jsonl` file as a reference and stores the rouge score in `test.hypo.score`.
```bash
python evaluate.py SciTLDR-Data/SciTLDR-A/ctrl /path/to/model/dir/ --checkpoint_file checkpoint_best.pt --beam 4 --lenpen 0.2
```
OR
```bas
python evaluate.py SciTLDR-Data/SciTLDR-AIC/ctrl /path/to/model/dir/ --checkpoint_file checkpoint_best.pt --beam 2 --lenpen 0.2
```


The Notebook: **[evaluateBART.ipynb]()** : [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1PY-Ecnq6puuparAjPEFcaJAzEw4arOAn?usp=sharing)
