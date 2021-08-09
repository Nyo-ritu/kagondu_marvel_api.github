from secrets import token_urlsafe
from flask import Blueprint
from flask.json import jsonify, request, jsonify
from flask.wrappers import Response
from marvel_api.helpers  import token_required
from marvel_api.models import db, User, Character, character_schema, characters_schema



api = Blueprint('api', __name__, url_prefix='/api' )

@api.route('/getdata')
def getdata():
    return {'some_value': 99, 'another_value': 500}

#CREATE Character ENDPOINT

@api.route('/character', methods = ['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    superpower = request.json['superpower']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    character = Character(name, description, comics_appeared_in, superpower, user_token = user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# retrieve all characters

@api.route('/character', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

    
# retrieve single character

@api.route('/character/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    character = Character.query.get(id)
    response = character_schema.dump(character)
    return jsonify(response)

# update a character by ID Endpoint

@api.route('/character/<id>', methods = ['POST'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id)
    print(character)
    if character:
        character.name = request.json['name']
        character.description = request.json['description']
        character.comics_appeared_in = request.json['comics_appeared_in']
        character.superpower = request.json['superpower']
        character.date_created = request.json['date_created']
        character.user_token = current_user_token.token
        db.session.commit()

        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That character does not exist!'})


# Delete character by ID

@api.route('/character/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    if character:
        db.session.delete(character)
        db.session.commit()

        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That drone does not exist!'})

