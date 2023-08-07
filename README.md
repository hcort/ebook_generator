Project used with vBulletinThreadUtils

* Use the parse_thread method from vBulletinThreadUtils
* You will need to create a config.ini file (see vBulletinThreadUtils docs)
* We pass MessageHTMLToText as a message processor for the parser. This was we will get the HTML of each post as a string
* Save the thread_info dictionary as a JSON file (optional)
* Iterate over the messages in the thread and generate an epub chapter from each of them

There are two methods to generate EPUBs in this project:
* create_epub.py: Use ebooklib library to handle all the internals
* json_to_files.py + create_files.py: Manually create the internal EPUB file structure

EPUB structure created in create_files.py:
* ebook
  * META-INF
    * container.xml
  * OEBPS
    * Content.opf
    * cover.jpg
    * file1.xhtml
    * file2.xhtml
    * ...
    * toc.xhtml
  * mimetype