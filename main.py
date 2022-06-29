from email import message
from pprint import pprint
from flask import Flask, flash, redirect, render_template, request, session
from apis.route import api, api_user, api_users, api_register, api_users_archiver
from neo4j import GraphDatabase
from flask_cors import CORS
from datetime import date


driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "connect"))
session_db = driver.session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupe3'
CORS(app)


#Pour gerer les routes
app.register_blueprint(api)



@app.route('/', methods = ["POST", "GET"])
def login():

    if request.method == 'POST':
        
        email = request.form.get('email')
        mdp = request.form.get('mdp')

        if email and mdp :

            user = api_user(email, "login")

            if user :
                if mdp == user['p.password']:

                    session["email"] = user['p.email']

                    if user['p.profile'] == "admin":
                        return redirect('/admin')
                    
                    else:
                        return redirect('/user')

                else:
                    message = "Mot de passe incorrect !"
            else:
                message = "Cet utilisateur n'existe pas !"
        
        else:
            message = "Veuillez remplir tous les champs !"
        
        return render_template('pages/login.html', message = message)


    return render_template('pages/login.html')



@app.route('/a', methods = ["POST", "GET"])
def register():

    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        password = request.form.get('mdp')
        passwordc = request.form.get('mdpc')

        if email and fname and lname and password and passwordc:

            if password == passwordc:

                user = api_user(email, "register")

                if user:
                    message = "Cet utilisateur existe déjà !"

                else:
                    
                    user = api_register(fname, lname, email, password)

                    if user:
                        return redirect('/')

                    else:
                        message = "Veuillez remplir tous les champs !"
            else:
                message = "Les deux mots de passe ne sont pas identiques !"
            
        else:
            message = "Veuillez remplir tous les champs"
        
        return render_template('pages/register.html', message = message)
        
    return render_template('pages/register.html')




@app.route('/admin', methods = ["GET", "POST"])
def admin():

    if 'email' in session:

        users = api_users()

        user = api_user(session['email'])

        current_user = {
            'fname' : user['p.name'],
            'lname' : user['p.lname'],
            'email' : session['email'],
            'profile' : user['p.profile']
        }

        if request.method == 'POST':

            print('hello')

        return render_template('pages/admin/admin.html', user = current_user, today = date.today() , users = users)

    else:
        return redirect('/')







@app.route('/archive')
def archive():
    if 'email' in session:

        user = api_user(session['email'])
        users = api_users_archiver()


        current_user = {
            'fname' : user['p.name'],
            'lname' : user['p.lname'],
            'email' : session['email'],
            'profile' : user['p.profile']
        }

        return render_template('pages/admin/archive.html', user = current_user, today = date.today(), users = users)
    
    return redirect('/')



@app.route('/user')
def user():

    if 'email' in session:
        user = api_user(session['email'])

        current_user = {
            'fname' : user['p.name'],
            'lname' : user['p.lname'],
            'email' : session['email'],
            'profile' : user['p.profile'],
            'sex' : user['p.sex'],
            'age' : user['p.age'],
            'job' : user['p.job'],
            'phone' : user['p.phone']
        }

        return render_template('pages/user/home.html', user = current_user, today = date.today())
    else:
        return redirect('/')


@app.route('/tree', methods = ["GET", "POST"])
def tree():

    if 'email' in session:
        user = api_user(session['email'])

        current_user = {
            'fname' : user['p.name'],
            'lname' : user['p.lname'],
            'email' : session['email'],
            'profile' : user['p.profile'],
        }

        if request.method == 'POST':
            print('hello')

        return render_template('pages/user/tree.html', user = current_user, today = date.today())
    
    else:
        return redirect('/')




@app.route('/chat')
def chat():

    if 'email' in session:
        user = api_user(session['email'])

        current_user = {
                'fname' : user['p.name'],
                'lname' : user['p.lname'],
                'email' : session['email'],
                'profile' : user['p.profile'],
        }
        return render_template('pages/user/chat.html', user = current_user, today = date.today())

    return redirect('/')





if __name__=='__main__':

    result = session_db.run("MERGE (p:Person {name : $name, lname : $lname, password : $password, email : $email, profile : $profile})",
        name = "Admin", lname = "DIALLO",
        password = "neo4j", email = "admin@neo.sn", 
        profile = "admin")

    app.run(debug=True,port=5000)