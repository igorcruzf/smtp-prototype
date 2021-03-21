from socket import *

serverName = 'localhost'
serverPort = 12000

# Criacao do socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# Conexao com o servidor
clientSocket.connect((serverName,serverPort))

sentence = input('Input lowercase sentence:').encode('UTF-8')
# Envio de bytes
clientSocket.send(sentence)

# Recepcao
modifiedSentence = clientSocket.recv(1024)
print('From Server:', modifiedSentence.decode('UTF-8'))

# Fechamento
clientSocket.close()
