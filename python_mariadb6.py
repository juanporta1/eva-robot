
import pymysql
from sshtunnel import SSHTunnelForwarder

_host = 'gestion-imdf.ddns.net'
_ssh_port = 22
_username = 'alumno6to'
_password = 'Ismdf.309'
_remote_bind_address = '127.0.0.1'
_remote_mysql_port = 3306
_local_bind_address = '127.0.0.1'
_local_mysql_port = 3306
_db_user = 'snegrette269' 
_db_password = '269Negrette'
_db_name = 'snegrette269'

with SSHTunnelForwarder(
        ('gestion-imdf.ddns.net', 22),
        ssh_username='alumno6to', ssh_password='Ismdf.309',
        remote_bind_address=('gestion-imdf.ddns.net', 3306)
    ) as tunnel:
        connection =pymysql.connect(
            user='snegrette269', password='269Negrette',
            host='127.0.0.1', port=tunnel.local_bind_port,
            database='snegrette269'
        )
        if(connection is not None):
            cur = connection.cursor()
            ####### ACÁ VIENE LA INSTRUCCION SQL QUE QUERÉS EJECUTAR ######
            sql="select * from 00002AUTOR"
            ####### ACÁ SE EJECUTA ######
            cur.execute(sql)
            ####### RECUPERA LAS FILAS COMO UNA LISTA ######
            rows = cur.fetchall()
            ####### COMMIT (CONFIRMA) LA TRANSACCION ######
            connection.commit()
            ####### MUESTRA LOS REGISTROS ######
            print(" ")
            print("Toda la lista en una sola línea:")
            print(rows)
            ####### RECORRO LA LISTA ######

            print(" ")
            print("Toda la lista en líneas separadas, registro x registro:")
            for i in rows:
                  print(i)

        connection.close()