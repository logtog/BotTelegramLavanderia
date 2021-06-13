# -- coding: utf-8 --
from conexaoBd import Conexao
import telebot
from telebot import types
from data import Data

data = Data()
conexao = Conexao()
user_dict = {}
order_dict = {}
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


@bot.message_handler(commands=['start'])
def welcome_message(message):
    try:
        chatid = message.chat.id
        global usuario
        cadastro, usuario = conexao.verifica_login(chatid)
        if cadastro:
            print(f'{usuario} acabou de iniciar o chat')
            bot.reply_to(message, f'Olá, {usuario}! O que gostaria de fazer hoje?\nO ID da conversa é: {chatid} 🥳🥳')
            bot.send_message(chatid,
                             'Digite uma das opções:\n\n\n/lavar - realiza um novo pedido\n/pedidos - verifica o status de todos os seus pedidos anteriores.')
            permissao, admin_id = conexao.admin(chatid)
            if permissao:
                bot.send_message(chatid, 'Digite /pedidos_admin para verificar os pedidos')

                @bot.message_handler(commands='pedidos_admin')
                def pedidos_admin(message):
                    chatid = message.chat.id
                    global permissao, admin_id
                    permissao, admin_id = conexao.admin(chatid)
                    if permissao:
                        print(usuario, ' acessou os pedidos como admin')
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
                        markup.add('Aguardando', 'Em progresso', 'Finalizado', 'Cancelado')  # quais as categorias
                        msg = bot.reply_to(message, 'Que tipo de atendimento gostaria de ver?',
                                           reply_markup=markup)  # envia a opcao
                        bot.register_next_step_handler(msg, mostra_pedidos_admin)
                    else:
                        bot.reply_to(message, 'Você não é admin')
                        welcome_message(message)

            @bot.message_handler(commands=['lavar'])
            def inicia_compra(message):
                compra = Lavar()
                compra.realiza_compra(message)

            @bot.message_handler(commands=['pedidos'])
            def inicia_pedidos(message):
                pedido = Pedidos()
                pedido.verifica_pedidos(message)
        else:
            msg = bot.reply_to(message, 'Olá, seja bem vindo ao Bot de Lavanderia da UNIVR!')
            bot.send_message(chatid, f'O ID da nossa conversa é: {chatid}')
            novo = Cadastro()
            novo.new_user(message)
    except Exception as a:
        print('algo deu errado no start')
        bot.reply_to(message, 'Algo deu errado, iremos começar do start novamente!')
        welcome_message(message)


class Cadastro:
    @staticmethod
    def new_user(message):
        msg = bot.reply_to(message, 'Vi que é a sua primeira vez comigo! Qual é o seu Nome completo?')
        bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chatid = message.chat.id
        name = message.text
        if name == '/start':
            welcome_message(message)
            return
        print(f'O {chatid} iniciou o processo de cadastro_cliente')
        user = User(name)
        user_dict[chatid] = user
        msg = bot.reply_to(message, 'Qual é o seu Email?')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as a:
        print('Algo deu errado no process_name_step')
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
        msg = bot.reply_to(message, 'Qual é a sua Rua? "Exemplo: Copacabana"')
        bot.register_next_step_handler(msg, process_rua_step)
    except Exception as a:
        print('Algo deu errado no process_email_step')
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro_cliente novamente!')
        novo1 = Cadastro()
        novo1.new_user(message)


def process_rua_step(message):
    try:
        chatid = message.chat.id
        rua = message.text
        user = user_dict[chatid]
        user.rua_usuario = rua
        msg = bot.reply_to(message, 'Qual é o número da sua casa/apartamento?')
        bot.register_next_step_handler(msg, process_numero_step)
    except Exception as a:
        print('Algo deu errado no process_rua_step')
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
        bot.send_message(chatid, '"Dica, caso queira começar novamente basta digitar /start')
        if numero == '/start':
            welcome_message(message)
            return
        user = user_dict[chatid]
        user.numero_usuario = numero
        msg = bot.reply_to(message, 'Qual é o seu Bairro?')
        bot.register_next_step_handler(msg, process_bairro_step)
    except Exception as a:
        print('Algo deu errado no process_numero_step')
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro_cliente novamente!')
        novo1 = Cadastro()
        novo1.new_user(message)


def process_bairro_step(message):
    chatid = message.chat.id
    bairro = message.text
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


class Lavar:
    @staticmethod
    def realiza_compra(message):
        chatid = message.chat.id
        print(usuario, 'acabou de iniciar o processo de pedido')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
        markup.add('Lavagem Rápida', 'Lavagem Completa')  # quais as categorias
        msg = bot.reply_to(message, 'Que tipo de Lavagem gostaria de fazer?', reply_markup=markup)  # envia a opcao
        bot.send_message(chatid,
                         '"Dica😉:\n\nEscolha lavagem rápida caso seja até 7 peças, se for mais escolha completa!! Muitas peças podem gerar custo adicional."')
        bot.register_next_step_handler(msg, process_tipo_pedido_step)


