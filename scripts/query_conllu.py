import conllu
import typing
import logging


class OutOfBoundaries(Exception):
    pass


class NotInSentence(Exception):
    pass


def get_node(token: conllu.models.Token, sent: conllu.models.TokenList) -> conllu.models.TokenTree:
    """
    A function that takes a sentence and one of its tokens as arguments and returns the TokenTree object corresponding to the given token

    :param token: a token in a conllu sentence
    :param sent: a conllu sentence
    :return: the TokenTree object
    """
    try:
        if token not in sent:
            raise NotInSentence
        tree = sent.to_tree()
        nodes = [tree]
        while nodes:
            for c in nodes[0].children:
                if c.token == token:
                    return c
                else:
                    nodes += nodes[0].children
                    nodes.remove(nodes[0])
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')


def get_parent(token: conllu.models.Token, sent: conllu.models.TokenList) -> typing.Union[conllu.models.Token, None]:
    """
    A function that takes a sentence and one of its tokens and returns the parent of the given token in the syntax tree

    :param token: a token in a conllu sentence
    :param sent: a conllu sentence
    :return: the parent of the given token in the sentence, None if the token is the root of the sentence or has no head; raise an error if the token is not in the sentence
    """
    try:
        if token not in sent:
            raise NotInSentence
        if not token['head']:
            return None
        elif token['head'] <= 0:
            return None
        else:
            for t in sent:
                if t['id'] == token['head']:
                    return t
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')


def get_children(token: conllu.models.Token, sent: conllu.models.TokenList) -> list:
    """
    A function that takes a sentence and one of its tokens and returns the list of tokens that have the token passed as argument as head of the relation

    :param token: a token in a conllu sentence
    :param sent: a conllu sentence
    :return: the list of siblings
    """
    try:
        if token not in sent:
            raise NotInSentence
        children = []
        for t in sent:
            if t['head'] == token['id']:
                children.append(t)
        return children
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')


def get_siblings(token: conllu.models.Token, sent: conllu.models.TokenList) -> list:
    """
    A function that takes a sentence and one of its tokens and returns the list of tokens that are siblings of the token passed as argument, i.e. the tokens that share the same parent

    :param token: a token in a conllu sentence
    :param sent: a conllu sentence
    :return: the list of siblings
    """
    try:
        if token not in sent:
            raise NotInSentence
        siblings = []
        if not token['head']:
            pass
        elif token['head'] <= 0:
            pass
        else:
            for t in sent:
                if t['head'] == token['head']:
                    siblings.append(t)
        return siblings
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')


def get_ancestors(token: conllu.models.Token, sent: conllu.models.TokenList) -> list:
    """
    A function that takes a sentence and one of its tokens and returns the list of ancestors of the given token, i.e. the walk from the token passed as argument to the root of the tree

    :param token: a token in a conllu sentence
    :param sent: a conllu sentence
    :return: the list of ancestors
    """
    try:
        if token not in sent:
            raise NotInSentence
        ancestors = []
        t = token
        parent = get_parent(t, sent)
        while parent:
            ancestors.append(parent)
            t = parent
            parent = get_parent(t, sent)
        return ancestors
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')


def get_descendants(token: conllu.models.Token, sent: conllu.models.TokenList, tok_obj=True) -> list:
    """
    A function that takes a sentence and one of its tokens and returns the list of descendants of the given token, i.e. the list of nodes in the subtree generated from the token passed as argument

    :param token: a token in a conllu sentence
    :param sent: a conllu sentence
    :param tok_obj: if true returns a list of Token objects, otherwise a list of TokenTree objects (default: True)
    :return: the list of descendants
    """
    try:
        if token not in sent:
            raise NotInSentence
        node = get_node(token, sent)
        descendants = node.children.copy()
        i = 0
        while i < len(descendants):
            if descendants[i].children:
                descendants += descendants[i].children
            i += 1
        if tok_obj:
            return [d.token for d in descendants]
        else:
            return descendants
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')


def is_multiword(token: conllu.models.Token) -> bool:
    """
    Function telling if the token passed as argument is a multiword token

    :param token: the token in a conllu sentence
    :return: True or False
    """
    if type(token['id']) is tuple:
        return True
    else:
        return False


def is_bounded(token: conllu.models.Token, sent: conllu.models.TokenList) -> bool:
    """
    Function telling if the token passed as argument is the result of the split of a multiword token

    :param token: a token in a conllu sentence
    :param sent: a conllu sentence
    :return: True or False
    """
    try:
        if token not in sent:
            raise NotInSentence
        i = sent.index(token)
        position = token['id']
        if is_multiword(token):
            return True
        for i in range(i-1, -1, -1):
            if type(sent[i]['id']) is tuple:
                bond = sent[i]['id']
                if bond[0] <= position <= bond[2]:
                    return True
        return False
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')


def match_conditions(token: conllu.models.Token, **conditions) -> bool:
    """
    A function telling if the token passed as argument matches the conditions passed as **kwargs

    :param token: a token from a conllu sentence
    :param conditions: pairs in the form of parameter=value or in the form of parameter=[value1, value2, ..., value_n];
    in the former case, the function returns False if the value of the parameter specified does not match the value of the same parameter in the token (or if the token does not have such parameter),
    in the latter case, the function returns False if none of the values in the list of the parameter specified does not match the value of the same parameter in the token (or if the token does not have such parameter)
    :return: True or False
    """
    if not token:
        return False
    for key in conditions:
        if key in token:
            if type(conditions[key]) is str:
                if token[key] != conditions[key]:
                    return False
            elif type(conditions[key]) is list:
                if token[key] not in conditions[key]:
                    return False
            else:
                return False
        elif token['feats']:
            if key in token['feats']:
                if type(conditions[key]) is str:
                    if token['feats'][key] != conditions[key]:
                        return False
                elif type(conditions[key]) is list:
                    if token['feats'][key] not in conditions[key]:
                        return False
                else:
                    return False
            else:
                return False
        elif token['misc']:
            if type(conditions[key]) is str:
                if token['misc'][key] != conditions[key]:
                    return False
            elif type(conditions[key]) is list:
                if token['misc'][key] not in conditions[key]:
                    return False
            else:
                return False
        else:
            return False
    return True


