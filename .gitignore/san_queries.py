import conllu
import query_conllu
import sys
import logging
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")


def match_query1(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 1:
    three consecutive tokens (verb is noun/pron's parent):
                TOKEN 1: upos=NOUN or upos=PRON; Case is Acc, Loc or Abl; deprel is obl, obl:source, obl:goal, obl:loc, obl:path, obl:manner, obl:temp
                TOKEN 2: lemma in the list
                TOKEN 3: upos=VERB

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if tok['lemma'] in lemmas:
        left = query_conllu.move_left(tok, sent)
        right = query_conllu.move_right(tok, sent)
        if query_conllu.match_conditions(right, upos='VERB') and query_conllu.match_conditions(left, upos=['NOUN', 'PRON'], deprel=['obl', 'obl:source', 'obl:goal', 'obl:loc', 'obl:path', 'obl:manner', 'obl:temp'], Case=['Acc', 'Loc', 'Abl']) and left['head'] == right['id']:
            return {'preverb': tok, 'verb': right, 'noun': left, 'sentence': sent}
        else:
            return {}
    else:
        return {}


def match_query2(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 2:
    three consecutive tokens (verb is noun/pron's parent):
                TOKEN 1: upos=VERB
                TOKEN 2: lemma in the list
                TOKEN 3: upos=VERB

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if tok['lemma'] in lemmas:
        left = query_conllu.move_left(tok, sent)
        right = query_conllu.move_right(tok, sent)
        if query_conllu.match_conditions(left, upos='VERB') and query_conllu.match_conditions(right, upos=['NOUN', 'PRON'], deprel=['obl', 'obl:source', 'obl:goal', 'obl:loc', 'obl:path', 'obl:manner', 'obl:temp'], Case=['Acc', 'Loc', 'Abl']) and right['head'] == left['id']:
            return {'preverb': tok, 'verb': left, 'noun': right, 'sentence': sent}
        else:
            return {}
    else:
        return {}


def match_query3(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 3:
    preverb-noun [...] verb. Verb is preverb and noun/pron's parent:
                TOKEN 1: lemma in the list
                TOKEN 2: upos=NOUN or upos=PRON; Case is Acc, Loc or Abl; deprel is obl, obl:source, obl:goal, obl:loc, obl:path, obl:manner, obl:temp
                TOKEN 3: TOKEN 1's parent and upos=VERB

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if tok['lemma'] in lemmas:
        right = query_conllu.move_right(tok, sent)
        parent_right = query_conllu.get_parent(right, sent)
        if query_conllu.match_conditions(parent_right, upos='VERB') and query_conllu.match_conditions(right, upos=['NOUN', 'PRON'], deprel=['obl', 'obl:source', 'obl:goal', 'obl:loc', 'obl:path', 'obl:manner', 'obl:temp'], Case=['Acc', 'Loc', 'Abl']) and query_conllu.move_right(right, sent) != parent_right and parent_right['id'] > right['id']:
            return {'preverb': tok, 'verb': parent_right, 'noun': right, 'sentence': sent}
        else:
            return {}
    else:
        return {}


def match_query4(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 4:
    preverb and any token (finite verb); verb is preverb's parent:
                TOKEN 1: lemma in the list; deprel=orphan
                TOKEN 2: upos=any and VerbForm field empty

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if tok['lemma'] in lemmas:
        parent = query_conllu.get_parent(tok, sent)
        if query_conllu.match_conditions(tok, deprel='orphan'):
            if query_conllu.match_conditions(parent, upos='VERB'):
                if query_conllu.match_conditions(parent, VerbForm=['Part', 'Inf', 'Gdv', 'Conv']):
                    return {'preverb': tok, 'verb': parent, 'noun': None, 'sentence': sent}
                else:
                    return {}
            else:
                return {'preverb': tok, 'verb': parent, 'noun': None, 'sentence': sent}
        else:
            return {}
    else:
        return {}


# define the list of lemmas that can be preverbs
lemmas = ['apa', 'ava', 'ā', 'ud', 'ni', 'nis', 'parā', 'puras', 'pra', 'sam', 'vi', 'achā', 'ati', 'adhi', 'anu',
          'antar', 'api', 'abhi', 'upa', 'tiras', 'paras', 'pari', 'puras', 'purā', 'prati']


logging.info('loading treebank')
filepath_tb = os.path.join('data', f'{sys.argv[1]}.conllu')

with open(filepath_tb, 'r') as data:
    tb = [tokenlist for tokenlist in conllu.parse_incr(data)]
logging.info(f'treebank {sys.argv[1]}.conllu loaded without errors')

res1 = 'Query 1: three consecutive tokens (verb is noun/pron\'s parent)\n' \
       '         TOKEN 1: upos=NOUN or upos=PRON; Case is Acc, Loc or Abl; deprel is obl, obl:source, obl:goal, obl:loc, obl:path, obl:manner, obl:temp\n' \
       '         TOKEN 2: lemma in the list\n' \
       '         TOKEN 3: upos=VERB\n'

res2 = 'Query 2: three consecutive tokens (verb is noun/pron\'s parent)\n' \
       '         TOKEN 1: upos=VERB\n' \
       '         TOKEN 2: lemma in the list\n' \
       '         TOKEN 3: upos=NOUN or upos=PRON; Case is Acc, Loc or Abl; deprel is obl, obl:source, obl:goal, obl:loc, obl:path, obl:manner, obl:temp\n'

res3 = 'Query 3: preverb-noun [...] verb. Verb is preverb and noun/pron\'s parent.\n' \
       '         TOKEN 1: lemma in the list\n' \
       '         TOKEN 2: upos=NOUN or upos=PRON; Case is Acc, Loc or Abl; deprel is obl, obl:source, obl:goal, obl:loc, obl:path, obl:manner, obl:temp\n' \
       '         TOKEN 3: TOKEN 1\'s parent and upos=VERB\n'

res4 = 'Query 4: preverb and any token (finite verb); verb is preverb\'s parent\n' \
       '         TOKEN 1: lemma in the list; deprel=orphan\n' \
       '         TOKEN 2: upos=any and VerbForm field empty\n'


logging.info('starting checking sentences')
for sent in tb:
    for tok in sent:
        q1 = match_query1(tok, sent)
        q2 = match_query2(tok, sent)
        q3 = match_query3(tok, sent)
        q4 = match_query4(tok, sent)
        if q1:
            res1 += f'\nsent_id: {q1["sentence"].metadata["sent_id"]}\n' \
                    f'Sentence: {q1["sentence"].metadata["text"]}\n' \
                    f'NOUN/PRON → {q1["noun"]["form"]}\n' \
                    f'PREVERB → {q1["preverb"]["form"]}; deprel: {q1["preverb"]["deprel"]}\n' \
                    f'VERB → {q1["verb"]["form"]}\n'
        if q2:
            res2 += f'\nsent_id: {q2["sentence"].metadata["sent_id"]}\n' \
                    f'Sentence: {q2["sentence"].metadata["text"]}\n' \
                    f'VERB → {q2["verb"]["form"]}\n' \
                    f'PREVERB → {q2["preverb"]["form"]}; deprel: {q2["preverb"]["deprel"]}\n' \
                    f'NOUN/PRON → {q2["noun"]["form"]}\n'
        if q3:
            res3 += f'\nsent_id: {q3["sentence"].metadata["sent_id"]}\n' \
                    f'Sentence: {q3["sentence"].metadata["text"]}\n' \
                    f'PREVERB → {q3["preverb"]["form"]}; deprel: {q3["preverb"]["deprel"]}\n' \
                    f'NOUN/PRON → {q3["noun"]["form"]}\n' \
                    f'VERB → {q3["verb"]["form"]}\n'
        if q4:
            res4 += f'\nsent_id: {q4["sentence"].metadata["sent_id"]}\n' \
                    f'Sentence: {q4["sentence"].metadata["text"]}\n' \
                    f'PREVERB → {q4["preverb"]["form"]}; deprel: {q4["preverb"]["deprel"]}\n' \
                    f'OTHER TOKEN → {q4["verb"]["form"]}; pos: {q4["verb"]["upos"]}\n'

logging.info('check over')

logging.info(f'saving results into files at {os.path.join("results", "sanskrit")}')

filepath_out = os.path.join('results', 'sanskrit', f'{sys.argv[1]}_q1.txt')
with open(filepath_out, 'w') as file:
    file.write(res1)


filepath_out = os.path.join('results', 'sanskrit', f'{sys.argv[1]}_q2.txt')
with open(filepath_out, 'w') as file:
    file.write(res2)


filepath_out = os.path.join('results', 'sanskrit', f'{sys.argv[1]}_q3.txt')
with open(filepath_out, 'w') as file:
    file.write(res3)


filepath_out = os.path.join('results', 'sanskrit', f'{sys.argv[1]}_q4.txt')
with open(filepath_out, 'w') as file:
    file.write(res4)

logging.info(f'{sys.argv[1]}.conllu --> job done')
