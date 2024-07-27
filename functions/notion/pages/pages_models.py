from flask_restx import Namespace, fields

from notion.blocks.block_models import create_block_model, update_block_model, block_content_model

api = Namespace('models', description='Models related operations')

page_model = api.model('Page', {
    'parent_type': fields.String(required=True, description='The type of the parent (database or page)'),
    'parent_id': fields.String(required=True, description='The ID of the parent'),
    'title': fields.String(required=True, description='The title of the page'),
    'icon': fields.Raw(description='The icon of the new page, either an emoji object or an external file object'),
    'cover': fields.Raw(description='The cover image of the new page, represented as a file object'),
    'properties': fields.Raw(description='The values of the page’s properties. If the parent is a database, then the schema must match the parent database’s properties. If the parent is a page, then the only valid object key is title.'),
    'content': fields.List(
        fields.Nested(block_content_model, description='List of blocks to add'),
        description='List of blocks for creating'
    )
})

update_page_model = api.model('UpdatePage', {
    'title': fields.String(description='The new title of the page', required=False),
    'blocks': fields.List(fields.Nested(api.model('Block', {
        'id': fields.String(description='The ID of the block', required=False),
        'type': fields.String(description='The type of the block', required=True),
        'text': fields.String(description='The text content of the block', required=True)
    })), description='List of blocks to update or create new if id is not passing.', required=False)
})


api.models[update_page_model.name] = update_page_model
api.models[page_model.name] = page_model
