# -- coding: utf-8 --
from conexaoBd import Conexao
import telebot

conexao = Conexao()
user_dict = {}

API_TOKEN = '1850427397:AAFkCK-eMgRvDTNthVWig-ekaG0rVXr2hvQ'
bot = telebot.TeleBot(API_TOKEN, parse_mode=None)


class User:
    def __init__(self, name):
        self.nome_usuario = name
        self.email_usuario = None
        self.rua_usuario = None
        self.numero_usuario = None
        self.bairro_usuario = None


@bot.message_handler(commands=['start'])
def welcome_message(message):
    try:
        chatid = message.chat.id
        cadastro, usuario = conexao.verifica_login(chatid)
        if cadastro:
            print(f'{usuario} acabou de iniciar o chat')
            bot.reply_to(message, f'Olá, {usuario}! O que gostaria de fazer hoje?\nO ID da conversa é: {chatid} 🥳🥳')
            bot.send_message(chatid, 'Digite uma das opções:\n\n\n/lavar - realiza um novo pedido\n/pedidos - verifica o status de todos os seus pedidos anteriores.')
            @bot.message_handler(commands=['lavar'])
            def inicia_compra(message):
                compra = Lavar()
                compra.realiza_compra(message)
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
        print(f'O {chatid} iniciou o processo de cadastro')
        user = User(name)
        user_dict[chatid] = user
        msg = bot.reply_to(message, 'Qual é o seu Email?')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as a:
        print('Algo deu errado no process_name_step')
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro novamente!')
        novo1 = Cadastro()
        novo1.new_user(message)


def process_email_step(message):
    try:
        chatid = message.chat.id
        email = message.text
        if email == '/start':
            welcome_message(message)
            return
        user = user_dict[chatid]
        user.email_usuario = email
        msg = bot.reply_to(message, 'Qual é a sua Rua? "Exemplo: Copacabana"')
        bot.register_next_step_handler(msg, process_rua_step)
    except Exception as a:
        print('Algo deu errado no process_email_step')
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro novamente!')
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
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro novamente!')
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
        bot.reply_to(message, 'Algo deu errado, iremos começar o cadastro novamente!')
        novo1 = Cadastro()
        novo1.new_user(message)


def process_bairro_step(message):
    chatid = message.chat.id
    bairro = message.text
    user = user_dict[chatid]
    novo = conexao.cadastro(user.nome_usuario, chatid, user.email_usuario, user.rua_usuario, user.numero_usuario,
                            bairro)
    cadastro, usuario = conexao.verifica_login(chatid)
    if cadastro:
        bot.reply_to(message,
                     f'Você foi cadastrado 🤩😁! Seja bem vindo {usuario}!!')
        bot.send_message(chatid,
                         f'Digite /lavar para realizar um novo pedido ou /pedidos para verificar o status de todos os seus pedidos anteriores.')
        print(f'{usuario} está no chat')
    else:
        bot.send_message(chatid, 'Algo deu errado! irei retornar a etapa de cadastro.')
        novo1 = Cadastro()
        novo1.new_user(message)


class Lavar:
    @staticmethod
    def realiza_compra(message):
        chatid = message.chat.id
        msg = bot.reply_to(message, 'teste compra')
        bot.register_next_step_handler(msg, process_tipo_pedido_step)


def process_tipo_pedido_step(message):
    chatid = message.chat.id
    bot.send_message(chatid, 'process_tipo_pedido_step')

bot.enable_save_next_step_handlers(delay=2)  # step
bot.load_next_step_handlers()
bot.polling()
