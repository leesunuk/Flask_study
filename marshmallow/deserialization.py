from marshmallow import Schema, fields
from serialization import animal
import json

JSON_animal_data = {"species" : "parrot",
                    "name" : "Camem",
                    "age" : 1,
                    "gender" : "male",
                    }

class AnimalSchema(Schema):
    species = fields.String()
    name = fields.String()
    age = fields.String()
    gender = fields.String()
    
send_animal_data = AnimalSchema()

data = send_animal_data.load(JSON_animal_data)
animal_object = animal(**data)

print(animal_object)