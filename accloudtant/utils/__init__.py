#!/bin/env python

import io
import tokenize
import token


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
        if (tokid == token.NAME):
            if tokval not in valid_tokens:
                tokid = token.STRING
                tokval = u'"%s"' % tokval

        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith("'"):
                tokval = u'"%s"' % tokval[1:-1].replace('"', '\\"')

        # remove invalid commas
        elif (tokid == token.OP) and ((tokval == '}') or (tokval == ']')):
            if (len(result) > 0) and (result[-1][1] == ','):
                result.pop()

        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith("'"):
                tokval = u'"%s"' % tokval[1:-1].replace('"', '\\"')
        result.append((tokid, tokval))

    return tokenize.untokenize(result)
