from dataclasses import field
from marshmallow import Schema, fields
class animal:
    def __init__(self, species, name, age, gender):
        self.species = species #종류
        self.name = name #이름
        self.age = age #나이
        self.gender = gender #성
        
my_pet = animal(
    "parrot",
    "Camem",
    "1",
    "male"
)

introduction_my_pet = {"species" : my_pet.__dict__['species'],
                       "name" : my_pet.__dict__['name'],
                       "age" : my_pet.__dict__['age'],
                       "gender" : my_pet.__dict__['gender'],
    
}
#print(introduction_my_pet)

class AnimalSchema(Schema):
    species = fields.String()
    name = fields.String()
    age = fields.String()
    gender = fields.String()
    
send_animal_data = AnimalSchema()

Camem_data = send_animal_data.dump(my_pet)
import json
# print(json.dumps(Camem_data))
