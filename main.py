from flask import Flask, render_template
from apis.route import api
from flask_cors import CORS
from config import session_db


from routes.index import auth
from routes.admin import admin
from routes.user import user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'BbjKJKSHGnbnLKB89T7R7LDJR7HGKJD0U99U'
CORS(app)


#**** BLUEPRINT REGISTER ***#
app.register_blueprint(api)
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)


#Pour la page 404
@app.errorhandler(404)
def not_found(error):
    return render_template('pages/not_found.html'),404




if __name__=='__main__':

    result = session_db.run("MERGE (p:Person {name : $name, lname : $lname, password : $password, email : $email, profile : $profile})",
        name = "Admin", lname = "admin",
        password = "neo4j", email = "admin@neo.sn", 
        profile = "admin")

    app.run(debug=True,port=5000)