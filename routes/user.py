from flask import Blueprint
from controllers.user import home, tree, chat

user = Blueprint('user', __name__) 

user.route('/user', methods=["POST", "GET"])(home)

user.route('/tree', methods = ["GET", "POST"])(tree)

user.route('/chat')(chat)