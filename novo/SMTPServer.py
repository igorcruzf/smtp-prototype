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
      
    # Loop dos estados
    while 1:

      # Mensagem do usuário
      sentence = connectionSocket.recv(1024).decode('UTF-8')

      # Estado 0 (Aguardando HELO)
      if (SERVER_STATE == 0):
        
        comando_digitado = verificar_comando(connectionSocket, sentence, ['HELO'])

        if (comando_digitado):
          if (comando_digitado == COMANDOS_ENUM["HELO"] and helo(connectionSocket, sentence)):
            print('Trocando para estado 1')
            SERVER_STATE = 1

      # Estado 1 (aguardando MAIL FROM, RSET, VRFY, NOOP, QUIT)
      elif (SERVER_STATE == 1):
      
        comando_digitado = verificar_comando(connectionSocket, sentence, ['MAIL FROM', 'NOOP', 'VRFY', 'RSET', 'QUIT'])

        if (comando_digitado):
          if (comando_digitado == COMANDOS_ENUM["MAIL FROM"] and mail_from(connectionSocket, sentence)):
            print('Trocando para estado 2')
            SERVER_STATE = 2
          
          elif (comando_digitado == COMANDOS_ENUM["NOOP"]):
            print('Executando NOOP')
            noop(connectionSocket)

          elif (comando_digitado == COMANDOS_ENUM["VRFY"]):
            print('Executando VRFY')
            vrfy(connectionSocket, sentence)

          elif (comando_digitado == COMANDOS_ENUM["RSET"]):
            print('Executando RSET')
            connectionSocket.send("250 OK".encode('UTF-8'))
            pass

          elif (comando_digitado == COMANDOS_ENUM["QUIT"]):
            print('Executando QUIT')
            quit(connectionSocket)
            break

      # Estado 2 (aguardando RCPT TO, RSET, VRFY, NOOP, QUIT)    
      # elif (SERVER_STATE == 2):
      #   comando_digitado = verificar_comando(connectionSocket, sentence, ['HELO'])

      #   if (comando_digitado):
      #     if (comando_digitado == COMANDOS_ENUM["RCPT TO"] and rcpt_to()):
      #       SERVER_STATE = 3

      # Estado 3 (aguardando RCPT TO, DATA, RSET, VRFY, NOOP, QUIT)
      # elif (server_state == 3):


main()