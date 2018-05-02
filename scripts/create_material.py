#!/usr/bin/env python
"""This module creates all the material in support of the lectures."""
import subprocess
import shutil
import os

if __name__ == '__main__':

    for dirname in ['figures', 'notes']:
        os.chdir(dirname)
        subprocess.check_call(['python', './create.py'])
        os.chdir('../')

    shutil.copy('notes/main.pdf', 'material.pdf')
