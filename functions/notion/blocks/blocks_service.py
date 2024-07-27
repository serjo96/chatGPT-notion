import requests
import json
import os

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
NOTION_TOKEN = os.getenv("NOTION_TOKEN")


def update_block(block, is_child):
    block_id = block['id']
    block_data = block['block_type_data']
    # Добавьте другие типы блоков здесь

    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }

    if is_child:
        response = requests.patch(f'{NOTION_API_URL}/blocks/{block_id}/children', headers=notion_headers, data=json.dumps(block_data))
    else:
        response = requests.patch(f'{NOTION_API_URL}/blocks/{block_id}', headers=notion_headers, data=json.dumps(block_data))

    if response.status_code != 200:
        return response.text

    return response.status_code == 200


def delete_block(block_id):
    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }
    response = requests.delete(f'{NOTION_API_URL}/blocks/{block_id}', headers=notion_headers)
    return response.status_code == 200


def create_block(page_id, blocks):
    block_data = {
        "children": blocks['block_type_data']
    }
    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }
    response = requests.patch(f'{NOTION_API_URL}/blocks/{page_id}/children', headers=notion_headers, data=json.dumps(block_data))
    return response
