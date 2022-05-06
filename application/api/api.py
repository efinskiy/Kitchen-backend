from crypt import methods
from flask import Blueprint
from werkzeug import exceptions

from .client import basket as client_basket
from .client import user as client_user
from .client import menu as client_menu
from .client import order as client_order

from .admin import category as admin_category
from .admin import product as admin_product
from .admin import settings as admin_settings
from .admin import logs as admin_logs
from .admin import auth as admin_auth
from .admin import user as admin_users

from . import handlers as handlers

from .wrappers import is_admin, is_kitchen

kitchen_api = Blueprint('kitchen_api', __name__)

@kitchen_api.app_errorhandler(exceptions.MethodNotAllowed)
def bp_handle_405(): return handlers.handle_method_not_allowed()

kitchen_api.app_errorhandler(exceptions.NotFound) 
def bp_handle_404(): return handlers.handle_404()

kitchen_api.before_app_request(handlers.checkCustomer)

kitchen_api.add_url_rule('/status', 'kitchenStatus', admin_settings.statusGet, methods=['GET'])

kitchen_api.add_url_rule('/basket', 'basketGet', client_basket.getBasket, methods=['GET'])
kitchen_api.add_url_rule('/basket', 'basketPost', client_basket.addProductToBasket, methods=['POST'])
kitchen_api.add_url_rule('/basket', 'basketPatch', client_basket.patchBasket, methods=['PATCH'])
kitchen_api.add_url_rule('/basket/clear', 'basketClear', client_basket.clear, methods=['GET'])

kitchen_api.add_url_rule('/user', 'userGet', client_user.return_userid, methods=['GET'])

kitchen_api.add_url_rule('/menu', 'menuGet', client_menu.getMenu, methods=['GET'])
kitchen_api.add_url_rule('/menu/info', 'productInfo', client_menu.getProductInfo, methods=['GET'])

kitchen_api.add_url_rule('/order', 'orderGet', client_order.orderGet, methods=['GET'])
kitchen_api.add_url_rule('/order', 'orderPost', client_order.createOrder, methods=['POST'])
kitchen_api.add_url_rule('/orders', 'ordersGet', client_order.ordersGet, methods=['GET'])

# ADMIN API
kitchen_api.add_url_rule('/admin/login', 'adminLogin', admin_auth.login, methods=['POST'])
kitchen_api.add_url_rule('/admin/logout', 'adminLogout', is_kitchen(admin_auth.logout), methods=['POST'])
kitchen_api.add_url_rule('/admin/user', 'adminNewUser', is_admin(admin_users.new_user), methods=['POST'])
kitchen_api.add_url_rule('/admin/whoami', 'whoami', admin_users.whoami, methods=['GET'])

kitchen_api.add_url_rule('/admin/settings', 'settingsGet', is_admin(admin_settings.settingsGet), methods=['GET'])
kitchen_api.add_url_rule('/admin/settings', 'settingsPatch', is_admin(admin_settings.settingsSet), methods=['PATCH'])
kitchen_api.add_url_rule('/admin/settings', 'settingsNew', is_admin(admin_settings.settingsNew), methods=['POST'])

kitchen_api.add_url_rule('/admin/product/amount', 'adminProductAmount', is_kitchen(admin_product.product_updateAmount), methods=['PATCH'])
kitchen_api.add_url_rule('/admin/product', 'adminProductCreate', is_kitchen(admin_product.product_create), methods=['POST'])
kitchen_api.add_url_rule('/admin/product', 'adminProductPatch', is_kitchen(admin_product.product_patch), methods=['PATCH'])

kitchen_api.add_url_rule('/admin/category', 'adminCategoryCreate', is_kitchen(admin_category.category_create), methods=['POST'])

kitchen_api.add_url_rule('/admin/log', 'adminLogGet', is_admin(admin_logs.log_get), methods=['GET'])
kitchen_api.add_url_rule('/admin/ip', 'getIP', admin_logs.get_ip, methods=['GET'])
# Handlers


# bps = kitchen_api