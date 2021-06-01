import pymysql
class conexao():
    def __init__(self,conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
        password=None,
        db='usuarios_telegram')):
        self.conn = conn
    def conectar(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM usuario WHERE id_usuario = 1')
        print(cur.fetch())
        cur.close()
        self.conn.close()

