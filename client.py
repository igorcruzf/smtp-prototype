from socket import *

serverName = 'localhost'
serverPort = 26

# Criacao do socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# Conexao com o servidor
clientSocket.connect((serverName,serverPort))

# Recepcao
response = clientSocket.recv(1024)
print('S:', response.decode('UTF-8'))

sentence = input('C: ')
# Envio de bytes
clientSocket.send(sentence.encode('UTF-8'))

# Recepcao
if (sentence != ''): 
  response = clientSocket.recv(1024)
  print('S:', response.decode('UTF-8'))

# Estado 0 - Cliente espera mensagem do servidor
# Estado 1 - Cliente não espera mensagem do servidor
estado = 0

while (True):
  if (estado == 0 and response.decode('UTF-8')[0:3] == '221'):
    break

  sentence = input('C: ')

  # Envio de bytes
  if (estado == 1 and sentence == ''): clientSocket.send('\n'.encode('UTF-8'))     
  else: clientSocket.send(sentence.encode('UTF-8'))

  if (estado == 0):
    # Recepcao
    if (sentence != ''): 
      response = clientSocket.recv(1024)
      print('S:', response.decode('UTF-8'))

    if (response.decode('UTF-8')[0:3] == '354'): 
      estado = 1

  elif (estado == 1):
    if (sentence == '.'):
      estado = 0
      response = clientSocket.recv(1024)
      print('S:', response.decode('UTF-8'))

# Fechamento
clientSocket.close()