import os
import json
from flask import request, jsonify
from flask_restx import Namespace, Resource
from .models import database_model
from dotenv import load_dotenv
import requests

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')

api = Namespace('databases', description='Database related operations')


@api.route('/create-database')
class CreateDatabase(Resource):
    @api.doc(body=database_model)
    def post(self):
        data = request.json
        notion_headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-05-13'
        }

        database_data = {
            'parent': {'type': 'page_id', 'page_id': data['parent_page_id']},
            'title': [{'type': 'text', 'text': {'content': data['title']}}],
            'properties': data['properties']
        }

        response = requests.post('https://api.notion.com/v1/databases', headers=notion_headers, data=json.dumps(database_data))

        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({"error": "Error creating database in Notion"}), 500

@api.route('/get-all-databases')
class GetAllDatabases(Resource):
    def get(self):
        notion_headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-05-13'
        }

        search_data = {
            'filter': {
                'property': 'object',
                'value': 'database'
            }
        }

        response = requests.post('https://api.notion.com/v1/search', headers=notion_headers, data=json.dumps(search_data))

        if response.status_code == 200:
            return response.json().get('results', []), 200
        else:
            return jsonify({"error": "Error retrieving databases"}), 500


@api.route('/get-database-id')
class GetDatabaseID(Resource):
    @api.doc(params={'database_name': 'The name of the database'})
    def post(self):
        data = request.json
        database_name = data.get('database_name')
        notion_headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-05-13'
        }

        search_data = {
            'query': database_name,
            'filter': {
                'property': 'object',
                'value': 'database'
            }
        }

        response = requests.post('https://api.notion.com/v1/search', headers=notion_headers, data=json.dumps(search_data))

        if response.status_code == 200:
            results = response.json().get('results', [])
            for result in results:
                if result.get('object') == 'database' and result.get('title'):
                    title = result['title'][0]['text']['content']
                    if title.lower() == database_name.lower():
                        return {"database_id": result['id']}
            return {"error": "Database not found"}, 404
        else:
            return {"error": "Error retrieving database ID"}, 500
