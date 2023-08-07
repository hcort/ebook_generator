import os
import pathlib

"""

    File structure:
    
    ebook
        META-INF
            container.xml
        OEBPS
            Content.opf
            cover.jpg
            file1.xhtml
            file2.xhtml
            ...
            toc.xhtml
        mimetype

"""


def create_chapter_file(path, idx, file_content):
    oebps = os.path.join(path, 'OEBPS')
    pathlib.Path(oebps).mkdir(parents=True, exist_ok=True)
    # os.mkdir(oebps, exist_ok=True)
    chapter_filename = f'chapter_{idx}.xhtml'
    with open(os.path.join(oebps, chapter_filename), 'w', encoding='utf-8') as file:
        file.write(file_content)
    return chapter_filename


def generate_temp_files(path, book_title, book_author, chapter_list):
    create_mimetype(path)
    create_container_xml(path)
    create_toc_xml(path, book_title, chapter_list)
    create_content_opf(path, book_title, book_author, chapter_list)


def create_mimetype(path):
    with open(os.path.join(path, 'mimetype'), 'w', encoding='utf-8') as file:
        file.write('application/epub+zip')


def create_container_xml(path):
    container_str = '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">' \
                    '<rootfiles><rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>' \
                    '</rootfiles>' \
                    '</container>'
    meta_inf = os.path.join(path, 'META-INF')
    pathlib.Path(meta_inf).mkdir(parents=True, exist_ok=True)
    # os.mkdir(meta_inf, exist_ok=True)
    with open(os.path.join(meta_inf, 'container.xml'), 'w', encoding='utf-8') as file:
        file.write(container_str)


def create_toc_xml(path, book_title, chapter_list):
    toc_str = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html>' \
              '<html xmlns="http://www.w3.org/1999/xhtml" ' \
              'xmlns:epub="http://www.idpf.org/2007/ops"><head><title>{title}</title></head>' \
              '<body><section class="frontmatter TableOfContents"><header><h1>Contents</h1></header>' \
              '<nav id="toc" role="doc-toc" epub:type="toc"><ol>{list_items}</ol></nav></section></body></html>'
    oebps = os.path.join(path, 'OEBPS')
    pathlib.Path(oebps).mkdir(parents=True, exist_ok=True)
    # os.mkdir(oebps, exist_ok=True)
    list_items_str = ''
    for item in chapter_list:
        list_items_str += '<li class="toc-Chapter-rw" id="num_0"><a href="{chapter_file_name}">' \
                          '<title>{chapter_title}</title></a></li>'.format(chapter_file_name=item['file'],
                                                                           chapter_title=item['title'])
    with open(os.path.join(oebps, 'toc.xhtml'), 'w', encoding='utf-8') as file:
        file.write(toc_str.format(title=book_title, list_items=list_items_str))


def create_content_opf(path, book_title, book_author, chapter_list):
    opf_str = '<package version="3.1" xmlns="http://www.idpf.org/2007/opf"><metadata>' \
              '<dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">{book_title}</dc:title>' \
              '<dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ns0="http://www.idpf.org/2007/opf" ' \
              'ns0:role="aut" ns0:file-as="Unbekannt">{book_author}</dc:creator>' \
              '<meta xmlns:dc="http://purl.org/dc/elements/1.1/" name="calibre:series" ' \
              'content="{book_title}"/></metadata><manifest>{item_list}<item href="toc.xhtml" id="toc" ' \
              'properties="nav" media-type="application/xhtml+xml"/></manifest>' \
              '<spine><itemref idref="toc" linear="no"/>{item_ref_list}</spine></package>'
    item_list_str = ''
    item_ref_str = ''
    for idx, item in enumerate(chapter_list):
        item_list_str += '<item id="file_{idx}" href="{filename}" ' \
                         'media-type="application/xhtml+xml"/>'.format(idx=idx, filename=item['file'])
        item_ref_str += '<itemref idref="file_{idx}"/>'.format(idx=idx)
    oebps = os.path.join(path, 'OEBPS')
    pathlib.Path(oebps).mkdir(parents=True, exist_ok=True)
    # os.mkdir(oebps, exist_ok=True)
    with open(os.path.join(oebps, 'Content.opf'), 'w', encoding='utf-8') as file:
        file.write(opf_str.format(book_title=book_title, book_author=book_author,
                                  item_list=item_list_str, item_ref_list=item_ref_str))
