"""ES6: COMPOUND NodeParser

Node parser description.

"""

from lexor.core.parser import NodeParser
from lexor.core.elements import Element
from lexor.util.logging import L


class CompoundNP(NodeParser):
    """Node parser short description. """

    def make_node(self):
        """State the type of node it returns. """
        parser = self.parser
        caret = parser.caret
        if parser.text[caret] != '{':
            return None
        node = Element('compound')
        # TODO: set the context of the compound statement:
        # function, object, for, while
        # L.log("PREVIOUS SIBLING: %r", parser.current_node[-1])
        node['context'] = 'TBD'
        node.pos = parser.copy_pos()
        parser.update(caret+1)
        return node

    def close(self, node):
        parser = self.parser
        caret = parser.caret
        if parser.text[caret] != '}':
            return None
        parser.update(caret+1)
        return parser.copy_pos()
