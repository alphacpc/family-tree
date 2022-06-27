from flask import Blueprint, request
from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "connect"))
session = driver.session()



api = Blueprint('api', __name__) 


###############################################################
######## APIs | GET | ARCHIVES | UPDATE | DELETE ##############
###############################################################
def api_register():

    fname = request.get_json().get('fname')
    lname = request.get_json().get('lname')
    email = request.get_json().get('email')
    password = request.get_json().get('mdp')

    if fname and lname and email and password :

        query = ("MERGE (p1:Person { name: $fname , lname : $lname, email : $email, password : $password, profile : $profile })")

        session.run(query, fname = fname, lname = lname, email = email, password = password, profile = "user")

        return {'message' : 'Ajout avec succès !', 'type': True}, 201
    
    else : 
        return {'message' : 'Veuillez remplire tous les champs !', 'type': False}, 401



def api_login():
    
    email = request.get_json().get('email')
    password = request.get_json().get('mdp')

    if email and password and len(email) > 4:
        return {"message" : "Success !", "type": True}, 201
    
    else : 
        return {"message" : "Cet utilisateur n'existe pas !", "type": False}, 401
        


def api_add_user():
    fname = request.get_json().get('fname')
    lname = request.get_json().get('lname')
    email = request.get_json().get('email')
    mdp = request.get_json().get('mdp')


    if fname and lname and email and mdp :
        print("Valeur  saisi : ", fname, lname, email, mdp)

        query = ("MERGE (p1:Person { name: $fname , lname : $lname, email : $email, password : $password, profile = $profile })")

        session.run(query, fname = fname, lname = lname, email = email, password = mdp, profile = "user")

        return {'message' : 'Utilisateur ajouté avec succès !', 'type': True}, 201
    
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
            "MERGE (p1)-[:" + lien.upper() + "]->(p2)"
        )

        session.run(query, current_user = "ousmane", fname = fname, lname = lname)

        return {'message' : 'Membre ajouté avec succès !', 'type': True}, 201
    
    else : 
        return {'message' : 'Veuillez vérifier les informations saisies !', 'type': False}, 401



def api_users():

    result = session.run("MATCH (p:Person) RETURN p.name, p.lname, p.email, p.id")

    for user in result:
        print(user)

    return {"data": 'Users loaded'}




def api_user():

    result = session.run("MATCH (p:Person {name : $name}) RETURN p.name, p.lname, p.email, p.id", name="Alpha")

    for user in result:
        print(user)

    return {"data": 'Single user loaded'}


def api_user_tree():
    
    result = session.run("MATCH (p:Person) RETURN p LIMIT 4")

    print(result)

    for user in result:
        print(user)

    return {"data": 'Tree loaded'}


api.route('/api/register/', methods=["POST"])(api_register)

api.route('/api/login/', methods=["POST"])(api_login)

api.route('/api/user/', methods=["POST"])(api_add_user)

api.route('/api/member/', methods=["POST"])(api_add_member)

api.route('/api/users')(api_users)

api.route('/api/user')(api_user)

api.route('/api/user/tree')(api_user_tree)

