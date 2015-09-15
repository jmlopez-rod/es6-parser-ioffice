"""ES6: IOFFICE parser EMPTY test

Testing suite to parse es6 empty in the ioffice style.

"""

from lexor.command.test import nose_msg_explanations


def test_empty():
    """es6.parser.ioffice.empty: MSG_EXPLANATION """
    nose_msg_explanations(
        'es6', 'parser', 'ioffice', 'empty'
    )
