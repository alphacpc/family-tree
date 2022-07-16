from flask import Blueprint
from controllers.admin import home, edit_user, detail_user, archive_user, archives, restore_user

admin = Blueprint('admin', __name__) 

admin.route('/admin', methods = ["GET", "POST"])(home)

admin.route('/edit', methods = ["GET", "POST"])(edit_user)

admin.route('/detail', methods = ["GET", "POST"])(detail_user)

admin.route('/archive')(archive_user)

admin.route('/restaure')(restore_user)

admin.route('/archives')(archives)