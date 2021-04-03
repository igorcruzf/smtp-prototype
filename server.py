from socket import *
import os
import sys
from datetime import datetime
from helpers import *

# Numero de porta na qual o servidor estara esperando conexoes.
serverPort = 26

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
    while SERVER_STATE != 4:

      # Mensagem do usuário
      sentence = connectionSocket.recv(1024).decode('UTF-8')

      # Estado 0 (Aguardando HELO, QUIT)
      if (SERVER_STATE == 0):
        
        SERVER_STATE = verificar_comando(connectionSocket, sentence, ['HELO', 'QUIT'], SERVER_STATE)

        if (SERVER_STATE == COMANDOS_ENUM["HELO"] and not helo(connectionSocket, sentence)):
            SERVER_STATE = 0

      # Estado 1 (aguardando MAIL FROM, QUIT)
      elif (SERVER_STATE == 1):
      
        message = ''
        rcpt = []

        SERVER_STATE = verificar_comando(connectionSocket, sentence, ['MAIL FROM', 'QUIT'], SERVER_STATE)

        if (SERVER_STATE == COMANDOS_ENUM["MAIL FROM"] and mail_from(connectionSocket, sentence)):
          print('MAIL FROM recebido, aguardando RCPT TO ou QUIT.')

      # Estado 2 (aguardando RCPT TO, QUIT e DATA caso já tenha recebido RCPT TO)    
      elif (SERVER_STATE == 2):
        SERVER_STATE = verificar_comando(connectionSocket, sentence, ['RCPT TO', 'DATA', 'QUIT', 'MAIL FROM'], SERVER_STATE)

        if (SERVER_STATE == COMANDOS_ENUM["RCPT TO"]):
          SERVER_STATE = 2
          rcpt_aux = rcpt_to(connectionSocket, sentence, rcpt)

          if (rcpt_aux): 
            rcpt = rcpt_aux
            print('Adicionando', rcpt_aux, 'na lista de destinatários.')
            print('Destinatários:', rcpt)
            print('RCPT TO recebido, aguardando outros RCPT TO, DATA ou QUIT.')

        elif (SERVER_STATE == COMANDOS_ENUM["MAIL FROM"] and mail_from(connectionSocket, sentence)):
          print('MAIL FROM recebido, resetando lista de destinatários.')
          rcpt = []
            
        elif (SERVER_STATE == COMANDOS_ENUM["DATA"] and not data(connectionSocket, rcpt, sentence)):
          SERVER_STATE = 2

      # Estado 3 (aguardando mensagens do data e o '.')
      elif (SERVER_STATE == 3):
        if (sentence == '.'): 
          message += '\n.\n'
          connectionSocket.send('250 Message accepted for delivery'.encode('UTF-8'))
          print('Mensagem enviada, esperando novo MAIL FROM ou QUIT.')
          write_data(rcpt, message)
          SERVER_STATE = 1
        else: message += (sentence + '\n')

    # Estado 4 (QUIT)
    print('Encerrando conexão atual.')
    quit(connectionSocket)


main()