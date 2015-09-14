"""ES6: COMMENT NodeParser

Parses all the comments in an es6 file.

"""

from lexor import core
from lexor.core.parser import NodeParser
from lexor.core.elements import Element, Comment, Text


class CommentNP(NodeParser):
    """Node parser short description. """

    def __init__(self, parser):
        NodeParser.__init__(self, parser)
        lang = parser.defaults['doc-parser-lang']
        style = parser.defaults['doc-parser-style']
        self.parser_name = '%s.parser.%s' % (lang, style)
        self.lexor_parser = core.Parser(lang, style)
        try:
            self.lexor_parser.load_node_parsers()
        except ImportError:
            self.lexor_parser = None
        self.indentation = 0
        self.line_start = 0

    def _check_doc_comment_lines(self, parser, lines):
        """Obtain the documentation and report if the lines are valid.
        """
        misaligned = []
        doc_string = ''
        for num, line in enumerate(lines):
            try:
                ignored, info = line.split('*', 1)
            except ValueError:
                ignored = ''
                info = line
                self.msg('E320', [self.line_start + num, 1])
            if ignored.strip() != '':
                self.msg('W302', [self.line_start + num, 1])
            if len(ignored) != self.indentation:
                misaligned.append(self.line_start + num)
            if info:
                if info.startswith(' '):
                    info = info[1:]
                else:
                    self.msg(
                        'W303',
                        [self.line_start + num, len(ignored) + 1]
                    )
            doc_string += info + '\n'
        if misaligned:
            self.msg('E330', parser.pos, [str(misaligned)])
        return misaligned, doc_string

    def _create_node(self, parser, end_index, misaligned, doc_string):
        """Parse the doc_string and return the node. """
        node = Element('doc-comment')
        if self.lexor_parser and not misaligned:
            self.lexor_parser.parse(doc_string)
            node['parsed'] = 'true'
            node.extend_children(self.lexor_parser.document)
            if self.lexor_parser.log:
                parser.update_log(
                    self.lexor_parser.log,
                    delta=[self.line_start - 1, self.indentation + 2]
                )
        else:
            if not misaligned:
                self.msg('E404', parser.pos, [self.parser_name])
            node['parsed'] = 'false'
            node.append_child(Text(doc_string))
        parser.update(end_index)
        return [node]

    def _doc_comment(self, parser, caret):
        """Doc comments begin with the sequence `/**` and end with
        `*/`. The doc comment must have the following form:

            /**
             * Content begins after `*` and must be separated by one
             * space.
             *
             * The contents in each doc comment is should be a valid
             * lexor file.
             */

        """
        index = parser.text.find('*/', caret+3)
        if index == -1:
            self.msg('E300', parser.pos)
            index = parser.end
            end_index = index
        else:
            end_index = index + 2
        content = parser.text[caret+3:index]
        # Collecting main information on doc comment structure
        self.line_start = parser.pos[0] + 1
        self.indentation = parser.pos[1]
        lines = content.split('\n')
        first_line = lines[0]
        last_line = lines[-1]
        lines = lines[1:-1]
        # Checking first line
        if first_line.strip() != '':
            self.msg('W300', parser.pos, [first_line.strip()])
        # Checking lines
        misaligned, doc_string = self._check_doc_comment_lines(
            parser, lines
        )
        # last line should be empty
        if last_line.strip() != '':
            self.msg('W301', parser.compute(end_index))
        if len(last_line) != self.indentation:
            self.msg('E310',
                     parser.compute(end_index - 2),
                     [self.indentation, len(last_line)])
        return self._create_node(
            parser, end_index, misaligned, doc_string
        )

    def _block_comment(self, parser, caret):
        """Block comments begin with the sequence `/*` and end with
        `*/`.
        """
        index = parser.text.find('*/', caret+2)
        if index == -1:
            self.msg('E200', parser.pos)
            index = parser.end
            end_index = index
        else:
            end_index = index + 2
        content = parser.text[caret+2:index]
        if parser.defaults['todo'] in ['true', 'on']:
            if 'todo' in content or 'TODO' in content:
                self.msg('W500', parser.pos)
        parser.update(end_index)
        return Comment(content)

    def _inline_comment(self, parser, caret):
        """Inline comments begin with `//` and end at the end of
        the line. Here we also expose the restriction that there
        must be at least 2 spaces before we start the comment and
        only one space between the start of the comment and its
        content.
        """
        # Two spaces between statement and comment
        prev = parser.text[max(caret-2, 0):caret]
        if len(prev) == 2 and prev[1] != '\n':
            if prev[1] != ' ' or prev[0] not in [' ', '\n']:
                self.msg('W100', parser.pos)
        elif len(prev) == 1 and prev[0] != ' ':
            self.msg('W100', parser.pos)
        index = parser.text.find('\n', caret+2)
        if index == -1:
            index = parser.end
        content = parser.text[caret+2:index]
        # Require single space after comment
        if not content.startswith(' '):
            self.msg('W101', parser.compute(caret+2))
        else:
            content = content[1:]
        if parser.defaults['todo'] in ['true', 'on']:
            if 'todo' in content or 'TODO' in content:
                self.msg('W500', parser.pos)
        parser.update(index)
        return Comment(content)

    def make_node(self):
        parser = self.parser
        caret = parser.caret
        if parser.text[caret:caret+3] == '/**':
            return self._doc_comment(parser, caret)
        elif parser.text[caret:caret+2] == '/*':
            comment = self._block_comment(parser, caret)
            comment.comment_type = 'block'
            return comment
        elif parser.text[caret:caret+2] == '//':
            comment = self._inline_comment(parser, caret)
            comment.comment_type = 'inline'
            return comment
        return None

    def close(self, _):
        pass


