"""ES6: IOFFICE Parsing Style

Parser description.

Defaults:

    - newline: Checks end of file for the newline character.
    - todo: Checks inline and block comments for the keyword TODO and
            reports it.

"""

from lexor import init, load_aux

DEFAULTS = {
    'newline': 'on',  # make sure it is off when running tests
    'todo': 'on',
    'doc-parser-lang': 'lexor',
    'doc-parser-style': '_',
}
INFO = init(
    version=(0, 0, 0, 'alpha', 0),
    lang='es6',
    type='parser',
    description='Parse es6 files. ',
    git={
        'host': 'github',
        'user': 'jmlopez-rod',
        'repo': 'es6-parser-ioffice'
    },
    author={
        'name': 'Manuel Lopez',
        'email': 'jmlopez.rod@gmail.com'
    },
    docs='http://jmlopez-rod.github.io/lexor-lang/es6-parser-ioffice',
    license='BSD License',
    path=__file__
)
MOD = load_aux(INFO)
REPOSITORY = [
    MOD['comment'].CommentNP,
    MOD['class'].ClassNP,
    MOD['compound'].CompoundNP,
    MOD['method'].MethodNP,
    MOD['token'].EmptyNP,
    MOD['token'].TokenNP,
    MOD['function'].FunctionNP,
    MOD['statement'].StatementNP,
]
MAPPING = {
    '__default__': (
        '/{}', [
            'EmptyNP',
            'CommentNP',
            'ClassNP',
            'FunctionNP',
            'CompoundNP',
            'StatementNP',
        ]
    ),
    '#document': (
        '/{};', [
            'EmptyNP',
            'CommentNP',
            'ClassNP',
            'FunctionNP',
            'CompoundNP',
            'StatementNP',
        ]
    ),
    'class-node': (
        '/}', [
            'MethodNP',
            'CommentNP',
        ]
    ),
    'statement-node': (
        ';/{}=', [
            'EmptyNP',
            'CommentNP',
            'ClassNP',
            'FunctionNP',
            'CompoundNP',
        ]
    ),
}


def post_process(parser):
    """Here we issue the warning about the new line at the end of
    the file. """
    if parser.defaults['newline'] in ['on', 'true', 'True']:
        if parser.caret != 0 and parser.text[parser.caret-1] != '\n':
            parser.msg(__name__, 'W101', parser.pos)


MSG = {
    'W101': 'no newline at end of file',
}
MSG_EXPLANATION = [
    """
    - End your document with the newline character.

    Reports W101.

""",
]
