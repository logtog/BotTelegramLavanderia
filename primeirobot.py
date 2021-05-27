#-- coding: utf-8 --
import telebot #importando a biblioteca pytelegrambotapi

API_TOKEN = '1850427397:AAFkCK-eMgRvDTNthVWig-ekaG0rVXr2hvQ' #@botfather

bot = telebot.TeleBot(API_TOKEN) #telebot-sumário e TeleBot(comando) aplicando token

#inicio

variavel = variavel

@bot.message_handler(commands=['start']) #recebo mensagem /start

def send_welcome(message):
	chatid = message.chat.id # pegar id da conversa
	msg = bot.reply_to(message,'Olá, seja bem vindo ao Bot de Lavanderia da Unisepe! \nO ID da nossa conversa é: ' + str(chatid)) #msg enviada para o usuario
	bot.send_message(chatid, 'Caso você precise de ajuda, use a função /ajuda.')

#ajuda
@bot.message_handler(commands=['ajuda']) #recebo comandos
def send_help(message):
	msg_help = bot.reply_to(message, 'Você não se lembra das funções? \nOpção 1:  /cadastro \nOpção 2:  /categoria \nOpção 4:  /contato')
bot.polling() #escuta usuario
