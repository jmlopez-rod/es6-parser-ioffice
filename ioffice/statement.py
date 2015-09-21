"""ES6: STATEMENT NodeParser

"""

from lexor.core.parser import NodeParser
from lexor.core.elements import Element


class StatementNP(NodeParser):
    """Node parser short description. """

    def make_node(self):
        """State the type of node it returns. """
        parser = self.parser
        parser['EmptyNP'].read_empty(' ')
        node = Element('statement-node')
        node.pos = parser.copy_pos()
        return node

    def close(self, node):
        parser = self.parser
        caret = parser.caret
        if parser.text[caret] != ';':
            return None
        parser.update(caret+1)
        return parser.copy_pos()
