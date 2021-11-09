import conllu
import query_conllu
import sys
import logging
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")

lemmas_grc = ['ἀμφί', 'ἀνά', 'ἀντί', 'ἀπό', 'διά', 'ἐν', 'εἰς', 'ἐκ', 'ἐπί', 'ὑπέρ', 'ὑπό', 'κατά', 'μετά', 'παρά',
              'περί', 'πρό', 'πρός', 'σύν']

lemmas_san = ['apa', 'ava', 'ā', 'ud', 'ni', 'nis', 'parā', 'puras', 'pra', 'sam', 'vi', 'achā', 'ati', 'adhi', 'anu',
              'antar', 'api', 'abhi', 'upa', 'tiras', 'paras', 'pari', 'puras', 'purā', 'prati']


def match_query_grc(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
    """
    Function that takes as arguments a token and a sentence and returns a dictionary containing the matched elements

    QUERY:
    two tokens - lemma in list and noun or pron (lemma's parent):
                TOKEN 1: lemma in list; deprel=compound:prt (head=TOKEN 2)
                TOKEN 2: upos is NOUN or PRON; deprel is advcl or conj

    :param tok: token in the sentence
    :param sent: conllu sentence
    :return: an empty dictionary if the token is not involved in a pattern matching the query, otherwise a dictionary with the matched tokens
    """
    if not query_conllu.is_bounded(tok, sent) and tok['lemma'] in lemmas_grc and query_conllu.match_conditions(tok, deprel='compound:prt'):
        parent = query_conllu.get_parent(tok, sent)
        if query_conllu.match_conditions(parent, upos=['NOUN', 'PRON'], deprel=['conj', 'advcl']):
            return {'preverb': tok, 'noun': parent, 'verb': None, 'sentence': sent}
        else:
            return {}
    else:
        return {}


def match_query_san(tok: conllu.models.Token, sent: conllu.models.TokenList) -> dict:
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
    if tok['lemma'] in lemmas_san:
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


def process_tb(tb: list, name: str) -> str:
    grc = name in ['iliad', 'odyssey']
    if grc:
        match_query = match_query_grc
        res = 'Query: two tokens - lemma in list and noun or pron (lemma\'s parent)\n' \
              '       TOKEN 1: lemma in list; deprel=compound:prt (head=TOKEN 2)\n' \
              '       TOKEN 2: upos is NOUN or PRON; deprel is advcl or conj\n'
    else:
        match_query = match_query_san
        res = 'Query: preverb and any token (finite verb); verb is preverb\'s parent\n' \
              '       TOKEN 1: lemma in the list; deprel=orphan\n' \
              '       TOKEN 2: upos=any and VerbForm field empty\n'

    logging.info('starting checking sentences')
    for sent in tb:
        for tok in sent:
            q = match_query(tok, sent)
            if q:
                if grc:
                    res += f'\nsent_id: {sent.metadata["sent_id"]}\n' \
                           f'{name} {tok["misc"]["Ref"]}\n' \
                           f'Sentence: {sent.metadata["text"]}\n' \
                           f'PREVERB → {q["preverb"]["form"]}\n' \
                           f'NOUN/PRON → {q["noun"]["form"]}; deprel: {q["noun"]["deprel"]}\n'
                else:
                    res += f'\nsent_id: {q["sentence"].metadata["sent_id"]}\n' \
                           f'Sentence: {q["sentence"].metadata["text"]}\n' \
                           f'PREVERB → {q["preverb"]["form"]}; deprel: {q["preverb"]["deprel"]}\n' \
                           f'OTHER TOKEN → {q["verb"]["form"]}; pos: {q["verb"]["upos"]}\n'
    logging.info('check over')
    return res


if __name__ == '__main__':
    for name in sys.argv[1:]:
        data_path = os.path.join('data')
        conllu_files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f)) and f.endswith('.conllu')]
        if name + '.conllu' not in conllu_files:
            logging.info(f'{name}.conllu does not exist in {data_path}')
        else:
            logging.info('loading treebank')
            filepath_tb = os.path.join('data', f'{name}.conllu')

            with open(filepath_tb, 'r') as data:
                tb = [tokenlist for tokenlist in conllu.parse_incr(data)]
            logging.info(f'treebank {name}.conllu loaded without errors')

            res = process_tb(tb, name)

            logging.info(f'saving results into files at {os.path.join("results")}')

            filepath_out = os.path.join('results', f'{name}_results.txt')
            with open(filepath_out, 'w') as file:
                file.write(res)

            logging.info(f'{name}.conllu --> job done')
