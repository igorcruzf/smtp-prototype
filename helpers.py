import os
import sys
import re

COMANDOS_ENUM = {
  "HELO": 1,
  "MAIL FROM": 2,
  "DATA": 3,
  "QUIT": 4,
  "RCPT TO": 5
}

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

# Abre o arquivo inicial e cria as caixas de mensagem
def popula_caixa():
  try: 
    nomeCaixa = sys.argv[1]
  except:
    print('Atenção: Você deve inserir o nome do arquivo de usuários como parâmetro na linha de comando.')
    sys.exit()

  if os.path.isfile(nomeCaixa) == False:
    print('Atenção: Arquivo Inexistente, encerrando aplicação.')
    sys.exit()

  arquivo = open(nomeCaixa, 'r+')

  usuarios = arquivo.readlines()

  for i in range(len(usuarios)):
    usuarios[i] = usuarios[i].replace('<', '').replace('>', '')
    if usuarios[i][-1] != '\n':
        usuario = (usuarios[i] + ".txt")
    else:
        usuario = (usuarios[i][0:-1] + ".txt")
    caixa = open(usuario, 'a+')
    caixa.close()

# Escreve nas caixas de mensagem os emails enviados
def write_data(userList, data):
  for user in range(len(userList)):
    caixa = open(userList[user] + '.txt', 'a+')
    caixa.write(data + '\n\n')
    caixa.close()

# Checa se o comando digitado é um dos comandos aceitos no atual estado da aplicação
def verificar_comando(connectionSocket, sentence, comandos, serverState):
  if (':' in sentence):
    comando = sentence.split(':')[0]
  elif (' ' in sentence):
    comando = sentence.split()[0]
  else: comando = sentence

  if(comando in comandos):
    return COMANDOS_ENUM[comando]

  if(comando in COMANDOS_ENUM):
    connectionSocket.send("503 Bad sequence error, command used in the wrong order".encode('UTF-8'))
  else:
    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))

  return serverState


def helo(connectionSocket, sentence):
  try: 
    message = "250 Hello " + sentence.split()[1] + ", pleased to meet you"
    connectionSocket.send(message.encode('UTF-8'))
    print('HELO recebido, aguardando por MAIL FROM ou QUIT.')
    return True  
  except:
    connectionSocket.send("501 Syntax error, invalid parameter".encode('UTF-8'))
    return False


def quit(connectionSocket):
  connectionSocket.send("221 redes.uff closing connection".encode('UTF-8'))
  connectionSocket.close()


def mail_from(connectionSocket, sentence):

  sentence = sentence.replace('MAIL FROM: ', '', 1)

  if (('<' != sentence[0]) or ('>' != sentence[-1])):
    connectionSocket.send("501 Syntax error, invalid parameter".encode('UTF-8'))
    return False

  sentence = sentence.replace('<', '', 1).replace('>', '', 1)

  if(not re.search(regex, sentence)):
    connectionSocket.send("501 Syntax error, invalid parameter".encode('UTF-8'))
    return False

  message = '250 ' + sentence + '... Sender ok'
  connectionSocket.send(message.encode('UTF-8'))
  return True



def rcpt_to(connectionSocket, sentence, rcpt):

  sentence = sentence.replace('RCPT TO: ', '', 1)

  if ((not ('@' in sentence)) or (len(sentence) < 1) or (('<' != sentence[0]) or ('>' != sentence[-1]))):
    connectionSocket.send("501 Syntax error, invalid parameter".encode('UTF-8'))
    return False

  sentence = sentence.replace('<', '', 1).replace('>', '' , 1)
  email = sentence.split('@')
  # email[0] = nome / email[1] = dominio

  if (email[1] != 'redes.uff' or len(email) != 2): 
    connectionSocket.send("550 Address unknown".encode('UTF-8'))
    return False

  # Checando se o usuário existe (verifica existência da caixa de entrada)
  if(os.path.isfile(email[0] + '.txt')):
    if (email[0] in rcpt):
      print('E-mail já presente na lista de destinatários.')
    else: 
      rcpt.append(email[0])

    message = '250 ' + email[0] + '@redes.uff' + '... Recipient ok'
    connectionSocket.send(message.encode('UTF-8'))
    return rcpt

  else:
    connectionSocket.send("550 Address unknown".encode('UTF-8'))
    return False

def data(connectionSocket, rcpt, sentence):
  if (sentence != 'DATA'):
    print('DATA com parâmetros inválidos')
    connectionSocket.send("501 Syntax error, invalid parameter".encode('UTF-8'))
    return False

  if (len(rcpt) < 1):
    print('DATA recebido sem destinatários definidos.')
    connectionSocket.send("503 Bad sequence error, command used in the wrong order".encode('UTF-8'))
    return False

  print('DATA recebido, aguardando texto da mensagem e o "." final')
  connectionSocket.send('354 Enter mail, end with "." on a line by itself'.encode('UTF-8'))
  return True