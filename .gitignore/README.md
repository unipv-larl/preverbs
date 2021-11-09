<div align="center">
 
# TITLE OF THE PAPER

[![Paper](http://img.shields.io/badge/paper-ACL--anthology-B31B1B.svg)]()

</div>

## Description

This is the repository for the paper [*TITLE OF THE PAPER*](), presented at the [Workshop on Natural Language Processing
for Digital Humanities (NLP4DH)](https://rootroo.com/en/nlp4dh-workshop/) co-located with 
[ICON 2021](http://icon2021.nits.ac.in/) by [authors](link).

## Abstract

> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin lobortis mattis orci. In tempus tincidunt ligula, quis
> aliquet lacus vestibulum iaculis. Proin pulvinar tincidunt velit, sed tempus sem aliquet non. Pellentesque fermentum
> erat sit amet tempus ullamcorper. Nulla posuere dui vehicula, gravida nulla id, condimentum felis. Sed eu ligula
> cursus, tempus dui at, consectetur urna. Vivamus viverra leo eget libero hendrerit eleifend. Nulla at erat at eros
> pellentesque cursus. Mauris laoreet nisl sit amet ex facilisis, sed interdum felis luctus.

## Download

You can download a copy of all the files in this repository by cloning the
[git](https://git-scm.com/) repository:
```sh
git clone https://github.com/git-username/git-repo.git
```
or [download a zip archive](https://github.com/git-username/git-repo/archive/master.zip).

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

* TOKEN 1: lemma in the list; deprel=orphan

* TOKEN 2: upos=any; if upos=VERB → deprel=[Part, Inf, Gdv, Conv]

##### List of lemmas

*apa, ava, ā, ud, ni, nis, parā, puras, pra, sam, vi, achā, ati, adhi, anu, antar, api, abhi, upa, tiras, paras, pari,
puras, purā, prati*

#### Examples



## Authors

### [Name Surname]()

email: [prova@mail.com](mailto:prova@mail.com)

### [Name Surname]()

email: [prova@mail.com](mailto:prova@mail.com)

### [Name Surname]()

email: [prova@mail.com](mailto:prova@mail.com)

## Cite this work
```bibtex
@inproceedings{id-paper-2021,
    title = "TITLE OF THE PAPER",
    author = "Surname, Name",
    booktitle = "TITLE OF THE BOOK",
    month = month,
    year = "",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/",
    pages = "xx--yy",
}
```
