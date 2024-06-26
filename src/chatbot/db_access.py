import pymysql
import ast, numpy
from sshtunnel import SSHTunnelForwarder
import face_recognition
def getFaces():
    with SSHTunnelForwarder(("gestion-imdf.ddns.net", 22),
                            ssh_username="alumno6to",
                            ssh_password="Ismdf.309",
                            remote_bind_address=("gestion-imdf.ddns.net",3306)) as tunnel:
        
        connection = pymysql.connect(user="jporta553",
                                    password="553Porta",
                                    port=tunnel.local_bind_port,
                                    host="127.0.0.1",
                                    database="jporta553")
        if connection is not None:
            cursor = connection.cursor()
            
            cursor.execute('''SELECT nombre,encode,id FROM Persona''')
            
            rows = cursor.fetchall()
            rows = list(rows)
            connection.commit()
            for i,person in enumerate(rows):
                    rows[i] = list(person)
                    rows[i][1] = numpy.array(eval(person[1]))
    return rows

def setNewFace(nombre,encode):
    with SSHTunnelForwarder(("gestion-imdf.ddns.net", 22),
                            ssh_username="alumno6to",
                            ssh_password="Ismdf.309",
                            remote_bind_address=("gestion-imdf.ddns.net",3306)) as tunnel:
        
        connection = pymysql.connect(user="jporta553",
                                    password="553Porta",
                                    port=tunnel.local_bind_port,
                                    host="127.0.0.1",
                                    database="jporta553")
        
        if connection is not None:
            cursor = connection.cursor()
            encode = str(encode.tolist())    
            cursor.execute('''INSERT INTO Persona (nombre, encode) VALUES (%s, %s)''', (nombre, encode))
            
            connection.commit()
            
def alterFace(nombre,id):
    with SSHTunnelForwarder(("gestion-imdf.ddns.net", 22),
                            ssh_username="alumno6to",
                            ssh_password="Ismdf.309",
                            remote_bind_address=("gestion-imdf.ddns.net",3306)) as tunnel:
        
        connection = pymysql.connect(user="jporta553",
                                    password="553Porta",
                                    port=tunnel.local_bind_port,
                                    host="127.0.0.1",
                                    database="jporta553")
        
        if connection is not None:
            cursor = connection.cursor() 
            cursor.execute('''UPDATE Persona SET nombre = (%s) WHERE id = (%s); ''', (nombre, id))
            
            connection.commit()
            

            