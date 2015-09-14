"""ES6: CLASS NodeParser

Node parser description.

"""

from lexor.core.parser import NodeParser
from lexor.core.elements import Element, Void


# TODO: the parsers get token function does not make distinction
# TODO: between non-space characters and operators. Once this is
# TODO: updated we may change some code in here on `read_token`.
class ClassNP(NodeParser):
    """Try parsing:

        class {}
        class extends Other {}
        class Polygon {}
        class Square extends Polygon {}

    """

    def error(self, code, pos, arg=None):
        """Returns a node  and sets the parser caret to the end of
        line so that it may stop parsing text.
        """
        self.msg(code, pos, arg)
        self.parser.update(self.parser.end)
        return Void('failed-class-node')

    def _inspect_spaces(self, spaces, same_line=False):
        if len(spaces) != 1:
            self.msg('W100', self.parser.pos, [len(spaces)])
        if same_line and spaces == '\n':
            self.msg('W101', self.parser.pos)

    def _get_next_token(self, spaces, index):
        self._inspect_spaces(spaces)
        self.parser.update(index)
        return self.parser.read_token(' \t\n\r\f\v{}')

    def _get_next_spaces(self, index):
        self.parser.update(index)
        return self.parser.read_spaces()

    def _update_class_name(self, node, token):
        node['name'] = token

    def _update_inherits(self, node, token):
        node['inherits'] = token

    def _token_is_extends(self, parser, index, node):
        spaces, index = self._get_next_spaces(index)
        if parser.text[index] == '{':
            return self.error('E101', parser.pos)
        token, index = self._get_next_token(spaces, index)
        self._update_inherits(node, token)
        spaces, index = self._get_next_spaces(index)
        if parser.text[index] == '{':
            self._inspect_spaces(spaces, True)
            parser.update(index + 1)
            return node
        parser.update(parser.caret + 1)
        return self.error('E102', parser.pos)

    def make_node(self):
        """State the type of node it returns. """
        parser = self.parser
        token, index = parser.read_token(' \t\n\r\f\v{}')
        if token != 'class':
            return None
        caret = parser.caret
        node = Element('class-node')
        node.pos = parser.copy_pos()
        parser.update(caret+5)
        spaces, index = parser.read_spaces()
        if parser.text[index] == '{':
            self._inspect_spaces(spaces, True)
            parser.update(index + 1)
            return node
        token, index = self._get_next_token(spaces, index)
        if token == 'extends':
            return self._token_is_extends(parser, index, node)
        self._update_class_name(node, token)
        spaces, index = self._get_next_spaces(index)
        if parser.text[index] == '{':
            self._inspect_spaces(spaces, True)
            parser.update(index + 1)
            return node
        token, index = self._get_next_token(spaces, index)
        if token == 'extends':
            return self._token_is_extends(parser, index, node)
        return self.error('E100', parser.pos, [token])

    def close(self, _):
        parser = self.parser
        caret = parser.caret
        if parser.text[caret] != '}':
            return None
        parser.update(caret+1)
        return parser.copy_pos()


MSG = {
    'W100': 'expected 1 space, found {0}',
    'W101': 'start curly bracket in same line as class declaration',
    'E100': 'expected `extends`, found `{0}`',
    'E101': 'missing base class to inherit from',
    'E102': 'expected starting curly bracket for class body',
}
MSG_EXPLANATION = [
    """
    - Use only one space when required.

    - Curly brackets should start in the same line as the class
      declaration.

    Okay: class {}

    W100: class{}
    W100: class  {}
    W101:
        class
        {}

""",
    """
    - To inherit from a class we use the "extends" keyword followed
      by the name of the class we wish to inherit from.

    - The general form for a class is:

        "class" BindingIdentifier? ClassHeritage? "{" ClassBody? "}"

      where ClassHeritage has the form:

        "extends" AssignmentExpression

    - NOTE: The 'AssignmentExpression' can only be a string without
            any spaces at the moment. If you try to use something
            like: `combine(MyMixin, MySuperClass)` then write it
            without spaces in the meantime:
                `combine(MyMixin,MySuperClass)`.
            When the time comes a warning will let you know that a
            space is required there.

    Okay: class Square extends Polygon {}
    Okay: class extends Base {}

    E100: class Square inherits Polygon {}
    E100: class Square [something-other-than-extends] Polygon {}

    E101: class Square extends {}

    E102: class Square extends Polygon Rectangle {}

"""
]
