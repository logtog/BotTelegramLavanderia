#-- coding: utf-8 --
from conexaobd import conexao
import requests
import telebot #importando a biblioteca pytelegrambotapi
import time
from telebot import types #esta selecionando a lib types que faz parte do telebot
import pymysql #biblioteca de conexao com o mysql

conexao.conectar()

API_TOKEN = '1850427397:AAFkCK-eMgRvDTNthVWig-ekaG0rVXr2hvQ' #@botfather

bot = telebot.TeleBot(API_TOKEN) #telebot-sumário e TeleBot(comando) aplicando token

#inicio
@bot.message_handler(commands=['start']) #recebo mensagem /start
def send_welcome(message):
	chatid = message.chat.id # pegar id da conversa
	msg = bot.reply_to(message,'Olá, seja bem vindo ao Bot de Lavanderia da Unisepe! \nO ID da nossa conversa é: ' + str(chatid)) #msg enviada para o usuario
	bot.send_message(chatid, 'Caso você precise de ajuda, use a função /ajuda.')

#ajuda
@bot.message_handler(commands=['ajuda']) #recebo comandos
def send_help(message):
	msg_help = bot.reply_to(message, 'Você não se lembra das funções? \nOpção 1:  /cadastro \nOpção 2:  /categoria \nOpção 3:  /contato')

@bot.message_handler(commands=['categoria'])
def send_category(message):
	chatid = message.chat.id
	msg = bot.reply_to(message,'Dica 🧐🧐: escolha lavagem rapida somente se for menos de 6 peças de roupas, caso for mais, escolha lavagem completa!')
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)#crio o layout de opções, digo para ele que só pode selecionar uma opções
	markup.add('Lavagem Rapida','Lavagem Completa')#opções que deve aparecer para o cliente
	msg_cat = bot.reply_to(message,"Escolha a categoria que você deseja:", reply_markup=markup)#qual das suas categorias você quer

while True:       # faz rodar para sempre
	try:
		bot.polling() #escuta usuario
	except Exception:
		time.sleep(15)
