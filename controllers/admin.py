from flask import session, render_template, redirect, request
from apis.route import api_users, api_user, api_get_parents, api_users_archiver
from config import session_db
from datetime import date


#PAGE D'ACCUEIL
def home():
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



#PAGE EDIT USER
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



#PAGE DETAIL USER
def detail_user():

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

        parents = api_get_parents(user_edit['name'])
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

        return render_template('pages/admin/detail.html', user = current_user, user_edit = user_edit, today = date.today().strftime("%d/%m/%Y") , gen1 = gen1, gen2 = gen2, gen3 = gen3, gen4 = gen4)

    else:
        return redirect('/')



#PAGE ARCHIVE USER
def archive_user():

    if 'email' in session:

        user_uuid = request.args.get('uuid')
        
        session_db.run("MATCH (p:Person {uuid: $uuid}) SET p.visible = 0 RETURN p", uuid = user_uuid).data()[0]['p']

        return redirect('/admin')
    
    return redirect('/')



#API RESTAURE USER
def restore_user():

    if 'email' in session:

        user_uuid = request.args.get('uuid')
        
        session_db.run("MATCH (p:Person {uuid: $uuid}) SET p.visible = 1 RETURN p", uuid = user_uuid).data()[0]['p']

        return redirect('/archives')

    return redirect('/')


#PAGE DES ARCHIVES
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
