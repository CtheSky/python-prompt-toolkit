from __future__ import unicode_literals
from prompt_toolkit.application.current import get_app
from prompt_toolkit.eventloop.context import TaskLocal, TaskLocalNotSetError
from prompt_toolkit.utils import is_windows
import sys

__all__ = [
    'create_input',
    'get_default_input',
]


def create_input(stdin=None):
    stdin = stdin or sys.stdin

    if is_windows():
        from .win32 import Win32Input
        return Win32Input(stdin)
    else:
        from .vt100 import Vt100Input
        return Vt100Input(stdin)


_default_input = TaskLocal()


def get_default_input():
    """
    Get the input class to be used by default.

    Called when creating a new Application(), when no `Input` has been passed.
    """
    # If an application is running, take the input from there. (This is
    # important for the "ENTER for continue" prompts after executing system
    # commands and displaying readline-style completions.)
    app = get_app(return_none=True)
    if app:
        return app.input

    # Other create/return the default input.
    try:
        value = _default_input.get()
    except TaskLocalNotSetError:
        return create_input()
    else:
        return value
