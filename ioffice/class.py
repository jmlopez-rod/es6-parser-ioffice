"""ES6: CLASS NodeParser

"""

from lexor.core.parser import NodeParser
from lexor.core.elements import Element, Void


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

    def _update_class_name(self, node, token):
        node['name'] = token

    def _update_inherits(self, node, token):
        node['inherits'] = token

    def _token_is_extends(self, node):
        parser = self.parser
        parser['EmptyNP'].read_empty(' ')
        pos = parser.copy_pos()

        base_class = parser['TokenNP'].read_token()
        token, index = parser['TokenNP'].inspect_token()
        while token == '.':
            base_class += token
            parser.update(index)
            base_class += parser['TokenNP'].read_token()
            token, index = parser['TokenNP'].inspect_token()


        if base_class == '{':
            return self.error('E101', pos)

        self._update_inherits(node, base_class)
        parser['EmptyNP'].read_empty(' ')
        token = parser['TokenNP'].read_token()

        if token == '{':
            return node

        return self.error('E102', parser.pos)

    def make_node(self):
        """State the type of node it returns. """
        parser = self.parser
        token, index = parser['TokenNP'].inspect_token()
        if token != 'class':
            return None

        node = Element('class-node')
        node.pos = parser.copy_pos()
        parser.update(index)

        parser['EmptyNP'].read_empty(' ')
        token = parser['TokenNP'].read_token()

        if token == '{':
            return node

        if token == 'extends':
            return self._token_is_extends(node)

        self._update_class_name(node, token)
        parser['EmptyNP'].read_empty(' ')
        token = parser['TokenNP'].read_token()

        if token == '{':
            return node

        if token == 'extends':
            return self._token_is_extends(node)

        return self.error('E100', parser.pos, [token])

    def close(self, _):
        parser = self.parser
        caret = parser.caret
        if parser.text[caret] != '}':
            return None
        parser.update(caret+1)
        return parser.copy_pos()


MSG = {
    'E100': 'expected `extends`, found `{0}`',
    'E101': 'missing base class to inherit from',
    'E102': 'expected starting curly bracket for class body',
}
MSG_EXPLANATION = [
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

""",
]
