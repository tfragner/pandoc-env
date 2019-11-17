from panflute import *
import uuid
import redis
import json

def action(elem, doc):
    pass

def finalize(doc):
    meta = doc.get_metadata()
    r = redis.Redis()
    try:
        if 'slug' not in meta:
            doc.metadata['slug'] = MetaString(str(uuid.uuid1()))
            r.mset({doc.get_metadata('slug'): json.dumps(doc.get_metadata())})
        else:
            res = r.get(doc.get_metadata('slug'))
            r.mset({doc.get_metadata('slug'): json.dumps(doc.get_metadata())})
    except:
        pass

def main(doc=None):
    return run_filter(action, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()