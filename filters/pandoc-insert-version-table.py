import panflute as pf
import os
import collections

def prepare(doc):
    doc.version_table_rows = []

def action(elem, doc):
    pass

def insert_version_rows(doc):

    meta = doc.get_metadata()
    if 'versions' in meta:
        versions = sorted(meta['versions'], key=lambda d: [int(u) for u in d['version'].split(('.'))])
        for elem in versions:
            c1 = pf.TableCell(pf.Para(pf.Str(elem['version'])))
            c2 = pf.TableCell(pf.LineBlock(pf.LineItem(pf.Str(elem['ersteller'])), pf.LineItem(pf.Str(elem['erstelldatum']))))
            c3 = pf.TableCell(pf.LineBlock(pf.LineItem(pf.Str(elem['pruefer'])), pf.LineItem(pf.Str(elem['pruefdatum']))))
            c4 = pf.TableCell(pf.LineBlock(pf.LineItem(pf.Str(elem['freigeber'])), pf.LineItem(pf.Str(elem['freigabedatum']))))
            c5 = pf.TableCell(pf.Para(pf.Str(elem['kurzbeschreibung'])))
            doc.version_table_rows.append(pf.TableRow(c1,c2,c3,c4,c5))
            doc.lastrow = versions[-1]

def finalize(doc):
    insert_version_rows(doc)
    if len(doc.version_table_rows) > 0:
        header = pf.TableRow(
            pf.TableCell(pf.Para(pf.Strong(pf.Str('Ver.')))), 
            pf.TableCell(pf.Para(pf.Strong(pf.Str('Ersteller')))), 
            pf.TableCell(pf.Para(pf.Strong(pf.Str('Prüfer')))), 
            pf.TableCell(pf.Para(pf.Strong(pf.Str('Freigeber')))), 
            pf.TableCell(pf.Para(pf.Strong(pf.Str('Beschreibung'))))
        )
        table = pf.Table(*doc.version_table_rows, header=header, width=[.2,.3,.3,.3,1])
        doc.content.insert(0, table)
        #doc.metadata['header-right']= doc.lastrow['freigabedatum'] + ' [V: ' + doc.lastrow['version'] + ']'
        #doc.metadata['header-left']= pf.MetaInlines(pf.RawInline("\\includegraphics{./.pandoc/includes/images/Bitter-Logo.png}"))
        #doc.metadata['date']= pf.MetaInlines(pf.RawInline('\\today'))
        #doc.metadata['header-center']= doc.get_metadata('title')
        #doc.metadata['footer-left']= doc.get_metadata('slug')

def main(doc=None):
    return pf.run_filter(action, finalize=finalize, prepare=prepare, doc=doc)

if __name__ == '__main__':
    main()