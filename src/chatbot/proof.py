import sshtunnel, pymysql

with sshtunnel.SSHTunnelForwarder(("gestion-imdf.ddns.net", 22),
                            ssh_username="alumno6to",
                            ssh_password="Ismdf.309",
                            remote_bind_address=("gestion-imdf.ddns.net",3306)) as tunnel:
        
        connection = pymysql.connect(user="jporta553",
                                    password="553Porta",
                                    port=tunnel.local_bind_port,
                                    host="localhost",
                                    database="jporta553")
        print(connection)
        if connection is not None:
            cursor = connection.cursor()
            