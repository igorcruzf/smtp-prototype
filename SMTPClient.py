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

sentence = input('C: ').encode('UTF-8')
# Envio de bytes
clientSocket.send(sentence)

# Recepcao
response = clientSocket.recv(1024)
print('S:', response.decode('UTF-8'))

estado = 0

while (True):
  sentence = input('C: ').encode('UTF-8')

  # Envio de bytes
  clientSocket.send(sentence)

  if (estado == 0):
    # Recepcao
    response = clientSocket.recv(1024)
    print('S:', response.decode('UTF-8'))

    if (sentence == 'DATA'.encode('UTF-8') and response.decode('UTF-8')[0:3] == '354'): 
      estado = 1
    if (sentence == 'QUIT'.encode('UTF-8')):
      break
  elif (estado == 1):
    if (sentence == '.'.encode('UTF-8')):
      estado = 0
      response = clientSocket.recv(1024)
      print('S:', response.decode('UTF-8'))




  

# Fechamento
clientSocket.close()
