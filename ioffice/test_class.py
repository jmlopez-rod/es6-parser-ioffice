"""ES6: IOFFICE parser CLASS test

Testing suite to parse es6 class in the ioffice style.

"""

from lexor.command.test import nose_msg_explanations


def test_class():
    """es6.parser.ioffice.class: MSG_EXPLANATION """
    nose_msg_explanations(
        'es6', 'parser', 'ioffice', 'class', {
            'newline': 'off'
        }
    )
