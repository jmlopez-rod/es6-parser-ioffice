"""ES6: IOFFICE parser COMMENT test

Testing suite to parse es6 comment in the ioffice style.

"""

from lexor.command.test import nose_msg_explanations


def test_comment():
    """es6.parser.ioffice.comment: MSG_EXPLANATION """
    nose_msg_explanations(
        'es6', 'parser', 'ioffice', 'comment', {
            'newline': 'off'
        }
    )
