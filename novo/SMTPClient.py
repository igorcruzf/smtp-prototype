from socket import *

serverName = 'localhost'
serverPort = 25

# Criacao do socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# Conexao com o servidor
clientSocket.connect((serverName,serverPort))

# Recepcao
response = clientSocket.recv(1024)
print('S:', response.decode('UTF-8'))

sentence = input('Send a message: ').encode('UTF-8')
# Envio de bytes
clientSocket.send(sentence)

# Recepcao
response = clientSocket.recv(1024)
print('From Server:', response.decode('UTF-8'))

estado = 0

while (True):
  sentence = input('Send a message: ').encode('UTF-8')

  # Envio de bytes
  clientSocket.send(sentence)

  if (estado == 0):
    # Recepcao
    response = clientSocket.recv(1024)
    print('From Server:', response.decode('UTF-8'))

  if (sentence == 'DATA'.encode('UTF-8')):
    print('Mudando estado por causa da DATA') 
    estado = 1
  elif (sentence == '.'.encode('UTF-8')): estado = 0




  

# Fechamento
clientSocket.close()
