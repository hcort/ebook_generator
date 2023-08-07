import json
import os

from vBulletinThreadUtils.MessageProcessor import MessageHTMLToText
from vBulletinThreadUtils.vBulletinSession import vbulletin_session
from vBulletinThreadUtils.vBulletinThreadParserGen import thread_id_to_thread_link_dict, parse_thread

from create_epub import create_epub_from_json, create_epub_from_file


def parse_thread_vBulletin(thread_id):
    """

    :param thread_id:  the id of the thread
    :return: The thread info dictionary with all the messages

    We use a MessageHTMLToText post_processor so we get the messages as HTML strings
    """
    thread_info = thread_id_to_thread_link_dict(thread_id)
    vbulletin_session.output_dir = './input/'
    bs4_tag_to_str = MessageHTMLToText()
    parse_thread(thread_info=thread_info, filter_obj=None, post_processor=bs4_tag_to_str)
    return thread_info


def thread_parsing_save_to_json_file(thread_id):
    """

    :param thread_id: the id of the thread
    :return: the filename of the generated epub

    Parses a thread and saves the result in a json file
    """
    thread_info = parse_thread_vBulletin(thread_id)
    json_filename = os.path.join(vbulletin_session.output_dir, f'{thread_info["id"]}.json')
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(thread_info, json_file)
    return json_filename


def thread_parsing_and_generate_json_epub(thread_id):
    """

    :param thread_id: the id of the thread
    :return: the filename of the generated json

    Parses a thread and saves the result in an intermedite json file
    Then uses this json file as input for the epub generator
    """
    json_filename = thread_parsing_save_to_json_file(thread_id)
    return create_epub_from_file(json_filename, output_folder='./output')


def thread_parsing_and_generate_epub(thread_id):
    """

    :param thread_id: the id of the thread
    :return: the filename of the generated json

    Parses a thread and generates the epub from the JSON object without intermediate files
    """
    thread_info = parse_thread_vBulletin(thread_id)
    return create_epub_from_json(json_dict=thread_info, output_folder='./output')


if __name__ == '__main__':
    thread_ids = ['...']
    for thid in thread_ids:
        thread_parsing_and_generate_epub(thid)

