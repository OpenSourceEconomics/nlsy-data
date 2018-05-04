#!/usr/bin/env python
""" This script construct the panel dataset based on the NLSY sources from the website which are in
the wide format.
"""

from clsSource import SourceCls

if __name__ == '__main__':

    fname = 'output/original.pkl'

    source_obj = SourceCls()

    source_obj.read_source()
    source_obj.transform_wide_to_panel()
    source_obj.add_basic_variables()
    source_obj.store(fname)

    source_obj.load(fname)
    source_obj.testing()
