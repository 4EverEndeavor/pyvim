#!/usr/bin/env python
"""
pyvim: Pure Python Vim clone.
Usage:
    pyvim [-p] [-o] [-O] [-u <pyvimrc>] [<location>...]

Options:
    -p           : Open files in tab pages.
    -o           : Split horizontally.
    -O           : Split vertically.
    -u <pyvimrc> : Use this .pyvimrc file instead.
"""
from __future__ import unicode_literals
import docopt
import os
import logging

from ..editor import Editor
from ..rc_file import run_rc_file

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
    pyvimrc = a['-u']

    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)

    # Create new editor instance.
    logger.info('Creating editor instance for locations: {}'.format(locations))
    editor = Editor()

    # Apply rc file.
    if pyvimrc:
        run_rc_file(editor, pyvimrc)
    else:
        default_pyvimrc = os.path.expanduser('~/.pyvimrc')

        if os.path.exists(default_pyvimrc):
            run_rc_file(editor, default_pyvimrc)

    # Load files and run.
    editor.load_initial_files(locations, in_tab_pages=in_tab_pages,
                              hsplit=hsplit, vsplit=vsplit)
    editor.run()


if __name__ == '__main__':
    run()
