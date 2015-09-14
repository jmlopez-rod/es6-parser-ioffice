"""ES6: IOFFICE parser COMPOUND test

Testing suite to parse es6 compound in the ioffice style.

"""

from lexor.command.test import nose_msg_explanations


def test_compound():
    """es6.parser.ioffice.compound: MSG_EXPLANATION """
    nose_msg_explanations(
        'es6', 'parser', 'ioffice', 'compound'
    )
