# -- coding: utf-8 --
from conexaoBd import Conexao
import telebot
from telebot import types
from data import Data
import time

data = Data()
conexao = Conexao()
user_dict = {}
order_dict = {}
interact_dict = {}
API_TOKEN = '1850427397:AAEqnBDE43H_OitumWDVyogxI18DUa3ErUE'
bot = telebot.TeleBot(API_TOKEN, parse_mode=None)


class User:
    def __init__(self, name):
        self.nome_usuario = name
        self.email_usuario = None
        self.rua_usuario = None
        self.numero_usuario = None
        self.bairro_usuario = None


class Order:
    def __init__(self, id):
        self.id = id
        self.tipo = None
        self.metodo = None
        self.dia = None
        self.hora = None


class InteractAdmin:
    def __init__(self, um_todos):
        self.um_todos = um_todos
        self.id_usuario = None
        self.id_pedido = None
        self.tipo_pedido = None
        self.tipo_mudanca = None
        self.mensagem = None


@bot.message_handler(commands=['start'])
def welcome_message(message):
    try:
        global resgate
        resgate = message
        chatid = message.chat.id
        global usuario
        cadastro, usuario = conexao.verifica_login(chatid)
        if cadastro:
            print(f'{usuario} acabou de iniciar o chat')
            bot.reply_to(message, f'Olá, {usuario}! O que gostaria de fazer hoje?\nO ID da conversa é: {chatid} 🥳🥳')
            bot.send_message(chatid,
                             'Digite uma das opções:\n\n/lavar - realiza um novo pedido\n/pedidos -'
                             ' verifica o status de todos os seus pedidos anteriores.')

            @bot.message_handler(commands=['lavar'])
            def inicia_compra(message):
                compra = Lavar()
                compra.realiza_compra(message)

            @bot.message_handler(commands=['pedidos'])
            def inicia_pedidos(message):
                pedido = Pedidos()
                pedido.verifica_pedidos(message)

            permissao, admin_id = conexao.admin(chatid)
            if permissao:
                bot.send_message(chatid,
                                 'Digite:\n\n/pedidosAdmin - verifica os pedidos\n/interagirAdmin - muda o status dos pedidos\n'
                                 '/mensagemAdmin - manda mensagem para cliente sobre o pedido\n'
                                 '/clienteAdmin - mostra cadastro do cliente pelo Id do produto')

                @bot.message_handler(commands='pedidosAdmin')
                def pedidos_admin(message):
                    chatid = message.chat.id
                    resgate = message
                    permissao, admin_id = conexao.admin(chatid)
                    if permissao:
                        cadastro, usuario = conexao.verifica_login(chatid)
                        print(usuario, ' acessou os pedidos como admin')
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
                        markup.add('Aguardando', 'Em progresso', 'Finalizado', 'Cancelado')  # quais as categorias
                        msg = bot.reply_to(message, 'Que tipo de pedido gostaria de ver?',
                                           reply_markup=markup)  # envia a opcao
                        bot.register_next_step_handler(msg, mostra_pedidos_admin)
                    else:
                        bot.reply_to(message, 'Você não é admin')
                        welcome_message(message)

                resgate = message

                @bot.message_handler(commands='interagirAdmin')
                def pedidos_admin(message):
                    resgate = message
                    chatid = message.chat.id
                    permissao, admin_id = conexao.admin(chatid)
                    if permissao:
                        cadastro, usuario = conexao.verifica_login(chatid)
                        print(usuario, ' quer interagir com pedidos')
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
                        markup.add('Todos', 'Um')  # quais as categorias
                        msg = bot.reply_to(message,
                                           'Gostaria de interagir com um em especifico ou todos da mesma categoria?',
                                           reply_markup=markup)  # envia a opcao
                        bot.register_next_step_handler(msg, interagir_pedidos_admin)
                    else:
                        bot.reply_to(message, 'Você não é admin')
                        welcome_message(message)

                @bot.message_handler(commands='mensagemAdmin')
                def mensagem_admin(message):
                    resgate = message
                    chatid = message.chat.id
                    permissao, admin_id = conexao.admin(chatid)
                    if permissao:
                        print(usuario, ' quer mandar mensagem para cliente')
                        msg = bot.reply_to(message,
                                           'Qual o ID do pedido?')
                        bot.register_next_step_handler(msg, mensagem_cliente_admin)
                    else:
                        bot.reply_to(message, 'Você não é admin')
                        welcome_message(message)

                resgate = message

                @bot.message_handler(commands='clienteAdmin')
                def mensagem_admin(message):
                    resgate = message
                    chatid = message.chat.id
                    permissao, admin_id = conexao.admin(chatid)
                    if permissao:
                        print(usuario, ' quer verificar cadastro')
                        msg = bot.reply_to(message,
                                           'Qual o ID do pedido?')
                        bot.register_next_step_handler(msg, cadastro_cliente_admin)
                    else:
                        bot.reply_to(message, 'Você não é admin')
                        welcome_message(message)
        else:
            msg = bot.reply_to(message, 'Olá, seja bem vindo ao Bot de Lavanderia da UNIVR!')
            bot.send_message(chatid, f'O ID da nossa conversa é: {chatid}')
            novo = Cadastro()
            novo.new_user(message)
    except Exception as a:
        print('algo deu errado no start: ', a)
        bot.reply_to(message, 'Algo deu errado, iremos começar do start novamente!')
        welcome_message(message)


