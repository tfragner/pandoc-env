import panflute as pf
import os
import sys

def action(elem, doc):
    pass

def finalize(doc):
    doc.content.insert(0, pf.Para(pf.RawInline('\\dummy{\\Begin{landscape}}', format='latex')))
    doc.content.insert(0, pf.Para(pf.RawInline('\\newcommand\\dummy[1]{#1}', format='latex')))
    doc.content.insert(0, pf.Para(pf.RawInline('\\newgeometry{layout=a3paper, top=25mm, left=30mm, right=30mm, bottom=25mm}', format='latex')))
    doc.content.insert(0, pf.Para(pf.RawInline('\\recalctypearea', format='latex')))
    doc.content.insert(0, pf.Para(pf.RawInline('\\KOMAoptions{paper=a3}', format='latex')))

    doc.content.insert(sys.maxsize, pf.Para(pf.RawInline('\\clearpage', format='latex')))
    doc.content.insert(sys.maxsize, pf.Para(pf.RawInline('\\dummy{\\End{landscape}}', format='latex')))
    doc.content.insert(sys.maxsize, pf.Para(pf.RawInline('\\KOMAoptions{paper=a4}', format='latex')))
    doc.content.insert(sys.maxsize, pf.Para(pf.RawInline('\\recalctypearea', format='latex')))
    doc.content.insert(sys.maxsize, pf.Para(pf.RawInline('\\restoregeometry', format='latex')))

def main(doc=None):
    return pf.run_filter(action, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()