"""ES6: IOFFICE parser METHOD test

Testing suite to parse es6 method in the ioffice style.

"""

from lexor.command.test import nose_msg_explanations


def test_method():
    """es6.parser.ioffice.method: MSG_EXPLANATION """
    nose_msg_explanations(
        'es6', 'parser', 'ioffice', 'method'
    )
