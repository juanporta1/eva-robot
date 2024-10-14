import json
import numpy

def getFaces():
    with open("src/chatbot/faces.json","r") as f:
        rows = json.load(f)
        newRows = []
        for i,person in enumerate(rows):
                newRows[i] = list(person)
                newRows[i][1] = numpy.array(eval(person[1]))
    return newRows

def setNewFace(nombre,encode):
    with open("src/chatbot/faces.json","r+") as f:
        rows = json.load(f)
        rows[f"{len(rows)}"] = [nombre,encode]
        f.seek(0)  
        json.dump(rows, f, indent=4)  
        f.truncate()           
        
def alterFace(nombre,id):
    with open("src/chatbot/faces.json","r+") as f:
        rows = json.load(f)
        rows[f"{id}"][0] = nombre
        
        f.seek(0)  
        json.dump(rows, f, indent=4)  
        f.truncate()            
