#!/usr/bin/env python
"""This module compiles the notes with the figures."""
import subprocess
import argparse
import shutil

if __name__ == '__main__':

    parser = argparse.ArgumentParser('Create presentation')

    parser.add_argument('--update', action='store_true', dest='update',
                        help='update public slides')

    is_update = parser.parse_args().update

    for task in ['pdflatex', 'bibtex', 'pdflatex', 'pdflatex']:
        subprocess.check_call(task + ' main', shell=True)
        
    if is_update:
        shutil.copy('main.pdf', '../distribution/presentation.pdf')