def len_sent(sent: conllu.models.TokenList, tokenized=True) -> int:
    """
    Function returning the length of a conllu sentence

    :param sent: the conllu sentence
    :param tokenized: if set to True, consider in the count the result of the split of multiword tokens, otherwise it consider the original sentence (default: True)
    :return: the length of the sentence
    """
    c_tok = 0
    c = 0
    for t in sent:
        if is_multiword(t):
            c += 1
        elif is_bounded(t, sent):
            c_tok += 1
        else:
            c += 1
            c_tok += 1
    if tokenized:
        return c_tok
    else:
        return c


def move_right(token: conllu.models.Token, sent: conllu.models.TokenList, tokenized=True) -> conllu.models.Token:
    """
    Function that returns the following token in the sentence

    :param token: a token in a conllu sentence
    :param sent: the conllu sentence
    :param tokenized: if set to True, considers as elements of the sentence the result of the tokenization and the split of the multiword tokens, otherwise it considers as elements the original words (default: True)
    :return: a Token object, None if the starting token is the last one in the sentence
    """
    try:
        if token not in sent:
            raise NotInSentence
        i = sent.index(token)
        if tokenized:
            if type(token['id']) is int:
                start_id = token['id']
                for j in range(i, len(sent)):
                    if sent[j]['id'] == start_id + 1:
                        return sent[j]
                raise OutOfBoundaries
            else:
                raise TypeError
        else:
            if type(token['id']) is tuple:
                start_id = token['id'][2]
            elif type(token['id']) is int and not is_bounded(token, sent):
                start_id = token['id']
            else:
                raise TypeError
            for j in range(i, len(sent)):
                if type(sent[j]['id']) is tuple and sent[j]['id'][0] == start_id + 1:
                    return sent[j]
                elif type(sent[j]['id']) is int and not is_bounded(sent[j], sent) and sent[j]['id'] == start_id + 1:
                    return sent[j]
                else:
                    pass
            raise OutOfBoundaries
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')
    except TypeError:
        logging.debug(f' Error type: try to change the value of the parameter \'tokenized\'')
    except OutOfBoundaries:
        pass


def move_left(token: conllu.models.Token, sent: conllu.models.TokenList, tokenized=True) -> conllu.models.Token:
    """
    Function that returns the preceding token in the sentence

    :param token: a token in a conllu sentence
    :param sent: the conllu sentence
    :param tokenized: if set to True, considers as elements of the sentence the result of the tokenization and the split of the multiword tokens, otherwise it considers as elements the original words (default: True)
    :return: a Token object, None if the starting token is the first one in the sentence
    """
    try:
        if token not in sent:
            raise NotInSentence
        i = sent.index(token)
        if tokenized:
            if type(token['id']) is int:
                start_id = token['id']
                for j in range(i-1, -1, -1):
                    if sent[j]['id'] == start_id - 1:
                        return sent[j]
                raise OutOfBoundaries
            else:
                raise TypeError
        else:
            if type(token['id']) is tuple:
                start_id = token['id'][0]
            elif type(token['id']) is int and not is_bounded(token, sent):
                start_id = token['id']
            else:
                raise TypeError
            for j in range(i, len(sent)):
                if type(sent[j]['id']) is tuple and sent[j]['id'][2] == start_id - 1:
                    return sent[j]
                elif type(sent[j]['id']) is int and not is_bounded(sent[j], sent) and sent[j]['id'] == start_id - 1:
                    return sent[j]
                else:
                    pass
            raise OutOfBoundaries
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')
    except TypeError:
        logging.debug(f' Error type: try to change the value of the parameter \'tokenized\'')
    except OutOfBoundaries:
        pass


def move_from_token(token: conllu.models.Token, sent: conllu.models.TokenList, distance: int, tokenized=True) -> typing.Union[conllu.models.Token, None]:
    """
    Function that returns the token in the sentence whose position relative to the token passed as argument is specified in the 'distance' parameter

    :param token: a token in a conllu sentence
    :param sent: the conllu sentence
    :param distance: the distance from the token (if negative moves left in the sentence, otherwise moves right in the sentence)
    :param tokenized: if set to True, considers as elements of the sentence the result of the tokenization and the split of the multiword tokens, otherwise it considers as elements the original words (default: True)
    :return: a Token object
    """
    try:
        if token not in sent:
            raise NotInSentence
        if distance == 0:
            return token
        elif distance > 0:
            c = 0
            t = token
            while c < distance:
                if move_right(t, sent, tokenized):
                    t = move_right(t, sent, tokenized)
                    c += 1
                else:
                    return None
            return t
        else:
            c = 0
            t = token
            while c > distance:
                if move_left(t, sent, tokenized):
                    t = move_left(t, sent, tokenized)
                    c -= 1
                else:
                    return None
            return t
    except NotInSentence:
        logging.debug(f' {token} not in {sent}')
