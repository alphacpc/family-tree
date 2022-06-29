from flask import Blueprint, render_template, request, jsonify, session, redirect
from neo4j import GraphDatabase
import uuid
from datetime import datetime

driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "connect"))
session_db = driver.session()



api = Blueprint('api', __name__) 


###############################################################
######## APIs | GET | ARCHIVES | UPDATE | DELETE ##############
###############################################################
def api_register(fname, lname, email, password):

    if fname and lname and email and password:

        uid = str(uuid.uuid1())
        

        query = ("""MERGE (p1:Person { 
            name: $fname , lname : $lname, 
            email : $email, password : $password, 
            profile : $profile , visible : $visible, 
            createdAt : $date,
            uuid : $uid
        })""")

        session_db.run(query, fname = fname, lname = lname, email = email, password = password, profile = "user", visible = 1, date = datetime.now(), uid= uid)

        return True
    
    else : 
        return False


def api_logout():
    session.clear()
    return redirect('/')
        


def api_add_user():
    fname = request.get_json().get('fname')
    lname = request.get_json().get('lname')
    email = request.get_json().get('email')
    mdp = request.get_json().get('mdp')


    if fname and lname and email and mdp :

        uid = str(uuid.uuid1())

        query = ("""MERGE (:Person { 
            name: $fname , lname : $lname, 
            email : $email, password : $password, 
            profile : $profile , visible : $visible, 
            createdAt : $date,
            uuid : $uid
        })""")

        session_db.run(query, fname = fname, lname = lname, email = email, password = mdp, profile = "user", visible = 1, date = datetime.now(), uid= uid)

        result = session_db.run("MATCH (p:Person {profile : 'user', email : $email}) RETURN p.name, p.lname, p.email, p.uuid", email = email).data() 

        return {'message' : 'Utilisateur ajouté avec succès !', 'type': True, 'data' : result}, 201

        # return redirect('/admin')
    
    else : 
        return {'message' : 'Veuillez vérifier les informations saisies !', 'type': False}, 401


def api_add_member():
    fname = request.get_json().get('fname')
    lname = request.get_json().get('lname')
    lien = request.get_json().get('lien')


    if fname and lname and lien :
        print("Valeur  saisi : ", fname, lname, lien)

        query = (
            "MATCH (p1:Person { name: $current_user})"
            "MERGE (p2:Person { name: $fname , lname : $lname })"
            "MERGE (p1)-[:LIEN {lien : $lien}]->(p2)"
        )

        session_db.run(query, current_user = "Astou", fname = fname, lname = lname, lien = lien)

        return {'message' : 'Membre ajouté avec succès !', 'type': True}, 201
    
    else : 
        return {'message' : 'Veuillez vérifier les informations saisies !', 'type': False}, 401



def api_users():

    result = session_db.run("MATCH (p:Person {profile : 'user', visible : 1}) RETURN p.name, p.lname, p.email, p.uuid LIMIT 200").data() 

    return result



def api_users_archiver():
    
    result = session_db.run("MATCH (p:Person {profile : 'user', visible : 0}) RETURN p.name, p.lname, p.email, p.uuid LIMIT 200").data() 

    return result



def api_user(email, type = "user"):

    if type == "login":
        query = "MATCH (p:Person {email : $email}) RETURN p.email, p.password, p.profile"
    
    elif type == "register":
        query = "MATCH (p:Person {email : $email}) RETURN p"
    
    else:
        query = "MATCH (p:Person {email : $email}) RETURN p.name, p.lname, p.email, p.profile, p.password, p.job, p.age, p.sex, p.phone, p.uuid"

    result = session_db.run(query, email= email)  
    user = result.data()

    if user :
        return user[0]

    else :
        return None













def api_user_tree():
    
    result = session_db.run("MATCH (p:Person) RETURN p LIMIT 4")

    print(result.data())

    for user in result:
        print(user)

    return {"data": 'Tree loaded'}




api.route('/api/register/', methods=["POST"])(api_register)

# api.route('/api/login/', methods=["POST"])(api_login)

api.route('/api/logout/')(api_logout)

api.route('/api/user/', methods=["POST"])(api_add_user)

api.route('/api/member/', methods=["POST"])(api_add_member)

api.route('/api/users')(api_users)

api.route('/api/user')(api_user)

api.route('/api/user/tree')(api_user_tree)

