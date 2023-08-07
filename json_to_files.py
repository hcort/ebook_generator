"""

    Import Json files and create all the xhtml files in the temporal folder

    Thread in JSON format:
    {
        "id": "",
        "url": "",
        "title": "",
        "hover": "",
        "author": "",
        "author_id": "",
        "parsed_messages": [
            "": {
                "author": {
                    "id": "",
                    "username": "",
                    "is_op": true,
                    "avatar": ""
                },
                "index": "",
                "date": "",
                "link": "",
                "title": "",
                "html_str": ""              < this is the HTML we will use as a "chapter" in the ebook
            },
            ...
        ],
        "first_post_id": ""
    }

"""
import json
import os
import shutil
import zipfile
from epubcheck import EpubCheck
from slugify import slugify

from create_files import create_chapter_file, generate_temp_files


def generate_chapter_files(temp_folder, book_chapters):
    generated_chapters = []
    for chapter in book_chapters:
        idx = book_chapters[chapter].get('index', '')
        date = book_chapters[chapter].get('date', '')
        last_date = date
        chapter_title = f'Capítulo #{idx} - {date}'
        chapter_filename = create_chapter_file(temp_folder, idx, book_chapters[chapter].get('html_str', ''))
        generated_chapters.append(
            {
                'title': chapter_title,
                'file': chapter_filename,
                'date': date
            }
        )
    return generated_chapters


def add_files_to_zip(epub, temp_folder):
    for root, subdirs, files in os.walk(temp_folder):
        for file in files:
            epub.write(os.path.join(root, file), file)
        for subdir in subdirs:
            for root_subdir, subdir_dirs, files_subdir in os.walk(os.path.join(root, subdir)):
                for subdir_file in files_subdir:
                    file_rel_path = os.path.join(root_subdir, subdir_file)
                    epub.write(file_rel_path, subdir + '/' + subdir_file)
        return


def parse_json_file(input_folder, filename, output_folder):
    with open(os.path.join(input_folder, filename), 'r') as json_file:
        json_dict = json.loads(json_file.read())
        book_title = json_dict.get('title', '')
        book_author = json_dict.get('author', '')
        temp_folder = os.path.join(output_folder, slugify(f'{filename}_{book_title}_epub'))
        generated_chapters = generate_chapter_files(temp_folder, json_dict.get('parsed_messages', []))
        last_date = generated_chapters[-1]['date']
        generate_temp_files(path=temp_folder,
                            book_title=book_title, book_author=book_author, chapter_list=generated_chapters)
        epub_name = os.path.join(output_folder, slugify(f'{book_title}_{book_author}_{last_date}') + '.epub')
        epub = zipfile.ZipFile(epub_name, "w")
        add_files_to_zip(epub=epub, temp_folder=temp_folder)
        epub.close()
        shutil.rmtree(temp_folder, ignore_errors=True)
        result = EpubCheck(epub_name)
        print(result.valid)
        print(result.messages)
