#!/usr/bin/env python

import panflute as pf
import os
import sys
import redis
import json
import redis

r = redis.Redis()

def prepare(doc):
    doc.identifiers = {}
    doc.walk(find_header)

def find_header(elem, doc):
    if isinstance(elem, pf.Header):
        doc.identifiers[elem.identifier] = pf.stringify(elem)

def action(elem, doc):
    if isinstance(elem, pf.Cite):
        title = None
        for c in elem.citations:
            id = c.id
            sec = 'sec' + id[3:]
            if sec in doc.identifiers:
                c.id = sec
                title = doc.identifiers[sec]
        if title is not None:
            return [pf.Str(title), pf.Space, pf.Str('(siehe Kapitel '), elem, pf.Str(')')]
        else:
            link = id[4:]
            text = link
            try:
                text = json.loads(r.get(link))['title']
            except:
                pass
            return pf.Link(pf.Str(text), url='https://doku.bitter.at/' + link)



def finalize(doc):
    pass

def main(doc=None):
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()