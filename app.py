from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient
import os
import pandas as pd
from dotenv import load_dotenv
import json
from bson import ObjectId
from flask_cors import CORS

from Student import Student
from Teacher import Teacher
from Point import Point
from Cours import Cours
from Room import Room
from Program import Program


load_dotenv()
MONGO_URI = os.environ.get('MONGO_URI')

# Init app
app = Flask(__name__)
CORS(app)

# Variables 
rows, cols = (10, 5)
headers = ["Lundi", "Mardi", "Mercredi", "jeudi","vendredi"]
teachers_array = []
program_courses = []
final_schedule = pd.DataFrame([["-Not Avail-"] * 5 for _ in range(10)], columns = headers)
avail_schedule = [[0]*cols]*rows
rooms_array = []
class MongoApiUsers:
    def __init__(self, data):
        self.client = MongoClient(MONGO_URI)  
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read_student(self):
        documents = self.collection.find()
        output = [{**data, '_id': str(data['_id'])} for data in documents]
        print(output)
        return output
    
    def read_workers(self):
        query = {'isWorker': True}
        documents = self.collection.find(query)
        output = [{**data, '_id': str(data['_id'])} for data in documents]
        for elt in output:
            for data in elt.get('availablity')['index']:
            # Supprimer l'attribut _id du document
                data.pop('_id', None)
            for data in elt.get('planning')['schedule']:
            # Supprimer l'attribut _id du document
                data.pop('_id', None)
            for data in elt.get('skills'):
            # Supprimer l'attribut _id du document
            # Ajout des skills dans le tableau
                data.pop('_id', None)
        for elt in output:
            skills = []
            for data in elt.get('skills'):
            # Supprimer l'attribut _id du document
            # Ajout des skills dans le tableau
                skills.append(Cours(data['course']))
            teachers_array.append(Teacher(elt.get('name'),skills,convert_to_int(elt.get('availablity')['index'])))
    
    def read_one(self, document_id):
        # Convertir la chaîne document_id en un objet ObjectId
        document_id = ObjectId(document_id)
        
        # Rechercher le document avec l'_id spécifié
        document = self.collection.find_one({'_id': document_id})
        # print(document)
        # Vérifier si le document a été trouvé
        if document:
            # Convertir l'objet '_id' en une chaîne de caractères
            document['_id'] = str(document['_id'])
            return document
        else:
            return None  # Le document avec l'_id spécifié n'a pas été trouvé
        
class MongoApiProgram:
    def __init__(self, data):
        self.client = MongoClient(MONGO_URI)  
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data
    
    def getProgramByName(self,name):
        query = {'name': name}
        documents = self.collection.find(query)
        output = [{**data, '_id': str(data['_id'])} for data in documents]
        session_courses = []
        if output:
            for data in output[0].get('list_courses'):
                session_courses.append(Cours(data['course'],int(data['t_hours']),int(data['weight'])))    
        # Supprimer l'attribut _id du document
                data.pop('_id', None)
        else:
             print("Aucun document trouvé avec ce nom.")
        if output:       
            program_courses.append(Program(output[0].get('name'),session_courses))   
            print('PROGRAM ',program_courses[0].session_course[0].h_t)
        else:
            print("Aucun document trouvé avec ce nom.")

class MongoApiRoom:
    def __init__(self, data):
        self.client = MongoClient(MONGO_URI)  
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data
    
    def getRooms(self):
        
        documents = self.collection.find()
        output = [{**data, '_id': str(data['_id'])} for data in documents]
        if output:
            for data in output:  
        # Supprimer l'attribut _id du document
                rooms_array.append(Room(data['name']))
                data.pop('_id', None)
                data.pop('__v', None)
        else:
             print("Aucun document trouvé avec ce nom.")
        if output:       
             print('')
        else:
            print("Aucun document trouvé avec ce nom.")
            
# if __name__ == '__main__':
#     data = {
#         "database": "test",
#         "collection": "users",
#     }
#     mongo_obj = MongoApiUsers(data)
#     some = mongo_obj.read()
#     print(some[0]['name'])
#     # print(json.dumps(mongo_obj.read(), indent=4))

def getSpecific(*arr,id):
    for i in (0,arr):
        if arr[i]['_id'] == id:
            return arr[i]

def array_to_json_2d(arr):
    json_objects = []
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            json_obj = {
                'x': x,
                'y': y,
                'z': arr[x][y]
            }
            json_objects.append(json_obj)
    return json_objects

def convert_to_int(data):
    converted_data = []
    
    for entry in data:
        converted_entry = {
             'x': int(entry['x']),
             'y': int(entry['y']),
             'z': entry['z']  # Conserve z tel quel
        }
        converted_data.append(converted_entry)
    
    return converted_data

def makeSchedule():
    teachers = teachers_array
    program = program_courses[0]
    for i in range(0,len(teachers)):
        for j in range(0,len(program.session_course)):
            for b in range(0,len(teachers[i].skills)):
                if teachers[i].skills[b].name == program.session_course[j].name:
                    print(teachers[i].skills[b].name," VS ", program.session_course[j].name)
                    new_av = []  
                    print(teachers[i].name, ' is able to do this course ',program.session_course[j].name)
                    for h in range(0,5):
                        for d in range(0,10):
                            print(teachers[i].availability.values[d,h])
                            if teachers[i].availability.values[d,h] == 1:
                                if program.session_course[j].h_t > 0:
                                     teachers[i].availability.values[d,h] = 0
                                     program.session_course[j].h_t -= 1
                                     print(program.session_course[j].name)
                                     final_schedule.values[d,h] = program.session_course[j].name + ' ' + teachers[i].name             
    print(final_schedule)  

@app.route('/<name>',methods=['GET'])
def get(name): 
    Users = MongoApiUsers({
        "database": "test",
        "collection": "users",
    })
    Programs = MongoApiProgram({
        "database": "test",
        "collection": "programs"
    })
    Rooms = MongoApiRoom({
        "database": "test",
        "collection": "rooms"
    })
    Users.read_workers()
    Programs.getProgramByName(name)
    Rooms.getRooms()
    makeSchedule()
    output_json = array_to_json_2d(final_schedule.values)
    print(output_json)
    return (output_json)
    

# Run Server
if __name__ == '__main__':
    app.run(debug=True,port=5002)





