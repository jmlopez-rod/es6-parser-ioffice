"""ES6: IOFFICE parser FUNCTION test

Testing suite to parse es6 function in the ioffice style.

"""

from lexor.command.test import nose_msg_explanations


def test_function():
    """es6.parser.ioffice.function: MSG_EXPLANATION """
    nose_msg_explanations(
        'es6', 'parser', 'ioffice', 'function'
    )