class Cadastro:
    @staticmethod
    def new_user(message):
        msg = bot.reply_to(message, 'Vi que é a sua primeira vez comigo! Qual é o seu Nome completo?')
        bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        resgate = message
        chatid = message.chat.id
        name = message.text
        if name == '/start':
            welcome_message(message)
            return
        print(f'O {chatid} iniciou o processo de cadastro_cliente')
        user = User(name)
        user_dict[chatid] = user
        msg = bot.reply_to(message, 'Qual é o seu Email?')
        resgate = message
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as a:
        print('Algo deu errado no process_name_step: ', a)
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro_cliente novamente!')
        novo1 = Cadastro()
        novo1.new_user(message)


def process_email_step(message):
    try:
        chatid = message.chat.id
        email = str(message.text)
        if email == '/start':
            welcome_message(message)
            return
        user = user_dict[chatid]
        email = email.lower()
        user.email_usuario = email
        resgate = message
        msg = bot.reply_to(message, 'Qual é a sua Rua? "Exemplo: Copacabana"')
        bot.register_next_step_handler(msg, process_rua_step)
    except Exception as a:
        print('Algo deu errado no process_email_step: ', a)
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro_cliente novamente!')
        novo1 = Cadastro()
        novo1.new_user(message)


def process_rua_step(message):
    try:
        resgate = message
        chatid = message.chat.id
        rua = message.text
        user = user_dict[chatid]
        user.rua_usuario = rua
        msg = bot.reply_to(message, 'Qual é o número da sua casa/apartamento?')
        bot.register_next_step_handler(msg, process_numero_step)
    except Exception as a:
        print('Algo deu errado no process_rua_step: ', a)
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro_cliente novamente!')
        novo1 = Cadastro()
        novo1.new_user(message)


def process_numero_step(message):
    try:
        chatid = message.chat.id
        numero = message.text
        if not numero.isdigit():
            msg = bot.reply_to(message, 'Por favor, digite um número! Qual é o número da sua casa/apartamento?')
            bot.register_next_step_handler(msg, process_numero_step)
            return
        bot.send_message(chatid, '"Dica, caso queira começar novamente basta digitar /start"')
        if numero == '/start':
            welcome_message(message)
            return
        user = user_dict[chatid]
        user.numero_usuario = numero
        msg = bot.reply_to(message, 'Qual é o seu Bairro?')
        resgate = message
        bot.register_next_step_handler(msg, process_bairro_step)
    except Exception as a:
        print('Algo deu errado no process_numero_step: ', a)
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro_cliente novamente!')
        novo1 = Cadastro()
        novo1.new_user(message)


