import os
import sshtunnel, pymysql
import time
def show():
    with sshtunnel.SSHTunnelForwarder(("gestion-imdf.ddns.net", 22),
                            ssh_username="alumno6to",
                            ssh_password="Ismdf.309",
                            remote_bind_address=("localhost",3306)) as tunnel:
        
        connection = pymysql.connect(user="jporta553",
                                    password="553Porta",
                                    port=tunnel.local_bind_port,
                                    host="localhost",
                                    database="jporta553")
        if connection is not None:
            cursor = connection.cursor()
            
        cursor.execute('''SELECT nombre,encode,id FROM Persona''')
        
        rows = cursor.fetchall()
        rows = list(rows)
        connection.commit()
        os.system("cls")
        for person in rows:
            print(f"Numero De ID: {person[2]}   Nombre: {person[0]}   Codificacion Biométrica: {person[1]}")
            print()

while True:
    show()
    time.sleep(60)
    