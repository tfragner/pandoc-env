#!/usr/bin/env python

import panflute as pf
import os
import yaml
from collections import OrderedDict

home = os.environ['HOME']

def prepare(doc):
    meta = doc.get_metadata()
    type = meta['document-type']

def action(elem, doc):
    pass

def include_type_frontmatter(doc, type):
    file = home + '/.pandoc/includes/types/' + type + '.yml'
    with open(file, encoding="utf-8") as f:
        raw = f.read()
        new_metadata = yaml.load(raw, Loader=yaml.FullLoader)
        new_metadata = OrderedDict(new_metadata)
        new_metadata.update(doc.get_metadata())
        doc.metadata = new_metadata

def include_format_frontmatter(doc, format):
    file = home + '/.pandoc/includes/formats/' + format + '.yml'
    with open(file, encoding="utf-8") as f:
        raw = f.read()
        new_metadata = yaml.load(raw, Loader=yaml.FullLoader)
        new_metadata = OrderedDict(new_metadata)
        new_metadata.update(doc.get_metadata())
        doc.metadata = new_metadata

def include_global_frontmatter(doc):
    file = home + '/.pandoc/includes/global.yml'
    with open(file, encoding="utf-8") as f:
        raw = f.read()
        new_metadata = yaml.load(raw, Loader=yaml.FullLoader)
        new_metadata = OrderedDict(new_metadata)
        new_metadata.update(doc.get_metadata())
        doc.metadata = new_metadata

def get_document_type(doc):
    meta = doc.get_metadata()
    if 'document-type' in meta:
        return meta['document-type']

def get_document_format(doc, type):
    meta = doc.get_metadata()
    file = home + '/.pandoc/includes/types/' + type + '.yml'
    with open(file, encoding="utf-8") as f:
        raw = f.read()
        new_metadata = yaml.load(raw, Loader=yaml.FullLoader)
        new_metadata = OrderedDict(new_metadata)
        new_metadata.update(doc.get_metadata())
        return new_metadata['document-format']

def combine_filters(doc, format):
    meta = doc.get_metadata()
    panflute_filters = []
    filter_sequence_before_content = [
        'panflute-filters-global-before',
        'panflute-filters-format-before',
        'panflute-filters-type-before',
    ]

    for elem in filter_sequence_before_content:
        if elem in meta:
            panflute_filters.extend(meta[elem])

    if format == 'collection':
        panflute_filters.extend(meta['panflute-filters-type-include-for-collection'])
    elif format == 'single':
        panflute_filters.extend(meta['panflute-filters-type-include-for-single'])
    elif format == 'content':
        panflute_filters.extend(meta['panflute-filters-type-include-for-content'])
    
    filter_sequence_after_content = [
        'panflute-filters-type-after',
        'panflute-filters-format-after',
        'panflute-filters-global-after',
    ]

    for elem in filter_sequence_after_content:
        if elem in meta:
            panflute_filters.extend(meta[elem])

    if 'panflute-filters-type-after-all' in meta:
        panflute_filters.extend(meta['panflute-filters-type-after-all'])

    doc.metadata['panflute-filters'] = panflute_filters


def finalize(doc):
    type = get_document_type(doc)
    format = get_document_format(doc, type)
    
    include_type_frontmatter(doc, type)
    include_format_frontmatter(doc, format)
    include_global_frontmatter(doc)
    combine_filters(doc, format)

def main(doc=None):
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()