#!/usr/bin/env python
"""This module creates all available figures and then provides them in a compiled document for
review.
"""
import subprocess
import glob


def create_figures():
    """This function creates all the figures that are available in this
    subdirectory."""
    for fname in glob.glob('fig-*.py'):
        subprocess.check_call(['python', './' + fname])


if __name__ == '__main__':

    create_figures()
