import os
from flask import Flask, Blueprint
from flask_restx import Api
from notion.pages.pages_controller import api as pages_api
from notion.pages.pages_models import api as pages_models_api
from notion.databases import api as databases_api
from notion.models import api as models_api
from notion.blocks.block_models import api as blocks_models_api
from notion.blocks.blocks_controller import api as blocks_api

# Инициализация Flask приложения
blueprint = Blueprint('api', __name__, url_prefix='/notion')
app = Flask(__name__)
api = Api(app, version='1.0', title='Notion API',
          description='A simple Notion API',
          doc='/notion/docs')  # Устанавливаем путь для документации

# Импортируем и регистрируем маршруты
api.add_namespace(pages_api, path='/notion/pages')
api.add_namespace(databases_api, path='/notion/databases')
api.add_namespace(blocks_api, path='/notion/blocks')  # Регистрируем наш новый API
api.add_namespace(models_api, path='/models')
api.add_namespace(blocks_models_api, path='/models/blocs')
api.add_namespace(pages_models_api, path='/models/pages')
app.register_blueprint(blueprint)


@app.route('/notion')
def index():
    return 'Welcome to the Notion API integration with Firebase Functions!'


if __name__ == "__main__":
    app.run(debug=True)
