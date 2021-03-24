import os
from os.path import join, dirname
import json
from typing import List
from concurrent.futures import ProcessPoolExecutor, wait

from dotenv import load_dotenv
from notion.client import NotionClient
from md2notion.upload import convert, uploadBlock
from tqdm import tqdm

from src import parser


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
COLLECTION_VIEW_URL = os.environ.get('COLLECTION_VIEW_URL')
SCRAPBOX_FILE_NAME = os.environ.get('SCRAPBOX_FILE_NAME')

notion_client = NotionClient(token_v2=NOTION_TOKEN)
collection_view = notion_client.get_collection_view(COLLECTION_VIEW_URL)


def load_scrapbox_file(filename: str):
    with open(filename, encoding='utf-8') as f:
        scrapbox_data = json.load(f)
    return scrapbox_data['pages']


def parse_scrapbox_lines(lines: List[str]) -> str:
    markdown_lines = [parser.scrapbox_to_markdown(line) for line in lines]
    return '\n'.join(markdown_lines)


def write_notion(scrapbox_pages):
    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(upload_markdown_block, scrapbox_page) for scrapbox_page in scrapbox_pages]
        done, not_done = wait(futures)
        [future.result() for future in tqdm(futures)]


def upload_markdown_block(scrapbox_page):
    new_page = collection_view.collection.add_row()
    new_page.title = scrapbox_page['title']

    markdown_text = parse_scrapbox_lines(scrapbox_page['lines'])
    notion_block = convert(markdown_text)
    for blockDescriptor in notion_block:
        uploadBlock(blockDescriptor, new_page, '')


def main():
    scrapbox_pages = load_scrapbox_file(SCRAPBOX_FILE_NAME)
    if scrapbox_pages is None or len(scrapbox_pages) == 0:
        raise Exception('ページが存在しない')
    write_notion(scrapbox_pages)


if __name__ == '__main__':
    main()
