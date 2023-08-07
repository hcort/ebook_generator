import json
import os

from ebooklib import epub
from slugify import slugify


def create_epub_from_file(json_filename, output_folder):
    json_dict = {}
    with open(json_filename, 'r') as json_file:
        json_dict = json.loads(json_file.read())
    if not json_dict:
        return
    create_epub_from_json(json_dict, output_folder)


def create_epub_from_json(json_dict, output_folder):
    book_title = json_dict.get('title', '')
    book_author = json_dict.get('author', '')
    epub_name = os.path.join(output_folder, slugify(f'{book_title}_{book_author}') + '.epub')

    book = epub.EpubBook()

    # set metadata
    book.set_identifier(epub_name)
    book.set_title(book_title)

    book.add_author(book_author)
    book.add_author(
        book_author,
        file_as=book_author
    )

    # create chapter
    all_messages = json_dict.get('parsed_messages', [])
    book.spine = ["nav"]
    for message in all_messages:
        msg = all_messages[message]
        file_name = f"chap_{msg['index']}.xhtml"
        title = f"Capítulo {msg['index']}"
        c1 = epub.EpubHtml(title=title, file_name=file_name, lang="es")
        c1.content = f"<h3>{msg['author']['username']} - {msg['date']}</h3>{msg['html_str']}"
        book.add_item(c1)
        book.toc.append((epub.Link(file_name, title, title), ()))
        book.spine.append(c1)

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = "BODY {color: white;}"
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style,
    )

    # add CSS file
    book.add_item(nav_css)

    epub.write_epub(epub_name, book, {})
    return epub_name
