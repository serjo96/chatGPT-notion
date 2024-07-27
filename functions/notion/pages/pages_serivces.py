import requests
import os
import json

from flask import jsonify

from common.excpetion import PageNotFoundError
from notion.blocks.blocks_service import update_block, create_block

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"
NOTION_API_URL = "https://api.notion.com/v1"


def create_page(data):
    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }

    page_data = {
        'parent': {f'{data["parent_type"]}_id': data['parent_id']},
        'properties': {
            'title': {
                'title': [
                    {'text': {'content': data['title']}}
                ]
            }
        },
        'children': data.get('content', [])
    }

    if 'icon' in data:
        page_data['icon'] = data['icon']
    if 'cover' in data:
        page_data['cover'] = data['cover']

    response = requests.post(f'{NOTION_API_URL}/pages', headers=notion_headers, data=json.dumps(page_data))

    if response.status_code == 200:
        return response.json(), 200
    else:
        error_response = json.loads(response.text)
        return error_response, response.status_code


def get_all_pages(include_blocks):
    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }

    search_data = {
        'filter': {
            'property': 'object',
            'value': 'page'
        }
    }

    response = requests.post(f'{NOTION_API_URL}/search', headers=notion_headers, data=json.dumps(search_data))

    if response.status_code != 200:
        return json.loads(response.text), response.status_code

    pages = response.json().get('results', [])
    all_pages_with_blocks = []

    for page in pages:
        if include_blocks:
            page_id = page['id']
            blocks_response = requests.get(f'{NOTION_API_URL}/blocks/{page_id}/children', headers=notion_headers)
            if blocks_response.status_code == 200:
                blocks = blocks_response.json().get('results', [])
                combined_data = {**page, 'blocks': blocks}
                all_pages_with_blocks.append(combined_data)
            else:
                return json.loads(blocks_response.text), blocks_response.status_code
        else:
            all_pages_with_blocks.append(page)

    return all_pages_with_blocks


def get_page_content(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }

    response = requests.get(url, headers=notion_headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise PageNotFoundError(f"Content for page with ID '{page_id}' not found")


def get_page_by_name(page_name):
    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }

    search_data = {
        'query': page_name,
        'filter': {
            'property': 'object',
            'value': 'page'
        }
    }

    response = requests.post(f'{NOTION_API_URL}/search', headers=notion_headers, data=json.dumps(search_data))

    if response.status_code == 200:
        results = response.json().get('results', [])
        normalized_page_name = page_name.lower()
    else:
        error_response = json.loads(response.text)
        return error_response

    for result in results:
        if result.get('object') == 'page':
            properties = result.get('properties', {})
            title_property = properties.get('title', {}).get('title', [])
            for title_item in title_property:
                if title_item.get('type') == 'text':
                    page_content = get_page_content(result['id'])
                    if page_content:
                        return {"page": result, "content": page_content}
                    else:
                        return {"page": result}

    raise PageNotFoundError(f"Page with name '{page_name}' not found")


def update_page(page_id, data):
    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }

    update_data = {}

    if 'title' in data:
        update_data['properties'] = {
            'title': {
                'title': [
                    {'text': {'content': data['title']}}
                ]
            }
        }

    if update_data:
        response = requests.patch(f'{NOTION_API_URL}/pages/{page_id}', headers=notion_headers,
                                  data=json.dumps(update_data))
        if response.status_code != 200:
            raise Exception("Error updating page properties in Notion")

    if 'blocks' in data:
        for block in data['blocks']:
            if 'id' in block:
                if not update_block(block):
                    raise Exception(f"Error updating block with ID {block['id']} in Notion")
            else:
                if not create_block(page_id, block):
                    raise Exception("Error creating new block in Notion")

    return {"message": "Page and blocks updated successfully"}


def delete_page(page_id):
    notion_headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': NOTION_VERSION
    }

    url = f"https://api.notion.com/v1/pages/{page_id}"
    data = {'archived': True}

    response = requests.patch(url, headers=notion_headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({"error": "Error deleting page in Notion"}), 500
