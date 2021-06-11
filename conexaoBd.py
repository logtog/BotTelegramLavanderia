#-- coding: utf-8 --
import pymysql #biblioteca de Conexao com o mysql

class Conexao():
    def verifica_login(self, chatid):
        conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                               password=None, db='usuarios_telegram')
        cur = conn.cursor()
        cur.execute(f'SELECT nome_usuario FROM usuario where chatid_usuario = {chatid}')
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            user = user[0].split()
            return True, user[0]
        else:
            return False, False

    def cadastro(self,nome, chatid, email, rua, numero, bairro):
        conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                               password=None, db='usuarios_telegram')
        cur = conn.cursor()
        sql = f'INSERT INTO `usuario`(`nome_usuario`, `chatid_usuario`, `email_usuario`, `rua_usuario`, `numero_usuario`, `bairro_usuario`) VALUES (%s,%s,%s,%s,%s,%s)'
        val = nome, str(chatid), email, rua, str(numero), bairro
        cur.execute(sql, val)
        conn.commit()
        cur.close()
        conn.close()
        nome = nome.split(' ')
        print(f'O {chatid} acabou de ser cadastrado como: ' + nome[0])

    def retorna_id(self,chatid):
        conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                               password=None, db='usuarios_telegram')
        cur = conn.cursor()
        cur.execute(f'SELECT id_usuario FROM usuario where chatid_usuario = {chatid}')
        id = cur.fetchone()
        cur.close()
        conn.close()
        return id