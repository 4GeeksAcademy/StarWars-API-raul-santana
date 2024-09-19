"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet,Character,FavoritePlanets, FavoriteCharacter
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    all_users_serialize = []

    for user in all_users:
        all_users_serialize.append(user.serialize())

    response_body = {
        "msg": "Hello, this is your GET /users response ",
        "data": all_users_serialize
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    single_user = User.query.get(user_id)
    if single_user is None:
        return jsonify({'msg': f'El usuario con este id {user_id} no existe'})
    print(type(single_user))
    return jsonify({'msg': 'Este es el usuario', 'data': single_user.serialize()}),200

@app.route('/planet', methods=['GET'])
def get_planet():
    all_planets = Planet.query.all()
    all_planets_serialize = []

    for planet in all_planets:
        all_planets_serialize.append(planet.serialize())

    response_body = {
        "msg": "Hello, this is your GET /planet response ",
        "data": all_planets_serialize
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    single_planet = Planet.query.get(planet_id)
    if single_planet is None:
        return jsonify({'msg': f'El planeta con este id {planet_id} no existe'})
    return jsonify({'msg': 'Este es el planet', 'data': single_planet.serialize()}),200

@app.route('/character', methods=['GET'])
def get_character():
    all_characters = Character.query.all()
    all_characters_serialize = []

    for character in all_characters:
        all_characters_serialize.append(character.serialize())

    response_body = {
        "msg": "Hello, this is your GET /character response ",
        "data": all_characters_serialize
    }
    return jsonify(response_body), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    single_character = Character.query.get(character_id)
    if single_character is None:
        return jsonify({'msg': f'El character  con este id {character_id} no existe'})
    return jsonify({'msg': 'Este es el character', 'data': single_character.serialize()}),200

@app.route('/user', methods=['POST'])
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Debes enviar informacion en el body'})
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = body['is_active']
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': '¡Usuario creado!',
                    'data': new_user.serialize()})

@app.route('/planet', methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Debes enviar informacion en el body'})
    new_planet = Planet()
    new_planet.name = body['name']
    new_planet.population = body['population']
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'msg': '¡Nuevo planeta creado!',
                    'data': new_planet.serialize()})

@app.route('/character', methods=['POST'])
def add_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Debes enviar informacion en el body'})
    new_character = Character()
    new_character.name = body['name']
    new_character.species = body['species']
    new_character.birthYear = body['birthYear']
    
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'msg': '¡Nuevo character ha sido creado!',
                    'data': new_character.serialize()})

@app.route('/user/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    body = request.get_json(silent=True)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}),404
    if "email" in body:
        user.email = body["email"]
    if "password" in body:
        user.password = body["password"]
    if "is_active" in body:
        user.is_active = body["is_active"]
    
    db.session.commit()
    return jsonify({'msg':'El usuario ha sido modificado'})

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def put_planet(planet_id):
    body = request.get_json(silent=True)
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}),404
    if "name" in body:
        planet.name = body["name"]
    if "population" in body:
        planet.population = body["population"]
     
    db.session.commit()
    return jsonify({'msg':'El planet ha sido modificado'})

@app.route('/character/<int:character_id>', methods=['PUT'])
def put_character(character_id):
    body = request.get_json(silent=True)
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({'msg': 'character not found'}),404
    if "name" in body:
        character.name = body["name"]
    if "species" in body:
        character.species = body["species"]
    if "birthYear" in body:
        character.birthYear = body["birthYear"]
     
    db.session.commit()
    return jsonify({'msg':'El character ha sido modificado'})

@app.route('/user/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}),404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': ' El usuario se ha eliminado correctamente'})

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def del_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'User not found'}),404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': ' El planeta se ha eliminado correctamente'})

@app.route('/character/<int:character_id>', methods=['DELETE'])
def del_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({'msg': 'User not found'}),404
    db.session.delete(character)
    db.session.commit()
    return jsonify({'msg': ' character eliminado correctamente'})

@app.route('/user/<int:id_user>/favorites', methods=['GET'])
def get_favorites(id_user):
    favorite_planets = FavoritePlanets.query.filter_by(user_id = id_user).all()
    favorite_planets_serialize = []
    for fav in favorite_planets:
        favorite_planets_serialize.append(fav.planet_relationship.serialize())
    return jsonify({'msg': 'ok',
                    'data':{
                        'favorite_planets': favorite_planets_serialize,
                        'favorite_character': 'info de los personajes favoritos'
                    }})

@app.route('/favorite/planet/<int:id_planet>/<int:user_id>', methods=['POST'])
def post_favorites(id_planet, user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con el {user_id} no se encuentra'}),404
    planet = Planet.query.get(id_planet)
    if planet is None:
        return jsonify({'msg': f'El planeta con el {id_planet} no se encuentra'}),404
    existing_favorite = FavoritePlanets.query.filter_by(planet_id = id_planet, user_id = user_id).all()
    if existing_favorite:
        return jsonify({'msg': 'El planeta ya esta en la lista de favoritos'}),400
    new_favorite = FavoritePlanets(planet_id = id_planet, user_id = user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify ({'msg': 'Planeta añadido a favoritos',
                     'data':new_favorite.serialize()})

@app.route('/favorite/character/<int:id_character>/<int:user_id>', methods=['POST'])
def post_character(id_character, user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con el {user_id} no se encuentra'}),404
    character = Character.query.get(id_character)
    if character is None:
        return jsonify({'msg': f'El character con el {id_character} no se encuentra'}),404
    existing_favorite = FavoriteCharacter.query.filter_by(character_id = id_character, user_id = user_id).all()
    if existing_favorite:
        return jsonify({'msg': 'El charactera ya esta en la lista de favoritos'}),400
    new_favorite = FavoriteCharacter(character_id = id_character, user_id = user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify ({'msg': 'character añadido a favoritos',
                     'data':new_favorite.serialize()})    

@app.route('/favorite/planet/<int:id_planet>/<int:user_id>', methods=['DELETE'])
def del_planet_favorites(id_planet, user_id):
    planet = Planet.query.get(id_planet)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}),404
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}),404
    favorite = FavoritePlanets.query.filter_by(planet_id = id_planet, user_id = user_id).first()
    if favorite is None:
        return jsonify({'msg': 'El planeta no esta en la lista de favoritos del usuario'})
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': ' planeta eliminado correctamente de los favoritos'})

@app.route('/favorite/character/<int:id_character>/<int:user_id>', methods=['DELETE'])
def del_character_favorites(id_character, user_id):
    character = Character.query.get(id_character)
    if character is None:
        return jsonify({'msg': 'character not found'}),404
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}),404
    favorite = FavoriteCharacter.query.filter_by(character_id = id_character, user_id = user_id).first()
    if favorite is None:
        return jsonify({'msg': 'El character no esta en la lista de favoritos del usuario'})
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': ' character eliminado correctamente de los favoritos'})

## [DELETE] /favorite/character/<int:people_id>

# this only runs if `$ python src/app.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