def process_bairro_step(message):
    try:
        chatid = message.chat.id
        bairro = message.text
        resgate = message
        user = user_dict[chatid]
        novo = conexao.cadastro_cliente(user.nome_usuario, chatid, user.email_usuario, user.rua_usuario,
                                        user.numero_usuario,
                                        bairro)
        cadastro, usuario = conexao.verifica_login(chatid)
        if cadastro:
            bot.reply_to(message,
                         f'Você foi cadastrado 🤩😁! Seja bem vindo {usuario}!!')
            bot.send_message(chatid,
                             f'Digite uma das opções:\n\n\n/lavar - realiza um novo pedido\n/pedidos - verifica o status de todos os seus pedidos anteriores.')

            @bot.message_handler(commands=['lavar'])
            def inicia_compra(message):
                compra = Lavar()
                compra.realiza_compra(message)

            print(f'{usuario} está no chat')
        else:
            bot.send_message(chatid, 'Algo deu errado! irei retornar a etapa de cadastro_cliente.')
            novo1 = Cadastro()
            novo1.new_user(message)
    except Exception as a:
        print('algo deu errado no process_bairro_step: ', a)


class Lavar:
    @staticmethod
    def realiza_compra(message):
        try:
            chatid = message.chat.id
            resgate = message
            cadastro, usuario = conexao.verifica_login(chatid)
            print(usuario, 'acabou de iniciar o processo de pedido')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
            resgate = message
            markup.add('Lavagem Rápida', 'Lavagem Completa')  # quais as categorias
            msg = bot.reply_to(message, 'Que tipo de Lavagem gostaria de fazer?', reply_markup=markup)  # envia a opcao
            bot.send_message(chatid,
                             '"Dica😉:\n\nEscolha lavagem rápida caso seja até 7 peças, se for mais escolha completa!! Muitas peças podem gerar custo adicional."')
            bot.register_next_step_handler(msg, process_tipo_pedido_step)
        except Exception as a:
            print('algo deu errado no realiza_compra: ', a)


