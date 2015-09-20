"""ES6: IOFFICE parser TOKEN test

Testing suite to parse es6 token in the ioffice style.

"""

from lexor.command.test import nose_msg_explanations


def test_token():
    """es6.parser.ioffice.token: MSG_EXPLANATION """
    nose_msg_explanations(
        'es6', 'parser', 'ioffice', 'token'
    )
