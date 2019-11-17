#!/usr/bin/env python

import panflute as pf
import os

def prepare(doc):
    doc.walk(find_headers)

def find_headers(elem, doc):
    if isinstance(elem, pf.Header):
        if hasattr(doc, 'highestHeaderLevel'):
            if elem.level < doc.highestHeaderLevel:
                doc.highestHeaderLevel = elem.level
        else:
            doc.highestHeaderLevel = elem.level

def action(elem, doc):
    if isinstance(elem, pf.Header):
        if hasattr(doc, 'highestHeaderLevel'):
            reduce = doc.highestHeaderLevel - 1
        elem.level = elem.level - reduce
        return elem

def finalize(doc):
    pass

def main(doc=None):
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()