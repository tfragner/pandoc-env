#!/usr/bin/env python

import panflute as pf
import os

def prepare(doc):
    doc.meta_table_rows = []

def action(elem, doc):
    pass

def create_tablecell_content(content, field_type):   
    if type(content) == list:
        lines = []
        for item in content:
            if field_type == 'doc':
                lines.append(pf.LineItem(pf.Str('-'), pf.Space, pf.Cite(pf.Str('@doc:' + item), citations=[pf.Citation('doc:' +item)])))
            elif field_type == 'raw':
                lines.append(pf.LineItem(pf.Str('-'), pf.Space, pf.RawInline(item)))
            else:
                lines.append(pf.LineItem(pf.Str('-'), pf.Space, pf.Str(item)))
        return pf.LineBlock(*lines)
    elif type(content) == str:
        if field_type == 'doc':
            return pf.Plain(pf.Cite(pf.Str('@doc:' + content), citations=[pf.Citation('doc:' +content )]))
        elif field_type == 'raw':
            return pf.Plain(pf.RawInline(content))
        else:
            return pf.Plain(pf.Str(content))
    else:
        return pf.Plain(pf.Str('not supported'))

def create_row(doc, field):
    field_name = field['name']
    field_caption = field['caption']
    field_type = field['type']
    meta = doc.get_metadata()
    c1 = pf.TableCell(pf.Para(pf.Strong(pf.Str(field_caption))))
    if field_name in meta:
        c2 = pf.TableCell(create_tablecell_content(meta[field_name], field_type))
    else:
        c2 = pf.TableCell(pf.Plain(pf.Str('missing')))
    doc.meta_table_rows.append(pf.TableRow(c1, c2))

def insert_mandatory_fields(doc):
    meta = doc.get_metadata()
    if 'meta-mandatory-fields' in meta:
        mandatory_fields = meta['meta-mandatory-fields']
        for field in mandatory_fields:
           create_row(doc, field)
        

def insert_optional_fields(doc):
    meta = doc.get_metadata()
    if 'meta-optional-fields' in meta:
        optional_fields = meta['meta-optional-fields']
        for field in optional_fields:
            if field['name'] in meta:
                create_row(doc, field)

def finalize(doc):
    meta = doc.get_metadata()
    insert_mandatory_fields(doc)
    insert_optional_fields(doc)
    header = pf.TableRow(pf.TableCell(pf.Plain(pf.Str('Parameter'))), pf.TableCell(pf.Plain(pf.Str('Wert'))))
    if len(doc.meta_table_rows) > 0:
        table = pf.Table(*doc.meta_table_rows, width=[.5,1], header=header)
        doc.content.insert(0, table)

def main(doc=None):
    return pf.run_filter(action, finalize=finalize, prepare=prepare, doc=doc)

if __name__ == '__main__':
    main()