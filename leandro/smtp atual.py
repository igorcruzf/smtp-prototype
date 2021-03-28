from socket import *
import os
import sys
from datetime import datetime

def popula_caixa():
  caixas = 'usuarios.txt'

  if os.path.isfile(caixas) == False:
    print('Arquivo Inexistente, encerrando aplicação')
    sys.exit()
    #Encerrar aplicação

  arquivo = open(caixas, 'r+')

  usuarios = arquivo.readlines()

  for i in range(len(usuarios)):
      if usuarios[i][-1] != '\n':
          usuario = (usuarios[i] + ".txt")
      else:
          usuario = (usuarios[i][0:-1] + ".txt")
      caixa = open('caixas/'+ usuario, 'a+')
      caixa.close()


popula_caixa()

# Numero de porta na qual o servidor estara esperando conexoes.
serverPort = 12000

# Criar o socket. AF_INET e SOCK_STREAM indicam TCP.
serverSocket = socket(AF_INET, SOCK_STREAM)

# Associar o socket a porta escolhida. Primeiro argumento vazio indica
# que desejamos aceitar conexoes em qualquer interface de rede desse host
serverSocket.bind(('', serverPort))

# Habilitar socket para aceitar conexoes. O argumento 1 indica que ate
# uma conexao sera deixada em espera, caso recebamos multiplas conexoes
# simultaneas
serverSocket.listen(1)

print('O servidor esta pronto para receber conexoes')


def main():
  # Loop infinito: servidor eh capaz de tratar multiplas conexoes
  while 1:

    try:
      # Aguardar nova conexao
      print('Aguardando conexao...')
      connectionSocket, addr = serverSocket.accept()
      print('Nova conexao recebida!')

      # Recepcao de dados
      if(not(helo(connectionSocket) and mail_from(connectionSocket))): 
        print('Fechando socket...')
        connectionSocket.close()
      else:
        userList = rcpt_to(connectionSocket)
        data = receive_data(connectionSocket, userList)
        write_data(userList, data)
      #inserir nos arquivos
      
    except Exception as e:
      print(e)
      connectionSocket.close()  


def helo(connectionSocket):
  print('Aguardando HELO...')
  sentence = connectionSocket.recv(1024).decode('UTF-8').split()

  while('HELO' != sentence[0] or len(sentence) == 1):

    if('QUIT' == sentence[0]):
      return False

    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
    print('Aguardando HELO...')
    sentence = connectionSocket.recv(1024).decode('UTF-8').split()
    print('Dado recebido do cliente: ', sentence)

  print('Helo recebido')
  message = "250 Hello " + sentence[1] + ", pleased to meet you"
  connectionSocket.send(message.encode('UTF-8'))
  return True

def mail_from(connectionSocket):
  print('Aguardando MAIL FROM')
  sentence = connectionSocket.recv(1024).decode('UTF-8').split(':')
      
  while('MAIL FROM' != sentence[0] or len(sentence) == 1):
    
    if('QUIT' == sentence[0]):
      return False

    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
    print('Aguardando MAIL FROM...')
    sentence = connectionSocket.recv(1024).decode('UTF-8').split()
  
  print('Mail from recebido' + sentence[1])
  message = '250 ' + sentence[1] + '... Sender ok'
  connectionSocket.send(message.encode('UTF-8'))

  return True


def rcpt_to(connectionSocket):

  userList = []

  print('Aguardando RCPT TO')
  sentence = connectionSocket.recv(1024).decode('UTF-8').split(':')

  while('DATA' != sentence[0]):

    while(('RCPT TO' != sentence[0] or len(sentence) == 1) and 'DATA' != sentence[0]):

      if('QUIT' == sentence[0]):
        return []

      connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
      print('Aguardando RCPT TO...')
      sentence = connectionSocket.recv(1024).decode('UTF-8').split(':')

    print('RCPT TO recebido' + sentence[1])
    user = sentence[1].split('@')[0]

    if(os.path.isfile('caixas/' + user + '.txt')):
      print('Encontrou o user ' + sentence[1] + 'User:' + user)
      message = '250 ' + sentence[1] + '... Recipient ok'
      connectionSocket.send(message.encode('UTF-8'))
      userList.append(user)
    else:
      print('Nao encontrou o user ' + sentence[1] + ' User: ' + user)
      connectionSocket.send("550 Address unknown".encode('UTF-8'))

    print('Aguardando RCPT TO')
    sentence = connectionSocket.recv(1024).decode('UTF-8').split(':')
  return userList

def receive_data(connectionSocket, userList):
  data = ''
  if(len(userList) != 0):
    print('Pegando dados para enviar...')
    connectionSocket.send('354 Enter mail, end with ".". on a line by itself'.encode('UTF-8'))
    sentence = connectionSocket.recv(1024)
    while('.' != sentence.decode('UTF-8')):
      print('dado recebido: ' + sentence.decode('UTF-8'))
      data += sentence.decode('UTF-8')
      sentence = connectionSocket.recv(1024)
    connectionSocket.send('250 Message accepted for delivery'.encode('UTF-8'))
  return data

def write_data(userlist, data):
    horario = datetime.now().strftime('%H:%M - %d/%m/%Y')
    for usuario in range(len(userlist)):
        caixa = open('caixas/'+ userlist[usuario] + '.txt', 'a+')
        #caixa.write('From:' + remetente + '\n')
        caixa.write(horario + '\n')
        caixa.write(data +'.' + '\n\n')
        caixa.close()

main()