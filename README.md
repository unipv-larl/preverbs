<div align="center">
 
# Annotating “Absolute” Preverbs in the Homeric and Vedic Treebanks

[![Conference](https://img.shields.io/badge/conference-LREC--2022-blue.svg)](https://lrec2022.lrec-conf.org/en/)
[![Workshop](https://img.shields.io/badge/workshop-LT4HALA-9cf.svg)](https://circse.github.io/LT4HALA/2022/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

</div>

## Description

This is the repository for the paper [*Annotating “Absolute” Preverbs in the Homeric and Vedic Treebanks*](), presented
at the [2nd Workshop on Language Technologies for Historical and Ancient Languages (LT4HALA)](https://circse.github.io/LT4HALA/2022/) co-located with [LREC 2022](https://lrec2022.lrec-conf.org/en/) by Chiara
Zanchi, Erica Biagetti and Luca Brigada Villa.

## Abstract

> Indo-European preverbs are uninflected
morphemes attaching to verbs and
modifying their meaning. In Early Vedic
and Homeric Greek, the same uninflected
morphemes held ambiguous morphosyntactic
status which raises issues
for syntactic annotation. In this paper, we
focus on the annotation of preverbs in so-
called “absolute” position in two treebanks
annotated according to the Universal
Dependencies scheme. After discussing
some issues related to the current
annotation, we propose a new scheme that
better accounts for the variety of absolute
constructions in which preverbs occur as
well as for their syntactic function.

## Download

You can download a copy of all the files in this repository by cloning the
[git](https://git-scm.com/) repository:
```sh
git clone https://github.com/unipv-larl/preverbs.git
```
or [download a zip archive](https://github.com/unipv-larl/preverbs/archive/master.zip).

## Requirements

**Programming language:** python3

**Modules and packages:** [conllu](https://pypi.org/project/conllu/), sys, logging, os

## Usage

### Content of the repository

In the repository you will find:

* this README

* **[scrpts](scripts):** a folder containing the scripts used to extract the occurrences from the treebanks

* **[data](data):** a folder containing the treebanks analyzed in the study

* **[results](results):** a folder where the results will be stored after the execution of the script

### Tutorial

The first thing you should do to run the script is open a terminal and move to the directory where you stored the files.

Then, you can execute these line of code:

```sh
python3 ./scripts/queries.py iliad odyssey RV
```

After the execution of the script you should find the results in the results folder.
## Queries

In this section we list and give a short explanation of the queries used to extract the occurrences from the treebanks.

### Ancient Greek query

The treebanks considered in our paper for Ancient Greek were the
[UD conversion of the Iliad and Odyssey](https://github.com/francescomambrini/katholou/tree/main/ud_treebanks/agdt/data)
(files starting with *tlg00012.tlg001*: Iliad - files starting with *tlg00012.tlg002*: Odyssey).

#### Query

The query to extract the occurrences from the Ancient Greek's treebanks was designed to find a pair of tokens involved
in a syntactic relation in which the head was a noun or a pronoun and the dependent was in the list of lemmas. In
addition to that, the noun (or pronoun)'s deprel must be "advcl" or "conj" and the dependent's deprel must be
"compound:prt".

* TOKEN 1: lemma in list; deprel=compound:prt; head=TOKEN 2

* TOKEN 2: upos=[NOUN, PRON]; deprel=[advcl, conj]

##### List of lemmas

*ἀμφί, ἀνά, ἀντί, ἀπό, διά, ἐν, εἰς, ἐκ, ἐπί, ὑπέρ, ὑπό, κατά, μετά, παρά, περί, πρό, πρός, σύν*

#### Examples

### Sanskrit query

The treebank considered in our paper for Sanskrit was the Rig Veda treebank (FONTE ?).

#### Query

The query to extract the occurrences from the Rig Veda treebank was designed to find a pair of tokens involved in a
syntactic relation in which the head could be any part-of-speech and the dependent was in the list of lemmas. In
addition to that, the lemma must have "orphan" as deprel and if the head of the relation is a verb, it must not be a
finite verb.

* TOKEN 1: lemma in the list; deprel=orphan; head=TOKEN 2

* TOKEN 2: upos=any; if upos=VERB → VerbForm=[Part, Inf, Gdv, Conv]

##### List of lemmas

*apa, ava, ā, ud, ni, nis, parā, puras, pra, sam, vi, achā, ati, adhi, anu, antar, api, abhi, upa, tiras, paras, pari,
puras, purā, prati*

#### Examples



## Authors

### Chiara Zanchi

email: [chiara.zanchi01@unipv.it](mailto:chiara.zanchi01@unipv.it)

### Erica Biagetti

email: [erica.biagetti@unipv.it](mailto:erica.biagetti@unipv.it)

### Luca Brigada Villa

email: [luca.brigadavilla@unibg.it](mailto:luca.brigadavilla@unibg.it)

## License

The data are distributed under a [CC-BY-SA license](https://creativecommons.org/licenses/by-sa/4.0/).

See the linked websites of the different projects for the licenses of the original data.
