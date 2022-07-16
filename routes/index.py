from flask import Blueprint
from controllers.auth import login, register

auth = Blueprint('auth', __name__) 

auth.route('/',methods = ['GET','POST'])(login)

auth.route('/inscription', methods = ["POST", "GET"])(register)
