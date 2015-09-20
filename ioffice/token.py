"""ES6: EMPTY NodeParser"""

import re
from lexor.core.parser import NodeParser
from lexor.core.elements import Text


RE_EMPTY = re.compile(r'\s+')
OPERATORS = sorted([
    '{', '}', '(', ')', '[', ']', '.',
    '...', ';', ',', '<', '>', '<=',
    '>=', '==', '!=', '===', '!==',
    '+', '-', '*', '%', '++', '--',
    '<<', '>>', '>>>', '&', '|', '^',
    '!', '~', '&&', '||', '?', ':',
    '=', '+=', '-=', '*=', '%=', '<<=',
    '>>=', '>>>=', '&=', '|=', '^=', '=>',
    '/', '/='
], key=len, reverse=True)
OPERATOR_START = ''.join(set([x[0] for x in OPERATORS]))
EMPTY = ' \t\n\r\f\v'


class EmptyNP(NodeParser):
    """Collect empty spaces. """

    def read_empty(self, expect=None):
        parser = self.parser
        match = RE_EMPTY.match(parser.text, parser.caret)
        if match:
            data = match.group()
            if expect:
                if data != expect:
                    args = [repr(expect), repr(data)]
                    self.msg('W100', parser.pos, args)
            else:
                # TODO Do checks on empty spaces here.
                # TODO: indentation errors are wrong ...
                indent = data.split('\n')
                indent_level = parser.current_node.level + 1
                for space in indent:
                    if space == '':
                        continue
                    if space != ' '*indent_level*2:
                        self.msg('W200', parser.pos, [indent_level])

            parser.update(match.end())
            return data
        return None

    def make_node(self):
        data = self.read_empty()
        if data:
            return Text(data)
        return None

    def close(self, _):
        pass


class TokenNP(NodeParser):
    """Collect tokens. """

    def read_token(self):
        token, index = self.inspect_token()
        if token == '':
            return None
        self.parser.update(index)
        return token

    def inspect_token(self):
        parser = self.parser
        char = parser.text[parser.caret]
        if char in EMPTY:
            return '', parser.caret
        caret = parser.caret
        if char in OPERATOR_START:
            for opt in OPERATORS:
                if parser.text[caret:caret+len(opt)] == opt:
                    return opt, caret + len(opt)
        while char not in EMPTY and char not in OPERATOR_START:
            caret += 1
            char = parser.text[caret]
        token = parser.text[parser.caret:caret]
        return token, caret

    def make_node(self):
        raise SyntaxError('Not meant to create nodes')

    def close(self, _):
        pass


MSG = {
    'W100': 'expected {0}, found {1}',
    'W200': 'expected indentation level of {0}',
}
MSG_EXPLANATION = [
    """
    - W100 triggers a warning about conventions.

""",
]
