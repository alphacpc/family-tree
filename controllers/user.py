from flask import session, render_template, redirect, request
from apis.route import api_user, api_get_parents
from config import session_db
from datetime import date



# PAGE D'ACCUEIL
def home():

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


# PAGE FAMILY TREE
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




# PAGE DE CHAT
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