"""ES6: METHOD NodeParser

Node parser description.

"""

from lexor.core.parser import NodeParser
from lexor.core.elements import Element, Void, Text
from lexor.util.logging import L


class MethodNP(NodeParser):
    """Node parser short description. """

    def error(self, code, pos, arg=None):
        """Returns a node and sets the parser caret to the end of
        line so that it may stop parsing text.
        """
        self.msg(code, pos, arg)
        self.parser.update(self.parser.end)
        return Void('failed-method-node')

    def _parse_arguments(self):
        parser = self.parser
        if parser.text[parser.caret] != '(':
            return None
        index = parser.caret + 1
        char = parser.text[index]
        result = []
        buff = ""
        level = 0
        is_quoted = False
        while True:
            if char == ',' and level == 0 and not is_quoted:
                result.append(buff.strip())
                buff = ''
            else:
                if char == '(':
                    level += 1
                elif char == ')':
                    level -= 1
                    if level == -1:
                        break
                elif char in '"\'':
                    is_quoted = not is_quoted
                buff += char
            index += 1
            char = parser.text[index]
        if buff != '':
            result.append(buff.strip())
        parser.update(index + 1)
        return result

    def make_node(self):
        """State the type of node it returns. """
        parser = self.parser
        parser['EmptyNP'].read_empty()

        if parser.text[parser.caret] == '/':
            return None

        if parser.text[parser.caret] == '}':
            return Text('')

        node = Element('class-method')
        node.pos = parser.copy_pos()

        token = parser['TokenNP'].read_token()

        if token == ';':
            self.msg('W100', node.pos)
            return Text('')

        if token == 'static':
            node['static'] = True
            parser['EmptyNP'].read_empty()
            token = parser['TokenNP'].read_token()

        if token in ['*', 'get', 'set']:
            node['pre'] = token
            parser['EmptyNP'].read_empty()
            token = parser['TokenNP'].read_token()

        if token == 'constructor':
            # TODO: Make sure there is only one constructor
            node.name = 'class-constructor'
        else:
            # TODO: no repeats
            node['name'] = token

        args = self._parse_arguments()
        if args is None:
            print 'TOKEN FAIL = ', token
            return self.error('E200', parser.pos)
        print args
        parser['EmptyNP'].read_empty(' ')
        if parser.text[parser.caret] != '{':
            return self.error('E300', parser.pos)
        parser.update(parser.caret + 1)
        return node


    def close(self, node):
        parser = self.parser
        caret = parser.caret
        if parser.text[caret] != '}':
            return None
        parser.update(caret+1)
        return parser.copy_pos()


MSG = {
    'W100': 'no need for semicolon on method declaration',
    'E200': 'expected `(` to begin reading method arguments',
    'E300': 'expected `{` to begin method body',
}
MSG_EXPLANATION = [
    """
    - `(` is expected immediately after the method name.

""",
]
