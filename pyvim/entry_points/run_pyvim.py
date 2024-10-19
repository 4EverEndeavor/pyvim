#!/usr/bin/env python
"""
pyvim: Pure Python Vim clone.
Usage:
    pyvim [-p] [-o] [-O] [-u <alternate_pyvimrc_file>] [<location>...]

Options:
    -p           : Open files in tab pages.
    -o           : Split horizontally.
    -O           : Split vertically.
    -u <alternate_pyvimrc_file> : Use this .alternate_pyvimrc_file file instead.
"""
from __future__ import unicode_literals
import docopt
import os
import logging

from ..editor import Editor
from ..rc_file import run_rc_file
from .. import pyvimrc

__all__ = (
    'run',
)

logger = logging.getLogger(__name__)


def run():
    breakpoint()
    a = docopt.docopt(__doc__)
    locations = a['<location>']
    in_tab_pages = a['-p']
    hsplit = a['-o']
    vsplit = a['-O']
    alternate_pyvimrc_file = a['-u']

    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)

    # Create new editor instance.
    logger.info('Creating editor instance for locations: {}'.format(locations))
    editor = Editor()

    # Apply rc file.
    if alternate_pyvimrc_file:
        run_rc_file(editor, alternate_pyvimrc_file)
    else:
        # default_pyvimrc = os.path.expanduser('~/.pyvimrc')
        # default_pyvimrc = os.path.expanduser('~/.pyvimrc')
        # if os.path.exists(default_pyvimrc):
        # run_rc_file(editor, default_pyvimrc)
        pyvimrc.configure(editor)

    # Load files and run.
    editor.load_initial_files(locations, in_tab_pages=in_tab_pages,
                              hsplit=hsplit, vsplit=vsplit)
    editor.run()


if __name__ == '__main__':
    run()
