from flask_restx import Namespace, fields

from notion.blocks.block_models import create_block_model, update_block_model, block_content_model

api = Namespace('models', description='Models related operations')

database_model = api.model('Database', {
    'parent_page_id': fields.String(required=True, description='The ID of the parent page'),
    'title': fields.String(required=True, description='The title of the database'),
    'properties': fields.Raw(required=True, description='The properties of the database')
})


# Регистрация моделей
api.models[database_model.name] = database_model
api.models[create_block_model.name] = create_block_model
api.models[update_block_model.name] = update_block_model
