"""
Need to install pkg prompt_toolkit
First time need to enter command from terminal:
pip install prompt_toolkit
"""

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings

cmd = WordCompleter(
    [
        "add",
        "add_note",
        "view_all",
        "search",
        "update",
        "delete",
        "reset",
        "file_sort",
        "exit",
    ],
    ignore_case=True,
)


kb = KeyBindings()


@kb.add("c-space")
def _(event):

    # Start auto completion. If the menu is showing already, select the next completion
    b = event.app.current_buffer

    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


def autocomplete():
    text: str = prompt("Type cmd: ", completer=cmd,
                       complete_while_typing=True, key_bindings=kb)
    # print("CMD is: %s" % text)
    return text


if __name__ == "__main__":
    autocomplete()
