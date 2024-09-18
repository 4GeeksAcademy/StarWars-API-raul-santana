from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planets_favorites = db.relationship('FavoritePlanets', back_populates='user_relationship')
    character_favorites = db.relationship('FavoriteCharacter', back_populates='user_relationship')

    def __repr__(self):
        return f'User con id {self.id} y email {self.email}'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column (db.Integer, nullable=False)
    characters = db.relationship('Character', back_populates='planet')
    favorite_by = db.relationship('FavoritePlanets', back_populates='planet_relationship')

    def __repr__(self):
        return f'El planeta se llama {self.name} y su poblacion es {self.population}'
    
    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "population":self.population
        }
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    species = db.Column(db.String(50), unique=False, nullable=False)
    birthYear = db.Column(db.String(50), unique=False, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))  
    planet = db.relationship('Planet', back_populates='characters')
    character_by = db.relationship('FavoriteCharacter', back_populates='character_relationship')
    
    def __repr__(self):
        return f'Character con id {self.id} name {self.name} species {self.species} birth_Year {self.birthYear}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "birthYear": self.birthYear
        }
    
class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_relationship = db.relationship('User', back_populates='planets_favorites')
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet_relationship = db.relationship('Planet', back_populates='favorite_by')

    def __repr__(self):
        return f'(El usuario {self.user_id} le gusta el planeta {self.planet_id})'
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id
        }
    
class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_relationship = db.relationship('User', back_populates='character_favorites')
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character_relationship = db.relationship('Character', back_populates='character_by')

    def __repr__(self):
        return f'(El usuario {self.user_id} le gusta el character {self.character_id})'
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id
        }
