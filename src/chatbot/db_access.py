import pymysql
from sshtunnel import SSHTunnelForwarder
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
            
            cursor.execute('''SELECT (nombre) FROM Persona''')
            
            rows = cursor.fetchall()
            
            connection.commit()
    return rows

def setNewFace(nombre):
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
            
            cursor.execute(f'''INSERT INTO Persona (nombre) VALUES ({nombre})''')
            
            connection.commit()