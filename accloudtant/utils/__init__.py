#!/bin/env python

import io
import tokenize
import token


def fix_unquoted(generated_token, valid_tokens):
    if generated_token[1] not in valid_tokens:
        new_value = u'"%s"' % generated_token[1]
        new_token = (token.STRING, new_value)
    return new_token


def fix_single_quoted(value):
    if value.startswith("'"):
        value = u'"%s"' % value[1:-1].replace('"', '\\"')
    return value


def remove_invalid_commas(result):
    if (len(result) > 0) and (result[-1][1] == ','):
        result.pop()
    return result


def fix_lazy_json(in_text):
    """
    This function modifies JS-contained JSON to be valid.

    Posted in http://stackoverflow.com/questions/4033633/handling-lazy-json-\
            in-python-expecting-property-name by Pau Sánchez (codigomanso.com)
    """
    tokengen = tokenize.generate_tokens(io.StringIO(in_text).readline)

    valid_tokens = ['true', 'false', 'null', '-Infinity', 'Infinity', 'NaN']
    result = []
    for tokid, tokval, _, _, _ in tokengen:
        # fix unquoted strings
        if tokid == token.NAME:
            tokid, tokval = fix_unquoted((tokid, tokval), valid_tokens)

        # fix single-quoted strings
        elif tokid == token.STRING:
            tokval = fix_single_quoted(tokval)

        # remove invalid commas
        elif (tokid == token.OP) and ((tokval == '}') or (tokval == ']')):
            result = remove_invalid_commas(result)

        result.append((tokid, tokval))

    return tokenize.untokenize(result)
