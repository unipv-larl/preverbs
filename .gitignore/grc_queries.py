import conllu
import query_conllu
import sys
import os
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")


def match_query1(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 1:
    Query 1: two tokens - adv (lemma in list) and verb (adv's parent):
                TOKEN 1: upos=ADV (head=TOKEN2)
                TOKEN 2: upos=VERB

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if not query_conllu.is_bounded(tok, sent) and query_conllu.match_conditions(tok, upos='ADV') and tok['lemma'] in lemmas:
        parent = query_conllu.get_parent(tok, sent)
        if query_conllu.match_conditions(parent, upos='VERB'):
            return {'preverb': tok, 'verb': parent, 'noun': None, 'sentence': sent}
        else:
            return {}
    else:
        return {}


def match_query2(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 2:
    three tokens - verb (noun's parent), adp, noun (adp's parent); noun follows, but not immediately adp:
                TOKEN 1: upos=VERB
                TOKEN 2: upos=ADP (head=TOKEN3)
                TOKEN 3: upos=NOUN or upos=PRON, deprel is obl, obl:arg or advmod (head=TOKEN1)

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if not query_conllu.is_bounded(tok, sent) and query_conllu.match_conditions(tok, upos='ADP') and tok['lemma'] in lemmas:
        parent = query_conllu.get_parent(tok, sent)
        gparent = query_conllu.get_parent(parent, sent)
        if query_conllu.match_conditions(parent, upos=['NOUN', 'PRON'], deprel=['obl', 'obl:arg', 'advmod']) and query_conllu.match_conditions(gparent, upos='VERB'):
            if parent['id'] - tok['id'] > 1:
                succ = query_conllu.move_right(tok, sent)
                while succ != parent:
                    if succ['head'] == parent['id']:
                        return {}
                    succ = query_conllu.move_right(succ, sent)
                return {'preverb': tok, 'verb': gparent, 'noun': parent, 'sentence': sent}
            else:
                return {}
        else:
            return {}


def match_query3(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 3:
    three consecutive tokens; adp-noun-verb:
                TOKEN 1: upos=ADP
                TOKEN 2: upos=NOUN or upos=PRON
                TOKEN 3: upos=VERB

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if not query_conllu.is_bounded(tok, sent) and tok['lemma'] in lemmas:
        right1 = query_conllu.move_right(tok, sent)
        right2 = query_conllu.move_right(right1, sent)
        if query_conllu.match_conditions(right2, upos='VERB'):
            if query_conllu.match_conditions(right1, upos=['NOUN', 'PRON']):
                return {'preverb': tok, 'verb': right2, 'noun': right1, 'sentence': sent}
            else:
                return {}
        else:
            return {}
    else:
        return {}


def match_query3a(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 3a:
    three consecutive tokens; adp-noun-verb:
                TOKEN 1: upos=ADP
                TOKEN 2: upos=NOUN or upos=PRON (is not TOKEN's 1 head)
                TOKEN 3: upos=VERB

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if not query_conllu.is_bounded(tok, sent) and tok['lemma'] in lemmas:
        right1 = query_conllu.move_right(tok, sent)
        right2 = query_conllu.move_right(right1, sent)
        if query_conllu.match_conditions(right2, upos='VERB'):
            if query_conllu.match_conditions(right1, upos=['NOUN', 'PRON']) and tok['head'] != right1['id']:
                return {'preverb': tok, 'verb': right2, 'noun': right1, 'sentence': sent}
            else:
                return {}
        else:
            return {}
    else:
        return {}


def match_query3b(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 3b:
    three consecutive tokens; adp-noun-verb:
                TOKEN 1: upos=ADP
                TOKEN 2: upos=NOUN or upos=PRON; deprel is obj or obl (head=TOKEN 3)
                TOKEN 3: upos=VERB

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if not query_conllu.is_bounded(tok, sent) and tok['lemma'] in lemmas:
        right1 = query_conllu.move_right(tok, sent)
        right2 = query_conllu.move_right(right1, sent)
        if query_conllu.match_conditions(right2, upos='VERB'):
            if query_conllu.match_conditions(right1, upos=['NOUN', 'PRON'], deprel=['obj', 'obl']) and right1['head'] == right2['id']:
                return {'preverb': tok, 'verb': right2, 'noun': right1, 'sentence': sent}
            else:
                return {}
        else:
            return {}
    else:
        return {}


def match_query4(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY 1:
    two tokens - lemma in list and noun or pron (lemma's parent):
                TOKEN 1: lemma in list; deprel=compound:prt (head=TOKEN 2)
                TOKEN 2: upos is NOUN or PRON; deprel is advcl or conj

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if not query_conllu.is_bounded(tok, sent) and tok['lemma'] in lemmas and query_conllu.match_conditions(tok, deprel='compound:prt'):
        parent = query_conllu.get_parent(tok, sent)
        if query_conllu.match_conditions(parent, upos=['NOUN', 'PRON'], deprel=['conj', 'advcl']):
            return {'preverb': tok, 'noun': parent, 'verb': None, 'sentence': sent}
        else:
            return {}
    else:
        return {}


# list of lemmas that can be preverbs
lemmas = ['ἀμφί', 'ἀνά', 'ἀντί', 'ἀπό', 'διά', 'ἐν', 'εἰς', 'ἐκ', 'ἐπί', 'ὑπέρ', 'ὑπό',
          'κατά', 'μετά', 'παρά', 'περί', 'πρό', 'πρός', 'σύν']


logging.info('loading treebank')
filepath_tb = os.path.join('data', f'{sys.argv[1]}.conllu')

with open(filepath_tb, 'r') as data:
    tb = [tokenlist for tokenlist in conllu.parse_incr(data)]
logging.info(f'treebank {sys.argv[1]}.conllu loaded without errors')

res1 = 'Query 1: two tokens - adv (lemma in list) and verb (adv\'s parent)\n' \
        '         TOKEN 1: upos=ADV (head=TOKEN2)\n' \
        '         TOKEN 2: upos=VERB\n'

res2 = 'Query 2: three tokens - verb (noun\'s parent), adp, noun (adp\'s parent); noun follows, but not immediately adp\n' \
        '         TOKEN 1: upos=VERB\n' \
        '         TOKEN 2: upos=ADP (head=TOKEN3)\n' \
        '         TOKEN 3: upos=NOUN or upos=PRON, deprel is obl, obl:arg or advmod (head=TOKEN1)\n'

res3 = 'Query 3: three consecutive tokens; adp-noun-verb\n' \
        '         TOKEN 1: upos=ADP\n' \
        '         TOKEN 2: upos=NOUN or upos=PRON\n' \
        '         TOKEN 3: upos=VERB\n'

res3a = 'Query 3a: three consecutive tokens; adp-noun-verb\n' \
        '         TOKEN 1: upos=ADP\n' \
        '         TOKEN 2: upos=NOUN or upos=PRON (is not TOKEN\'s 1 head)\n' \
        '         TOKEN 3: upos=VERB\n'

res3b = 'Query 3b: three consecutive tokens; adp-noun-verb\n' \
        '         TOKEN 1: upos=ADP\n' \
        '         TOKEN 2: upos=NOUN or upos=PRON; deprel is obj or obl (head=TOKEN 3)\n' \
        '         TOKEN 3: upos=VERB\n'

res4 = 'Query 4: two tokens - lemma in list and noun or pron (lemma\'s parent)\n' \
        '         TOKEN 1: lemma in list; deprel=compound:prt (head=TOKEN 2)\n' \
        '         TOKEN 2: upos is NOUN or PRON; deprel is advcl or conj\n'


logging.info('starting checking sentences')
for sent in tb:
    for tok in sent:
        q1 = match_query1(tok, sent)
        q2 = match_query2(tok, sent)
        q3 = match_query3(tok, sent)
        q3a = match_query3b(tok, sent)
        q3b = match_query3b(tok, sent)
        q4 = match_query4(tok, sent)
        if q1:
            res1 += f'\nsent_id: {sent.metadata["sent_id"]}\n' \
                    f'{sys.argv[1]} {tok["misc"]["Ref"]}\n' \
                    f'Sentence: {sent.metadata["text"]}\n' \
                    f'ADV → {q1["preverb"]["form"]}; deprel: {q1["preverb"]["deprel"]}\n' \
                    f'VERB → {q1["verb"]["form"]}\n'
        if q2:
            res2 += f'\nsent_id: {sent.metadata["sent_id"]}\n' \
                    f'{sys.argv[1]} {tok["misc"]["Ref"]}\n' \
                    f'Sentence: {sent.metadata["text"]}\n' \
                    f'PREVERB → {q2["preverb"]["form"]}; deprel: {q2["preverb"]["deprel"]}\n' \
                    f'NOUN → {q2["noun"]["form"]}; deprel: {q2["noun"]["deprel"]}\n' \
                    f'VERB → {q2["verb"]["form"]}\n'
        if q3:
            res3 += f'\nsent_id: {sent.metadata["sent_id"]}\n' \
                    f'{sys.argv[1]} {tok["misc"]["Ref"]}\n' \
                    f'Sentence: {sent.metadata["text"]}\n' \
                    f'PREVERB → {q3["preverb"]["form"]}; deprel: {q3["preverb"]["deprel"]}\n' \
                    f'NOUN → {q3["noun"]["form"]}; deprel: {q3["noun"]["deprel"]}\n' \
                    f'VERB → {q3["verb"]["form"]}\n'
        if q3a:
            res3a += f'\nsent_id: {sent.metadata["sent_id"]}\n' \
                    f'{sys.argv[1]} {tok["misc"]["Ref"]}\n' \
                    f'Sentence: {sent.metadata["text"]}\n' \
                    f'PREVERB → {q3a["preverb"]["form"]}; deprel: {q3a["preverb"]["deprel"]}\n' \
                    f'NOUN → {q3a["noun"]["form"]}; deprel: {q3a["noun"]["deprel"]}\n' \
                    f'VERB → {q3a["verb"]["form"]}\n'
        if q3b:
            res3b += f'\nsent_id: {sent.metadata["sent_id"]}\n' \
                    f'{sys.argv[1]} {tok["misc"]["Ref"]}\n' \
                    f'Sentence: {sent.metadata["text"]}\n' \
                    f'PREVERB → {q3b["preverb"]["form"]}; deprel: {q3b["preverb"]["deprel"]}\n' \
                    f'NOUN → {q3b["noun"]["form"]}; deprel: {q3b["noun"]["deprel"]}\n' \
                    f'VERB → {q3b["verb"]["form"]}\n'
        if q4:
            res4 += f'\nsent_id: {sent.metadata["sent_id"]}\n' \
                    f'{sys.argv[1]} {tok["misc"]["Ref"]}\n' \
                    f'Sentence: {sent.metadata["text"]}\n' \
                    f'PREVERB → {q4["preverb"]["form"]}\n' \
                    f'NOUN/PRON → {q4["noun"]["form"]}; deprel: {q4["noun"]["deprel"]}\n'

logging.info('check over')

logging.info(f'saving results into files at {os.path.join("results", "ancient_greek")}')

filepath_out = os.path.join('results', 'ancient_greek', f'{sys.argv[1]}_q1.txt')
with open(filepath_out, 'w') as file:
    file.write(res1)


filepath_out = os.path.join('results', 'ancient_greek', f'{sys.argv[1]}_q2.txt')
with open(filepath_out, 'w') as file:
    file.write(res2)


filepath_out = os.path.join('results', 'ancient_greek', f'{sys.argv[1]}_q3.txt')
with open(filepath_out, 'w') as file:
    file.write(res3)


filepath_out = os.path.join('results', 'ancient_greek', f'{sys.argv[1]}_q3a.txt')
with open(filepath_out, 'w') as file:
    file.write(res3a)


filepath_out = os.path.join('results', 'ancient_greek', f'{sys.argv[1]}_q3b.txt')
with open(filepath_out, 'w') as file:
    file.write(res3b)


filepath_out = os.path.join('results', 'ancient_greek', f'{sys.argv[1]}_q4.txt')
with open(filepath_out, 'w') as file:
    file.write(res4)

logging.info(f'{sys.argv[1]}.conllu --> job done')
