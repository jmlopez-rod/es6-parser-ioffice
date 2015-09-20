"""ES6: FUNCTION NodeParser

"""

from lexor.core.parser import NodeParser
from lexor.core.elements import Element, Void


class FunctionNP(NodeParser):
    """Node parser short description. """

    def error(self, code, pos, arg=None):
        """Returns a node and sets the parser caret to the end of
        line so that it may stop parsing text.
        """
        self.msg(code, pos, arg)
        self.parser.update(self.parser.end)
        return Void('failed-function-node')

    def _read_parameters(self):
        parser = self.parser
        params = {}
        order = []
        expects = 'param'
        while True:
            # TODO: tell EmptyNP that we are parsing parameters
            parser['EmptyNP'].read_empty()
            token = parser['TokenNP'].read_token()
            if token == ')':
                break
            if expects == 'param':
                if token == ',':
                    # TODO: handle the error
                    exit(1)
                order.append(token)
                params[token] = ''
                expects = 'operator'
            elif expects == 'default':
                if token in [',', '=']:
                    # TODO: handle error
                    exit(1)
                params[order[-1]] = token
                expects = ','
            else:
                if token == '=':
                    expects = 'default'
                elif token != ',':
                    # TODO: handle the error
                    exit(1)
                else:
                    expects = 'param'
        return order, [params[x] for x in order]

    def make_node(self):
        """State the type of node it returns. """
        parser = self.parser
        token, index = parser['TokenNP'].inspect_token()
        if token != 'function':
            return None

        node = Element('function-node')
        node.pos = parser.copy_pos()
        parser.update(index)

        parser['EmptyNP'].read_empty(' ')
        token = parser['TokenNP'].read_token()

        if token == '(':
            params, defaults = self._read_parameters()
            node['params'] = params
            node['defaults'] = defaults
        else:
            node['name'] = token
            token = parser['TokenNP'].read_token()
            if token != '(':
                return self.error('E200', parser.pos)
            params, defaults = self._read_parameters()
            node['params'] = params
            node['defaults'] = defaults

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
    'E200': 'expected `(` to begin reading method arguments',
    'E300': 'expected `{{` to begin function body',
}
MSG_EXPLANATION = [
    """
    - `(` is expected immediately after the method name.

""",
]
