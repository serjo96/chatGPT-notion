import json
from flask import request, jsonify, Response
from flask_restx import Namespace, Resource, fields
from .block_models import update_block_model, create_block_model
from .blocks_service import update_block, delete_block, create_block

api = Namespace('blocks', description='Block related operations')


@api.route('/update-block')
class UpdateBlock(Resource):
    @api.expect(update_block_model, validate=True)
    @api.doc(params={'is_child': {'description': 'Flag to update a child block', 'type': 'boolean'}})
    def patch(self):
        data = request.json
        is_child = request.args.get('is_child', 'false').lower() == 'true'

        if update_block(data, is_child):
            return {"message": "Block updated successfully"}
        else:
            return jsonify({"error": "Error updating block in Notion"}), 500


@api.route('/delete-block')
class DeleteBlock(Resource):
    @api.doc(params={'block_id': 'The ID of the block to delete'})
    def delete(self):
        block_id = request.args.get('block_id')
        if not block_id:
            return {"error": "Block ID is required"}, 400

        if delete_block(block_id):
            return {"message": "Block deleted successfully"}
        else:
            return jsonify({"error": "Error deleting block in Notion"}), 500


@api.route('/create-block')
class CreateBlock(Resource):
    @api.expect(create_block_model)
    def post(self):
        data = request.json
        page_id = data['page_id']
        response = create_block(page_id, data)

        if response.status_code == 200:
            return {"message": "Block created successfully"}
        else:
            error_response = json.loads(response.text)
            return error_response
