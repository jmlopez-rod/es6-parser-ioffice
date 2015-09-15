"""ES6: EMPTY NodeParser"""

import re
from lexor.core.parser import NodeParser
from lexor.core.elements import Text

RE = re.compile(r'\s*\n')


class EmptyNP(NodeParser):
    """Collect empty spaces. """

    def make_node(self):
        parser = self.parser
        match = RE.match(parser.text, parser.caret)
        if match:
            data = parser.text[parser.caret:match.end()]
            parser.update(match.end())
            return Text(data)
        return None

    def close(self, _):
        pass
