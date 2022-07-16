from flask import request, session, render_template, redirect
from apis.route import api_user, api_register


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

