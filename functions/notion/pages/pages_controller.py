import json

from flask import Blueprint, request, jsonify, Response
from flask_restx import Namespace, Resource, fields

from notion.pages.pages_models import page_model, update_page_model
from notion.pages.pages_serivces import create_page, delete_page, get_page_by_name, get_all_pages

api = Namespace('pages', description='Page related operations')


@api.route('/create-page')
class CreatePage(Resource):
    @api.expect(page_model, validate=True)
    def post(self):
        data = request.json
        try:
            response, status_code = create_page(data)
            return response, status_code
        except Exception as error:
            error_response = json.loads(error.text)
            return error_response


@api.route('/get-all-pages')
class GetAllPages(Resource):
    @api.doc(
        params={'include_blocks': {'description': 'Include blocks in response', 'type': 'boolean', 'default': True}})
    def get(self):
        include_blocks = request.args.get('include_blocks', 'true').lower() == 'true'

        try:
            response = get_all_pages(include_blocks)
            return response
        except Exception as error:
            error_response = json.loads(error.text)
            return error_response


@api.route('/get-page')
class GetPageID(Resource):
    @api.doc(params={'page_name': 'The name of the page'})
    def get(self):
        page_name = request.args.get('page_name')
        if not page_name:
            return {"error": "Page name is required"}, 400

        try:
            return get_page_by_name(page_name)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@api.route('/update-page')
class UpdatePage(Resource):
    @api.expect(update_page_model)
    @api.doc(params={'page_id': 'The ID of the page to update'})
    def patch(self):
        data = request.json
        page_id = request.args.get('page_id')
        try:
            response = update_page(page_id, data)
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@api.route('/delete-page')
class DeletePage(Resource):
    @api.doc(params={'page_id': 'The ID of the page to delete'})
    def delete(self):
        page_id = request.args.get('page_id')
        if not page_id:
            return {"error": "Page ID is required"}, 400

        response, status_code = delete_page(page_id)
        return jsonify(response), status_code
