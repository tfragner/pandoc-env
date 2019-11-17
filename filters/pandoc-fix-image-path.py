from panflute import *

filepath = ''

def prepare(doc):
    global filepath
    if 'filepath' in doc.get_metadata():
        filepath = doc.get_metadata('filepath')

def action(elem, doc):
    if isinstance(elem, Image):
        if not elem.url.startswith('/'):
            elem.url = filepath + '/' + elem.url
        return elem
            

def finalize(doc):
    pass

def main(doc=None):
    return run_filter(action, prepare=prepare, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()