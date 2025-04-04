"""
    Change ebook (epub and mobi) names to "[author] - [title].ext"

    Ebooks downloaded from Telegram come with non-relevant filenames. This script reads epub and mobi files, extracts title and author from the ebook and renames the file with a more relavant name.

    It uses the ebook parsing libraries from:

    https://github.com/aerkalov/ebooklib

    https://github.com/kroo/mobi-python
"""

import os
import sys

# https://github.com/aerkalov/ebooklib
# la instalación de esta librería da problemas con PyCharm por la dependencia con lxml
from ebooklib import epub
# https://github.com/kroo/mobi-python
from mobi import Mobi

bad_chars = ['"', '*', '>', '<', '?', '\\', '/', '|', ':']


def remove_bad_chars(text):
    for c in bad_chars:
        if c in text:
            text = text.replace(c, '')
    return text


def read_epub_data(nombre_comp):
    try:
        book = epub.read_epub(nombre_comp)
        tit = book.get_metadata('DC', 'title')[0][0]
        aut = book.get_metadata('DC', 'creator')[0][0]
        return [aut, tit, '.epub']
    except Exception as err:
        print(os.path.join(nombre_comp) + ' ERROR:' + str(err))
        return [None, None, None]


def read_mobi_data(nombre_comp):
    try:
        book = Mobi(nombre_comp)
        book.parse();
        tit = book.title().decode('utf-8')
        aut = book.author().decode('utf-8')
        return [aut, tit, '.mobi']
    except Exception as err:
        print(os.path.join(nombre_comp) + ' ERROR:' + str(err))
        return [None, None, None]


def parse_folders(path):
    for dir_name_root, sub_dir_root_list, file_root_list in os.walk(path):
        for filename in file_root_list:
            [aut, tit, ext] = None, None, None
            nombre_comp = os.path.join(dir_name_root, filename)
            if filename.endswith('epub'):
                [aut, tit, ext] = read_epub_data(nombre_comp)
            if filename.endswith('mobi'):
                [aut, tit, ext] = read_mobi_data(nombre_comp)
            if aut and tit and ext:
                nuevo_nombre = (os.path.join(dir_name_root, remove_bad_chars(aut + ' - ' + tit + ext)))
                try:
                    if nuevo_nombre != nombre_comp:
                        # eliminar duplicadoss
                        if os.path.isfile(nuevo_nombre):
                            os.remove(nombre_comp)
                        else:
                            os.rename(nombre_comp, nuevo_nombre)
                except Exception as err:
                    print(os.path.join(dir_name_root, filename) + ' ERROR:' + str(err))
        for subdir in sub_dir_root_list:
            parse_folders(subdir)


def main():
    if len(sys.argv) != 2:
        print('ERROR: no path given')
        exit
    parse_folders(sys.argv[1])


# Lanzamos la función principal
if __name__ == "__main__":
    main()
