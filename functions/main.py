import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
from firebase_functions import https_fn
from werkzeug.wrappers import Response as WerkzeugResponse
import logging
from app import app

# Загрузка переменных окружения
load_dotenv()

# Инициализация Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)


# Firebase Functions handler
@https_fn.on_request()
def api(req: https_fn.CallableRequest) -> https_fn.Response:
    logging.debug('Received request at Firebase function')

    def wsgi_app(environ, start_response):
        return app.wsgi_app(environ, start_response)

    response = WerkzeugResponse.from_app(wsgi_app, req)
    logging.debug(f'Response status: {response.status_code}')
    logging.debug(f'Response headers: {response.headers}')
    logging.debug(f'Response body: {response.get_data()}')

    return https_fn.Response(response.get_data(), headers=dict(response.headers), status=response.status_code)

