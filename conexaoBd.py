# -- coding: utf-8 --
import pymysql  # biblioteca de Conexao com o mysql
import data

data = data.Data()


class Conexao:
    @staticmethod
    def verifica_login(chatid):
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

    @staticmethod
    def cadastro_cliente(nome, chatid, email, rua, numero, bairro):
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

    @staticmethod
    def retorna_id(chatid):
        conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                               password=None, db='usuarios_telegram')
        cur = conn.cursor()
        cur.execute(f'SELECT id_usuario FROM usuario where chatid_usuario = {chatid}')
        id = cur.fetchone()
        cur.close()
        conn.close()
        return id

    @staticmethod
    def cadastro_pedido_reserva(id_usuario, tipo_pedido, metodo_pedido, dia_pedido, hora_pedido):
        try:
            hoje = data.datetime()
            agendamento_pedido = hoje.replace(day=int(dia_pedido), hour=int(hora_pedido), minute=0, second=0)

            status_pedido = 'Aguardando'

            conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                                   password=None, db='usuarios_telegram')
            cur = conn.cursor()
            sql = f'INSERT INTO pedidos(fk_id_usuario, data_pedido, tipo_pedido, metodo_pedido, agendamento_pedido, status_pedido) VALUES (%s,%s,%s,%s,%s,%s)'
            val = (
                str(id_usuario), str(hoje), str(tipo_pedido), str(metodo_pedido), str(agendamento_pedido),
                status_pedido)
            cur.execute(sql, val)
            conn.commit()
            cur.close()
            conn.close()

            return True
        except Exception as a:
            print(a)
            return False

    @staticmethod
    def cadastro_pedido_coleta(id_usuario, tipo_usuario, metodo_usuario):
        try:
            hoje = data.datetime()

            status_pedido = 'Aguardando'

            conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                                   password=None, db='usuarios_telegram')
            cur = conn.cursor()
            sql = f'INSERT INTO pedidos(fk_id_usuario, data_pedido, tipo_pedido, metodo_pedido,status_pedido) VALUES (%s, %s, %s, %s, %s)'
            val = (str(id_usuario), str(hoje), str(tipo_usuario), str(metodo_usuario), str(status_pedido))
            cur.execute(sql, val)
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as a:
            print(a)
            return False

    @staticmethod
    def retorna_pedidos(id):
        conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                               password=None, db='usuarios_telegram')
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM pedidos where id_usuario = {id}')
        pedidos = cur.fetchall()
        cur.close()
        conn.close()
        if pedidos:
            return pedidos
        else:
            return False

    @staticmethod
    def admin(chatid):
        try:
            conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                               password=None, db='usuarios_telegram')
            cur = conn.cursor()
            cur.execute(f'SELECT chatid_usuario FROM usuario where chatid_usuario = {chatid} AND permissao = "admin"')
            permissao = cur.fetchone()
            cur.close()
            conn.close()
            if permissao:
                return True, chatid
            else:
                return False, False
        except Exception as a:
            print(a)

    @staticmethod
    def retorna_admins():
        try:
            conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                               password=None, db='usuarios_telegram')
            cur = conn.cursor()
            cur.execute(f'SELECT chatid_usuario FROM usuario where permissao = "admin"')
            chatid = cur.fetchall()
            cur.close()
            conn.close()
            if chatid:
                return chatid
            else:
                return False
        except Exception as a:
            print(a)

    @staticmethod
    def retorna_pedidos_admin(tipo):
        try:
            conn = pymysql.connect(host='127.0.0.1', unix_socket='/opt/lampp/var/mysql/mysql.sock', user='root',
                                   password=None, db='usuarios_telegram')
            cur = conn.cursor()
            cur.execute(f'SELECT id_pedido, usuario.chatid_usuario as chatid, usuario.nome_usuario as nome, tipo_pedido, data_pedido, metodo_pedido, agendamento_pedido, status_pedido FROM pedidos INNER JOIN usuario on id_usuario = fk_id_usuario where status_pedido = "{tipo}"')
            pedidos = cur.fetchall()
            cur.close()
            conn.close()
            if pedidos:
                return pedidos
            else:
                return False
        except Exception as a:
            print(a)