def process_tipo_pedido_step(message):
    try:
        chatid = message.chat.id
        tipo = message.text
        id = conexao.retorna_id(chatid)
        order = Order(id[0])
        order_dict[chatid] = order
        resgate = message
        if (tipo == u'Lavagem Rápida') or (tipo == u'Lavagem Completa'):
            order.tipo = tipo
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
            markup.add('Reserva', 'Coleta')  # quais as categorias
            resgate = message
            msg = bot.reply_to(message, 'Qual o método do pedido?', reply_markup=markup)
            bot.send_message(chatid,
                             '"DICA😉:\n\nReserva - é reservada uma máquina na lavanderia e o cliente vai na data reservada.\nColeta - o transporte coleta no endereço do cliente de segunda a sexta (entre 8H até 11H e 14H até as 17H), faz a lavagem e depois o cliente busca."')
            bot.register_next_step_handler(msg, process_metodo_step)
        else:
            msg = bot.reply_to(message, 'Use um dos botoes!!!')
            erro = Lavar()
            erro.realiza_compra(message)
    except Exception as a:
        print('algo deu errado no process_tipo_pedido_step: ', a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        erro = Lavar()
        erro.realiza_compra(message)


def process_metodo_step(message):
    try:
        chatid = message.chat.id
        metodo = message.text
        cadastro, usuario = conexao.verifica_login(chatid)
        order = order_dict[chatid]
        resgate = message
        hoje, dia_semana = data.dia_reserva()
        global dia1, dia2
        dia1, dia2 = data.soma_reserva(dia_semana, hoje)
        if (metodo == u'Reserva') or (metodo == u'Coleta'):
            order.metodo = metodo
            if metodo == 'Coleta':
                pedido = conexao.cadastro_pedido_coleta(order.id, order.tipo, order.metodo)
                if pedido:
                    print(f'{usuario} fez um pedido de Coleta')
                    id_usuario = conexao.retorna_id(chatid)
                    id_usuario = int(id_usuario[0])
                    resgate = message
                    id_pedido = conexao.retorna_id_pedido_admin(id_usuario)
                    admins = conexao.retorna_admins()
                    bot.reply_to(message,
                                 'Caso prefira, pague usando Pix ou quando o veículo de coleta chegar no crédito! https://nubank.com.br/pagar/jrnl3/EbbhLT53li')
                    bot.send_message(chatid, 'Seu pedido já foi registrado! Aguardando ele ser lido.')
                    bot.send_message(chatid,
                                     '"Dica😉:\n\nPara ver o status de todos os seus pedidos digite: /pedidos\nou digite /lavar para realizar outro."')
                    admins = conexao.retorna_admins()
                    if admins:
                        for i in admins:
                            bot.send_message(i[0],
                                             f'{usuario} acabou de realizar um pedido de Coleta com o ID: {id_pedido}!')
            if metodo == 'Reserva':
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
                markup.add(f'{dia1}', f'{dia2}')  # quais as categorias
                msg = bot.reply_to(message, 'Qual o dia da reserva?', reply_markup=markup)
                bot.register_next_step_handler(msg, process_dia_step)
        else:
            bot.send_message(chatid, 'Use um dos botôes!!!')
            erro = Lavar()
            erro.realiza_compra(message)
    except Exception as a:
        print('algo deu errado no process_metodo_step: ', a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        erro = Lavar()
        erro.realiza_compra(message)


def process_dia_step(message):
    try:
        hoje, dia_semana = data.dia_reserva()
        chatid = message.chat.id
        dia = message.text
        resgate = message
        order = order_dict[chatid]
        certo = data.verifica_digitado(dia, dia1, dia2)
        if certo:
            resgate = message
            order.dia = dia
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
            markup.add('8H', '9H', '10H', '11H', '14H', '15H', '16H', '17H', '18H')  # quais as categorias
            msg = bot.reply_to(message, 'Qual o horário da reserva?', reply_markup=markup)
            bot.register_next_step_handler(msg, process_hora_step)
        else:
            print('erro no process_dia_step')
            bot.send_message(chatid, 'Use um dos botoes!!!')
            erro = Lavar()
            erro.realiza_compra(message)
    except Exception as a:
        print('algo deu errado no process_dia_pedido_step: ', a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        erro = Lavar()
        erro.realiza_compra(message)


def process_hora_step(message):
    try:
        chatid = message.chat.id
        cadastro, usuario = conexao.verifica_login(chatid)
        hora = message.text
        resgate = message
        hora = int(hora.replace('H', ''))
        if (hora == 8) or (hora == 9) or (hora == 10) or (hora == 11) or (hora == 14) or (hora == 15) or (
                hora == 16) or (hora == 17) or (hora == 18):
            order = order_dict[chatid]
            pedido = conexao.cadastro_pedido_reserva(order.id, order.tipo, order.metodo, order.dia, hora)
            if pedido:
                print(usuario, ' fez um pedido de reserva')
                bot.reply_to(message,
                             'Caso prefira, pague usando Pix ou no estabelecimento. https://nubank.com.br/pagar/jrnl3/EbbhLT53li')
                bot.send_message(chatid, 'Seu pedido já foi registrado! Aguardando ele ser lido.')
                id_usuario = conexao.retorna_id(chatid)
                id_usuario = int(id_usuario[0])
                resgate = message
                id_pedido = conexao.retorna_id_pedido_admin(id_usuario)
                admins = conexao.retorna_admins()
                if admins:
                    for i in admins:
                        bot.send_message(i[0],
                                         f'{usuario} acabou de realizar um pedido de Reserva como ID: {id_pedido}!')
                bot.send_message(chatid,
                                 '"Dica😉:\n\nPara ver o status de todos os seus pedidos digite: /pedidos\nou digite /lavar para realizar outro."')
            else:
                bot.send_message(chatid, 'algo deu errado, iremos voltar ao inicio!')
                erro = Lavar()
                erro.realiza_compra(message)
        else:
            bot.send_message(chatid, 'Use um dos botôes!!!')
            erro = Lavar()
            erro.realiza_compra(message)
    except Exception as a:
        print('algo deu errado no process_hora_pedido_step: ', a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        erro = Lavar()
        erro.realiza_compra(message)


class Pedidos:
    @staticmethod
    def verifica_pedidos(message):
        try:
            chatid = message.chat.id
            id = conexao.retorna_id(chatid)
            id = int(id[0])
            pedidos = conexao.retorna_pedidos(int(id))
            cont = 0
            resgate = message
            cadastro, usuario = conexao.verifica_login(chatid)
            print(usuario, ' quer saber sobre os pedidos')
            if pedidos:
                msg = bot.reply_to(message, 'Seus pedidos são: ')
                for i in pedidos:
                    cont += 1
                    dia_pedido = data.troca_forma(i[3])
                    if i[4] == 'Reserva':
                        dia_agendado = data.troca_forma(i[5])
                        bot.send_message(chatid,
                                         f'Pedido {cont}:\n\nTipo: {i[2]}\nData do pedido: {dia_pedido}\nMétodo do pedido: {i[4]}'
                                         f'\nReservado para: {dia_agendado}\nStatus do pedido: {i[6]}')

                    else:
                        bot.send_message(chatid,
                                         f'Pedido {cont}:\n\nTipo: {i[2]}\nData do pedido: {dia_pedido}\nMétodo do pedido: {i[4]}'
                                         f'\nStatus do pedido: {i[6]}')
                bot.send_message(chatid, 'Esses são os seus pedidos.')
                welcome_message(message)
            else:
                msg = bot.reply_to(message, 'Você não tem pedidos!')
                welcome_message(message)
        except Exception as a:
            print('Algo deu errado no verifica_pedidos: ', a)
            bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
            welcome_message(message)


def mostra_pedidos_admin(message):
    try:
        chatid = message.chat.id
        tipo = message.text
        resgate = message
        pedidos_admin = conexao.retorna_pedidos_admin(tipo)
        if pedidos_admin:
            for i in pedidos_admin:
                dia_pedido = data.troca_forma(i[4])
                if i[4] == 'Reserva':
                    dia_agendado = data.troca_forma(i[6])
                    bot.send_message(chatid,
                                     f'Id Pedido: {i[0]}\n\nNome do Cliente: {i[2]}\nChat Id: {i[1]}\nTipo do pedido: {i[3]}'
                                     f'\nData do pedido {dia_pedido}\nAgendado para: {dia_agendado}\nMétodo do pedido: {i[5]} Status do pedido: {i[7]}')
                else:
                    bot.send_message(chatid,
                                     f'Id Pedido: {i[0]}\n\nNome do Cliente: {i[2]}\nChat Id: {i[1]}\nTipo: {i[3]}\nData do pedido: {dia_pedido}\nMétodo do pedido: {i[5]}'
                                     f'\nStatus do pedido: {i[7]}')
            bot.send_message(chatid, 'Esses são os pedido.')
            welcome_message(message)
        else:
            msg = bot.reply_to(message, 'Você não tem pedidos desse tipo')
            welcome_message(message)
    except Exception as a:
        print('algo deu errado no mostra_pedidos_admin')
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        welcome_message(message)


def interagir_pedidos_admin(message):
    try:
        chatid = message.chat.id
        um_todos = message.text
        resgate = message
        bot.send_message(chatid, '"Dica, caso queira começar novamente basta digitar /start"')
        interact_admin = InteractAdmin(um_todos)
        interact_dict[chatid] = interact_admin
        cadastro, usuario = conexao.verifica_login(chatid)
        if um_todos == 'Todos':
            print(usuario, ' quer interagir com todos os pedidos')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
            markup.add('Aguardando', 'Em progresso', 'Finalizado', 'Cancelado')  # quais as categorias
            msg = bot.reply_to(message, 'Com que tipo de atendimento gostaria de interagir?',
                               reply_markup=markup)  # envia a opcao
            bot.register_next_step_handler(msg, interage_todos_admin)
        if um_todos == 'Um':
            msg = bot.reply_to(message, 'Qual o ID do pedido que gostaria de interagir?')
            bot.register_next_step_handler(msg, process_interagir_um_step)
    except Exception as a:
        print('algo deu errado no interagir_pedidos_admin')
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        welcome_message(message)


def process_interagir_um_step(message):
    try:
        chatid = message.chat.id
        id_pedido = message.text
        interact_admin = interact_dict[chatid]
        interact_admin.id_pedido = id_pedido
        resgate = message
        print(usuario, f' quer interagir com o pedido de ID: {id_pedido}')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Aguardando', 'Em progresso', 'Finalizado', 'Cancelado')  # quais as categorias
        msg = bot.reply_to(message, 'Qual status gostaria de colocar?',
                           reply_markup=markup)  # envia a opcao
        bot.register_next_step_handler(msg, mensagem_todos_interacao_admin)
    except Exception as a:
        print('algo deu errado no process_interagir_um_step')
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        welcome_message(message)


def interage_todos_admin(message):
    try:
        chatid = message.chat.id
        tipo = message.text
        resgate = message
        tipo = str(tipo)
        pedidos_admin = conexao.retorna_pedidos_admin(tipo)
        if pedidos_admin:
            interact_admin = interact_dict[chatid]
            interact_admin.tipo_pedido = tipo
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
            markup.add('Aguardando', 'Em progresso', 'Finalizado', 'Cancelado')  # quais as categorias
            msg = bot.reply_to(message, 'Qual status gostaria de colocar?',
                               reply_markup=markup)  # envia a opcao
            bot.register_next_step_handler(msg, mensagem_todos_interacao_admin)
        else:
            msg = bot.reply_to(message, 'Você não tem pedidos desse tipo')
            welcome_message(message)
    except Exception as a:
        print('algo deu errado no interage_todos_admin: ', a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        welcome_message(message)


def mensagem_todos_interacao_admin(message):
    try:
        chatid = message.chat.id
        mudanca = message.text
        resgate = message
        cadastro, usuario = conexao.verifica_login(chatid)
        interact_admin = interact_dict[chatid]
        chatids = conexao.retorna_chatid_pedido_admin(interact_admin.tipo_pedido, interact_admin.um_todos,
                                                      interact_admin.id_pedido)
        alterado = conexao.altera_status_pedido_admin(interact_admin.um_todos, interact_admin.tipo_pedido, mudanca,
                                                      interact_admin.id_pedido)
        um_todos = str(interact_admin.um_todos)
        if um_todos == 'Todos':
            print(usuario, ' acabou de alterar todos os pedidos')
            bot.send_message(chatid, 'Pedidos alterado')
            welcome_message(message)
        else:
            print(usuario, ' acabou de alterar o pedido: ', interact_admin.id_pedido)
            bot.send_message(chatid, 'Pedido alterado')
            welcome_message(message)
        if alterado:
            for i in chatids:
                dia_pedido = data.troca_forma(i[2])
                bot.send_message(int(i[1]),
                                 f'{i[0]},\nSeu pedido feito no dia: {dia_pedido}, acabou de receber o status de: {mudanca}')
    except Exception as a:
        print('Algo deu errado no mensagem_todos_interacao_admin: ', a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        welcome_message(message)


def mensagem_cliente_admin(message):
    try:
        chatid = message.chat.id
        id_pedido = message.text
        resgate = message
        interact_admin = InteractAdmin(None)
        interact_dict[chatid] = interact_admin
        interact_admin.id_pedido = id_pedido
        msg = bot.reply_to(message, 'Que mensagem gostaria de mandar para o cliente?')
        bot.register_next_step_handler(msg, process_mandar_mensagem_step)
    except Exception as a:
        print('algo deu errado no mensagem_cliente_admin: ', a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        welcome_message(message)


def process_mandar_mensagem_step(message):
    try:
        chatid = message.chat.id
        mensagem = message.text
        resgate = message
        cadastro, usuario = conexao.verifica_login(chatid)
        interact_admin = interact_dict[chatid]
        chatids = conexao.retorna_chatid_pedido_admin(None, 'Um', interact_admin.id_pedido)
        for i in chatids:
            bot.send_message(i[1], f'{usuario} mandou uma mensagem pelo bot: {mensagem}')
        bot.send_message(chatid, 'Mensagem enviada')
        welcome_message(message)
    except Exception as a:
        print('algo deu errado no process_mandar_mensagem_step: ', a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        welcome_message(message)


def cadastro_cliente_admin(message):
    try:
        chatid = message.chat.id
        id_produto = message.text
        resgate = message
        cadastro = conexao.mostra_cadastro_cliente(id_produto)
        for i in cadastro:
            bot.send_message(chatid, f'Id Usuario: {i[0]}\n\nNome: {i[1]}\nEmail: {i[2]}\n'
                                     f'Rua: {i[3]}\nNúmero: {i[4]}\nBairro: {i[5]}')
        bot.send_message(chatid, 'Esses são os cadastros.')
        welcome_message(message)
    except Exception as a:
        print('algo deu errado no cadastro_cliente_admin: ')
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        welcome_message(message)


while True:
    try:
        bot.enable_save_next_step_handlers(delay=2)  # step
        bot.load_next_step_handlers()
        bot.polling()
    except Exception as a:
        print(usuario, ' fez um erro')
        chatid_resgate = resgate.chat.id
        bot.send_message(chatid_resgate, 'Por favor, use apenas comandos!!!')
        time.sleep(5)
        welcome_message(resgate)