MSG = {
    'W100': 'missing at least two spaces before inline comment',
    'W101': 'missing single space after inline comment sequence',
    'W300': 'ignoring `{0}` at start of documentation comment',
    'W301': 'doc comment closing delimiter line has content',
    'W303': 'missing space between `*` and content',
    'W500': 'TODO comment found',
    'E200': 'block comment closing delimiter not found',
    'E300': 'documentation comment closing delimiter not found',
    'E310': 'expected indentation of {0} spaces, found {1}',
    'E320': 'doc comment is missing string `*`',
    'E330': 'misaligned `*` in documentation comment at lines {0}',
    'E404': 'unable to find `{0}` to parse documentation string',
}
MSG_EXPLANATION = [
    """
    - Inline comments should be separated by at least two spaces from
      a statement.

    Okay: x += 2;  // Compensate for border
    Okay: x += 2;    // Compensate for border

    W100: x += 2;// Compensate for border
    W100: x += 2; // Compensate for border

""",
    """
    - Inline comments should start with the sequence `//` and a
      single space.

    Okay: x += 2;  // Compensate for border

    W101: x += 2;  //Compensate for border

""",
    """
    - Block comments end when the sequence `*/` is first encountered.

    Okay: /* block comment */

    E200: /* block comment
    E200: /* block comment * /

""",
    """
    - Documentation comments end when the sequence `*/` is
      first encountered.

    Okay:
        /**
         * Documentation comment.
         */

    E300:
        /**
         * Documentation comment.
         * /

""",
    """
    - Documentation comments begin at the line following the sequence
      `/**`. Anything else written in the line containing the starting
      sequence will be ignored and a warning will be issued.


    Okay:
        /**
         * Documentation comment.
         */

    W300:
        /** This message will be ignored.
         * Documentation comment.
         */
""",
    """
    - Documentation comments should end with a line containing
      only the sequence `*/`.

    - Content on the same line before `*/` will be ignored.


    Okay:
        /**
         * Documentation comment.
         */

    W301:
        /**
         * Documentation comment. */
    W301:
        /**
         * Documentation comment.
        **/

""",
    """
    - Each line of a documentation comment begins with `*` so that
      it aligns with the first `*` in the starting sequence `/**`.

    - A space must follow each `*`.

    Okay:
        /**
         * Documentation comment.
         */

    E320:
        /**
          Documentation comment.
         */

    E330:
        /**
          * Documentation comment.
          */

    W303:
        /**
          *Documentation comment.
          */
""",
    """
    - A valid parser style is required to parse documentation
      comments. To fix this try installing a parser by executing:

          lexor install <parser-name>

      for instance:

          lexor install lexor.parser.default

    Reports E404

""",
    """
    - A comment containing the keywords 'todo' or 'TODO' will raise
      the warning code E500.

    - You may disable this warning by setting the style default
      `todo` to 'off'.

    - NOTE: documentation comments do not perform this check.

"""
]
