from flask import Blueprint
from .databases.get_all_databases import get_all_databases_route
from .databases.get_database_id import get_database_id_route
from .pages.create_page import create_page
from .pages.get_all_pages import get_all_pages_route
from .pages.get_page_id import get_page_id_route
from .pages.update_page import update_page

notion_bp = Blueprint('notion', __name__)

# Database routes
notion_bp.route('/get-all-databases', methods=['GET'])(get_all_databases_route)
notion_bp.route('/get-database-id', methods=['POST'])(get_database_id_route)

# Page routes
notion_bp.route('/create-page', methods=['POST'])(create_page)
notion_bp.route('/get-all-pages', methods=['GET'])(get_all_pages_route)
notion_bp.route('/get-page-id', methods=['POST'])(get_page_id_route)
notion_bp.route('/update-page', methods=['PATCH'])(update_page)
