from flask import Blueprint, request



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
        return {'message' : 'Ajout avec succès !', 'type': True}, 201
    
    else : 
        return {'message' : 'Veuillez remplire tous les champs ! from Back', 'type': False}, 401



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
        return {'message' : 'Utilisateur ajouté avec succès !', 'type': True}, 201
    
    else : 
        return {'message' : 'Veuillez vérifier les informations saisies !', 'type': False}, 401


def api_add_member():
    fname = request.get_json().get('fname')
    lname = request.get_json().get('lname')
    lien = request.get_json().get('lien')


    if fname and lname and lien :
        print("Valeur  saisi : ", fname, lname, lien)
        return {'message' : 'Membre ajouté avec succès !', 'type': True}, 201
    
    else : 
        return {'message' : 'Veuillez vérifier les informations saisies !', 'type': False}, 401





api.route('/api/register/', methods=["POST"])(api_register)

api.route('/api/login/', methods=["POST"])(api_login)

api.route('/api/user/', methods=["POST"])(api_add_user)

api.route('/api/member/', methods=["POST"])(api_add_member)
