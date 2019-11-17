from panflute import *

def action(elem, doc):
    pass

def finalize(doc):
    doc.content.insert(0, Para(RawInline('\\newpage', format='latex')))

def main(doc=None):
    return run_filter(action, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()