from socket import *
import os
import sys
from datetime import datetime
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
      
    # Loop dos estados
    while 1:

      # Mensagem do usuário
      sentence = connectionSocket.recv(1024).decode('UTF-8')

      # Estado 0 (Aguardando HELO)
      if (SERVER_STATE == 0):
        
        comando_digitado = verificar_comando(connectionSocket, sentence, ['HELO'])

        if (comando_digitado):
          if (comando_digitado == COMANDOS_ENUM["HELO"] and helo(connectionSocket, sentence)):
            print('HELLO recebido, aguardando por MAIL FROM ou QUIT.')
            SERVER_STATE = 1

      # Estado 1 (aguardando MAIL FROM, QUIT)
      elif (SERVER_STATE == 1):
      
        message = ''
        rcpt = []

        comando_digitado = verificar_comando(connectionSocket, sentence, ['MAIL FROM', 'QUIT'])

        if (comando_digitado):
          if (comando_digitado == COMANDOS_ENUM["MAIL FROM"] and mail_from(connectionSocket, sentence)):
            print('MAIL FROM recebido, aguardando RCPT TO ou QUIT.')
            SERVER_STATE = 2

          elif (comando_digitado == COMANDOS_ENUM["QUIT"]):
            print('Encerrando conexão atual.')
            quit(connectionSocket)
            break

      # Estado 2 (aguardando RCPT TO, QUIT e DATA caso já tenha recebido RCPT TO)    
      elif (SERVER_STATE == 2):
        comando_digitado = verificar_comando(connectionSocket, sentence, ['RCPT TO', 'DATA', 'QUIT', 'MAIL FROM'])

        if (comando_digitado):
          if (comando_digitado == COMANDOS_ENUM["RCPT TO"]):
            rcpt_aux = rcpt_to(connectionSocket, sentence, rcpt)

            if (rcpt_aux): 
              rcpt = rcpt_aux
              print('Adicionando', rcpt_aux, 'na lista de destinatários.')
              print('Destinatários:', rcpt)
              print('RCPT TO recebido, aguardando outros RCPT TO, DATA ou QUIT.')

          elif (comando_digitado == COMANDOS_ENUM["MAIL FROM"] and mail_from(connectionSocket, sentence)):
            print('MAIL FROM recebido, resetando lista de destinatários.')
            rcpt = []

          elif (comando_digitado == COMANDOS_ENUM["QUIT"]):
            print('Encerrando conexão atual.')
            quit(connectionSocket)
            break
        
          elif (comando_digitado == COMANDOS_ENUM["DATA"] and data(connectionSocket, rcpt)):
            SERVER_STATE = 3

      # Estado 3 (aguardando mensagens do data e o '.')
      elif (SERVER_STATE == 3):
        if (sentence == '.'): 
          connectionSocket.send('250 Message accepted for delivery'.encode('UTF-8'))
          print('Mensagem enviada, esperando novo MAIL FROM ou QUIT.')
          write_data(rcpt, message)
          SERVER_STATE = 1

        else: message += (sentence + '\n')


main()