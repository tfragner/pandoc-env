import panflute as pf

def action(elem, doc):
    pass

def finalize(doc):
    meta = doc.get_metadata()
    if 'title' in meta:
        if 'latex-level' in meta:
            if doc.get_metadata('latex-level') == 'chapter':
                doc.content.insert(0, pf.Para(pf.RawInline('\chapter{' + doc.get_metadata('title') + '}', format='latex')))
            elif doc.get_metadata('latex-level') == 'part':
                doc.content.insert(0, pf.Para(pf.RawInline('\part{' + doc.get_metadata('title') + '}', format='latex')))
            elif doc.get_metadata('latex-level') == 'subsection':
                header = pf.Header(pf.Str(doc.get_metadata('title')), level=1)
                if 'slug' in meta:
                    header.identifier = 'sec:' + doc.get_metadata('slug')
                doc.content.insert(0, header)
        else:
            header = pf.Header(pf.Str(doc.get_metadata('title')), level=1)
            if 'slug' in meta:
                header.identifier = 'sec:' + doc.get_metadata('slug')
            doc.content.insert(0, header)

def main(doc=None):
    return pf.run_filter(action, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()