def process_tipo_pedido_step(message):
    try:
        chatid = message.chat.id
        tipo = message.text
        id = conexao.retorna_id(chatid)
        order = Order(id[0])
        order_dict[chatid] = order
        if (tipo == u'Lavagem Rápida') or (tipo == u'Lavagem Completa'):
            order.tipo = tipo
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # cria a opção
            markup.add('Reserva', 'Coleta')  # quais as categorias
            msg = bot.reply_to(message, 'Qual o método do pedido?', reply_markup=markup)
            bot.send_message(chatid,
                             '"DICA😉:\n\nReserva - é reservada uma máquina na lavanderia e o cliente vai na data reservada.\nColeta - o transporte coleta no endereço do cliente de segunda a sexta (entre 8H até 11H e 14H até as 17H), faz a lavagem e depois o cliente busca."')
            bot.register_next_step_handler(msg, process_metodo_step)
        else:
            msg = bot.reply_to(message, 'Use um dos botoes!!!')
            erro = Lavar()
            erro.realiza_compra(message)
    except Exception as a:
        print(a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        erro = Lavar()
        erro.realiza_compra(message)


def process_metodo_step(message):
    try:
        chatid = message.chat.id
        metodo = message.text
        order = order_dict[chatid]
        hoje, dia_semana = data.dia_reserva()
        global dia1, dia2
        dia1, dia2 = data.soma_reserva(dia_semana, hoje)
        if (metodo == u'Reserva') or (metodo == u'Coleta'):
            order.metodo = metodo
            if metodo == 'Coleta':
                pedido = conexao.cadastro_pedido_coleta(order.id, order.tipo, order.metodo)
                if pedido:
                    bot.reply_to(message,
                                 'Caso prefira, pague usando Pix ou quando o veículo de coleta chegar no crédito! https://nubank.com.br/pagar/jrnl3/EbbhLT53li')
                    bot.send_message(chatid, 'Seu pedido já foi registrado! Aguardando ele ser lido.')
                    bot.send_message(chatid,
                                     '"Dica😉:\n\nPara ver o status de todos os seus pedidos digite: /pedidos\nou digite /lavar para realizar outro."')
                    admins = conexao.retorna_admins()
                    if admins:
                        for i in admins:
                            bot.send_message(i[0], f'{usuario} acabou de realizar um pedido de coleta!')
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
        print(a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        erro = Lavar()
        erro.realiza_compra(message)


def process_dia_step(message):
    try:
        hoje, dia_semana = data.dia_reserva()
        chatid = message.chat.id
        dia = message.text
        order = order_dict[chatid]
        certo = data.verifica_digitado(dia, dia1, dia2)
        if certo:
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
        print(a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        erro = Lavar()
        erro.realiza_compra(message)


def process_hora_step(message):
    try:
        chatid = message.chat.id
        hora = message.text
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
                admins = conexao.retorna_admins()
                if admins:
                    for i in admins:
                        bot.send_message(i[0], f'{usuario} acabou de realizar um pedido de coleta!')
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
        print(a)
        bot.reply_to(message, 'Erro!! Iremos voltar para o inicio!')
        erro = Lavar()
        erro.realiza_compra(message)


class Pedidos:
    @staticmethod
    def verifica_pedidos(message):
        chatid = message.chat.id
        id = conexao.retorna_id(chatid)
        id = int(id[0])
        pedidos = conexao.retorna_pedidos(int(id))
        cont = 0
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
        else:
            msg = bot.reply_to(message, 'Você não tem pedidos!')


def mostra_pedidos_admin(message):
    chatid = message.chat.id
    permissao, admin_id = conexao.admin(chatid)
    tipo = message.text
    pedidos_admin = conexao.retorna_pedidos_admin(tipo)
    if pedidos_admin:
        for i in pedidos_admin:
            dia_pedido = data.troca_forma(i[4])
            if i[4] == 'Reserva':
                dia_agendado = data.troca_forma(i[6])
                bot.send_message(chatid,
                                 f'Id Pedido: {i[0]}\n\nChat Id: {i[1]}\nNome do Cliente: {i[2]}\nTipo do pedido: {i[3]}'
                                 f'\nData do pedido {dia_pedido}\nAgendado para: {dia_agendado}\nMétodo do pedido: {i[4]} Status do pedido: {i[7]}')
            else:
                bot.send_message(chatid,
                                 f'Id Pedido: {i[0]}\n\nChat Id: {i[1]}\nNome do Cliente: {i[2]}\nTipo: {i[3]}\nData do pedido: {dia_pedido}\nMétodo do pedido: {i[4]}'
                                 f'\nStatus do pedido: {i[7]}')
    else:
        msg = bot.reply_to(message, 'Você não tem pedidos desse tipo')
        welcome_message(message)


def altera_estado_pedidos(message):
    chatid = message.chat.id



bot.enable_save_next_step_handlers(delay=2)  # step
bot.load_next_step_handlers()
bot.polling()
