import panflute as pf

def prepare(doc):
    meta = doc.get_metadata()
    if 'latex-level' in meta and meta['latex-level'] == 'subsection':
        doc.fixsubsection = True

def action(elem, doc):
    if isinstance(elem, pf.Header) and hasattr(doc, 'fixsubsection') and doc.fixsubsection:
        elem.level = elem.level + 1
        return elem

def finalize(doc):
    pass

def main(doc=None):
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()