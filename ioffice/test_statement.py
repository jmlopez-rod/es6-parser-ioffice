"""ES6: IOFFICE parser STATEMENT test

Testing suite to parse es6 statement in the ioffice style.

"""

from lexor.command.test import nose_msg_explanations


def test_statement():
    """es6.parser.ioffice.statement: MSG_EXPLANATION """
    nose_msg_explanations(
        'es6', 'parser', 'ioffice', 'statement'
    )
