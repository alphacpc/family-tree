from crypt import methods
from email import message
from pprint import pprint
from flask import Flask, flash, redirect, render_template, request, session
from apis.route import api, api_user, api_users, api_register, api_users_archiver, api_get_parents
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

        return render_template('pages/admin/admin.html', user = current_user, today = date.today().strftime("%d/%m/%Y") , users = users)

    else:
        return redirect('/')






@app.route('/edit', methods = ["GET", "POST"])
def edit_user():

    if 'email' in session:

        user = api_user(session['email'])

        user_uuid = request.args.get('uuid')
        user_edit = session_db.run("MATCH (p:Person {uuid: $uuid}) RETURN p", uuid = user_uuid).data()[0]['p']

        current_user = {
            'fname' : user['p.name'],
            'lname' : user['p.lname'],
            'email' : session['email'],
            'profile' : user['p.profile']
        }

        if request.method == "POST":
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            email = request.form.get('email')
            mdp = request.form.get('mdp')

            query = "MATCH (p:Person {uuid : $uuid}) SET p += { name : $fname, lname : $lname, email : $email, password : $password }"

            session_db.run(query, uuid =user_uuid, fname = fname, lname = lname, email = email, password = mdp)

            return redirect('/admin')

        return render_template('pages/admin/edit_user.html', user = current_user, user_edit = user_edit, today = date.today().strftime("%d/%m/%Y"))

    else:
        return redirect('/')








@app.route('/detail', methods = ["GET", "POST"])
def detail_user():

    if 'email' in session:
    
        user = api_user(session['email'])

        user_uuid = request.args.get('uuid')
        user_edit = session_db.run("MATCH (p:Person {uuid: $uuid}) RETURN p", uuid = user_uuid).data()[0]['p']

        print(user_edit)

        current_user = {
            'fname' : user['p.name'],
            'lname' : user['p.lname'],
            'email' : session['email'],
            'profile' : user['p.profile']
        }

        if request.method == 'POST':
            pass

        return render_template('pages/admin/detail.html', user = current_user, user_edit = user_edit, today = date.today().strftime("%d/%m/%Y"))

    else:
        return redirect('/')












@app.route('/archive')
def archive_user():

    if 'email' in session:

        user_uuid = request.args.get('uuid')
        
        session_db.run("MATCH (p:Person {uuid: $uuid}) SET p.visible = 0 RETURN p", uuid = user_uuid).data()[0]['p']

        return redirect('/admin')
    
    return redirect('/')




@app.route('/restaure')
def restore_user():

    if 'email' in session:

        user_uuid = request.args.get('uuid')
        
        session_db.run("MATCH (p:Person {uuid: $uuid}) SET p.visible = 1 RETURN p", uuid = user_uuid).data()[0]['p']

        return redirect('/archives')

    return redirect('/')








@app.route('/archives')
def archives():
    if 'email' in session:

        user = api_user(session['email'])
        users = api_users_archiver()


        current_user = {
            'fname' : user['p.name'],
            'lname' : user['p.lname'],
            'email' : session['email'],
            'profile' : user['p.profile']
        }

        return render_template('pages/admin/archive.html', user = current_user, today = date.today().strftime("%d/%m/%Y"), users = users)
    
    return redirect('/')



@app.route('/user', methods=["POST", "GET"])
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
        
        if request.method == "POST":

            fname = request.form.get('fname')
            lname = request.form.get('lname')
            phone = request.form.get('phone')
            email = request.form.get('email')
            job = request.form.get('job')
            age = request.form.get('age')
            sex = request.form.get('sex')

            query = """
                MATCH (p:Person {uuid : $uuid}) SET p += { name : $fname, lname : $lname, email : $email, phone : $phone, job : $job, age : $age, sex : $sex}
            """
            session_db.run(query, uuid = user['p.uuid'], fname = fname, lname = lname, phone = phone, email = email, job = job, age = age, sex = sex)

            return redirect('/user')

        return render_template('pages/user/home.html', user = current_user, today = date.today().strftime("%d/%m/%Y"))
    else:
        return redirect('/')


@app.route('/tree', methods = ["GET", "POST"])
def tree():

    if 'email' in session:

        user = api_user(session['email'])

        print(user['p.name'])
        parents = api_get_parents(user['p.name'])
        gen1, gen2, gen3, gen4 = [], [], [], []

        print(parents)

        for parent in parents:
            if parent['generation'] == "1" :
                gen1.append(parent)

            elif parent['generation'] == "2" :
                gen2.append(parent)

            elif parent['generation'] == "3" :
                gen3.append(parent)

            else :
                gen4.append(parent)

        print("generation 1", gen1)
        print("generation 2", gen2)
        print("generation 3", gen3)
        print(gen4)
        
        current_user = {
            'fname' : user['p.name'],
            'lname' : user['p.lname'],
            'email' : session['email'],
            'profile' : user['p.profile'],
        }

        if request.method == 'POST':
            print('hello')

        return render_template('pages/user/tree.html', user = current_user, today = date.today().strftime("%d/%m/%Y"), gen1 = gen1, gen2 = gen2, gen3 = gen3, gen4 = gen4)
    
    else:
        return redirect('/')




@app.route('/chat')
def chat():

    if 'email' in session:
        user = api_user(session['email'])

        parents = api_get_parents(user['p.name'])

        current_user = {
                'fname' : user['p.name'],
                'lname' : user['p.lname'],
                'email' : session['email'],
                'profile' : user['p.profile'],
        }
        return render_template('pages/user/chat.html', user = current_user, today = date.today().strftime("%d/%m/%Y"), parents = parents)

    return redirect('/')



if __name__=='__main__':

    result = session_db.run("MERGE (p:Person {name : $name, lname : $lname, password : $password, email : $email, profile : $profile})",
        name = "Admin", lname = "admin",
        password = "neo4j", email = "admin@neo.sn", 
        profile = "admin")

    app.run(debug=True,port=5000)