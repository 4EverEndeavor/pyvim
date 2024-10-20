# vim: set ft=python:
"""
Pyvim configuration. Save to file to: ~/.pyvimrc
"""
from pyvim.toolkit.application import run_in_terminal
from pyvim.toolkit.filters import ViInsertMode
from pyvim.toolkit.key_binding.key_processor import KeyPress
from pyvim.toolkit.keys import Keys
from pyvim import editor
from subprocess import call
import six

__all__ = (
    'configure',
)


def configure(editor: editor):
    """
    Configuration function. We receive a ``pyvim.editor.Editor`` instance as
    argument that we can manipulate in here.
    """
    # Show line numbers by default. (:set number)
    editor.show_line_numbers = True
    editor.relative_number = True

    # Highlight search. (:set hlsearch)
    editor.highlight_search = True

    # Case insensitive searching. (:set ignorecase)
    editor.ignore_case = True

    # Expand tab. (Pressing Tab will insert spaces.)
    editor.expand_tab = True  # (:set expandtab)
    editor.tabstop = 4  # (:set tabstop=4)

    # Scroll offset (:set scrolloff)
    editor.scroll_offset = 2

    # Show tabs and trailing whitespace. (:set list)
    editor.display_unprintable_characters = True

    # Use Jedi for autocompletion of Python files. (:set jedi)
    editor.enable_jedi = True

    # Apply colorscheme. (:colorscheme emacs)
    editor.use_colorscheme('emacs')


    # Add custom key bindings:

    @editor.add_key_binding('j', 'k', filter=ViInsertMode())
    def _(event):
        """
        Typing 'jj' in Insert mode, should go back to navigation mode.

        (imap jj <esc>)
        """
        event.cli.key_processor.feed(KeyPress(Keys.Escape))

    @editor.add_key_binding(Keys.F9)
    def save_and_execute_python_file(event):
        """
        F9: Execute the current Python file.
        """
        # Save buffer first.
        editor_buffer = editor.current_editor_buffer

        if editor_buffer is not None:
            if editor_buffer.location is None:
                editor.show_message("File doesn't have a filename. Please save first.")
                return
            else:
                editor_buffer.write()

        # Now run the Python interpreter. But use
        # `CommandLineInterface.run_in_terminal` to go to the background and
        # not destroy the window layout.
        def execute():
            call(['python3', editor_buffer.location])
            six.moves.input('Press enter to continue...')

        run_in_terminal(execute)

