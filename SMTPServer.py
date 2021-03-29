from socket import *
import os
import sys
from helpers import *

# Numero de porta na qual o servidor estara esperando conexoes.
serverPort = 25

# Criar o socket. AF_INET e SOCK_STREAM indicam TCP.
serverSocket = socket(AF_INET, SOCK_STREAM)

# Associar o socket a porta escolhida. Primeiro argumento vazio indica
# que desejamos aceitar conexoes em qualquer interface de rede desse host
serverSocket.bind(('', serverPort))


# Habilitar socket para aceitar conexoes. O argumento 1 indica que ate
# uma conexao sera deixada em espera, caso recebamos multiplas conexoes
# simultaneas
serverSocket.listen(1)

#Comandos implentados

# Após receber QUIT
# 0 - Aguardando HELO

# Após receber HELO, RSET, ou fechar a DATA
# 1 - Aguardando MAIL FROM, RSET, VRFY, NOOP, QUIT

# Após receber o MAIL FROM
# 2 - Aguardando RCPT TO, DATA, MAIL FROM, RSET, VRFY, NOOP, QUIT

# Após receber DATA
# 3 - Aguardando o .


def main():
  popula_caixa()

  # Loop da conexão
  while 1:

    # Estado do servidor
    SERVER_STATE = 0

    # Aguardar nova conexão
    connectionSocket, addr = serverSocket.accept()
    print('Nova conexão recebida!')

    connectionSocket.send("220 redes.uff".encode('UTF-8'))

    userList =[]

    sender = ''

    data = ''
      
    # Loop dos estados
    while 1:

      # Mensagem do usuário
      sentence = connectionSocket.recv(1024).decode('UTF-8')

      # Estado 0 (Aguardando HELO)
      if (SERVER_STATE == 0):
        
        comando_digitado = verificar_comando(connectionSocket, sentence, ['HELO', 'QUIT'])

        if (comando_digitado):
          if (comando_digitado == COMANDOS_ENUM["HELO"] and helo(connectionSocket, sentence)):
            SERVER_STATE = 1
          
          elif (comando_digitado == COMANDOS_ENUM["QUIT"]):
            quit(connectionSocket)
            break

      # Estado 1 (Aguardando MAIL FROM/ RSET, VRFY, NOOP, QUIT)
      elif (SERVER_STATE == 1):
      
        comando_digitado = verificar_comando(connectionSocket, sentence, ['MAIL FROM', 'NOOP', 'VRFY', 'RSET', 'QUIT'])

        if (comando_digitado):
          if (comando_digitado == COMANDOS_ENUM["MAIL FROM"] and mail_from(connectionSocket, sentence)):
            sender = sentence = sentence.replace(' ', '').split(':')[1]
            SERVER_STATE = 2
          
          elif (comando_digitado == COMANDOS_ENUM["NOOP"]):
            noop(connectionSocket)

          elif (comando_digitado == COMANDOS_ENUM["VRFY"]):
            vrfy(connectionSocket, sentence)

          elif (comando_digitado == COMANDOS_ENUM["RSET"]):
            connectionSocket.send("250 OK".encode('UTF-8'))
            SERVER_STATE = 0

          elif (comando_digitado == COMANDOS_ENUM["QUIT"]):
            quit(connectionSocket)
            break

      # Estado 2 (Aguardando DATA / RCPT TO, RSET, VRFY, NOOP, QUIT, MAIL FROM)    
      elif (SERVER_STATE == 2):
        comando_digitado = verificar_comando(connectionSocket, sentence, 
        ['DATA', 'RCPT TO', 'RSET', 'VRFY', 'NOOP', 'QUIT', 'MAIL FROM'])

        if (comando_digitado):
          if (comando_digitado == COMANDOS_ENUM["RCPT TO"] and rcpt_to(connectionSocket, sentence)):
            #Adiciona um usuário na lista de remetentes
            userList.append(sentence.replace(' ', '').split(':')[1])

          elif (comando_digitado == COMANDOS_ENUM["MAIL FROM"] and mail_from(connectionSocket, sentence)):
            sender = sentence = sentence.replace(' ', '').split(':')[1]
            #Apaga a lista antiga de destinatarios
            userList.clear() 
            SERVER_STATE = 2

          
          elif (comando_digitado == COMANDOS_ENUM["RSET"]):
            print('Executando RSET')
            connectionSocket.send("250 OK".encode('UTF-8'))
            print('Mantendo estado 0')
            #Apaga remetente e destinatários e volta pro início
            sender = ''
            userList.clear()
            SERVER_STATE = 0

          elif (comando_digitado == COMANDOS_ENUM["VRFY"]):
            vrfy(connectionSocket, sentence)

          elif (comando_digitado == COMANDOS_ENUM["NOOP"]):
            noop(connectionSocket)

          elif (comando_digitado == COMANDOS_ENUM["QUIT"]):
            quit(connectionSocket)
            break

          elif (comando_digitado == COMANDOS_ENUM["DATA"]):
            if (acpt_data(connectionSocket, sentence, userList)):
              SERVER_STATE = 3        

      # Estado 3 (Aguardando o .)
      elif (SERVER_STATE == 3):
        if (sentence != '.'):
          data += sentence
        else:
          write_data(sender, userList, data)
          connectionSocket.send('250 Message accepted for delivery'.encode('UTF-8'))
          userList.clear()
          sender=''
          SERVER_STATE = 0


main()