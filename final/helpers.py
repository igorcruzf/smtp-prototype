import os
import sys
from datetime import datetime

COMANDOS_ENUM = {
  "HELO": 1,
  "MAIL FROM": 2,
  "RCPT TO": 3,
  "DATA": 4,
  "QUIT": 5
}

# Abre o arquivo inicial e cria as caixas de mensagem
def popula_caixa():
  try: 
    nomeCaixa = sys.argv[1]
  except Exception as e:
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
  horario = datetime.now().strftime('%H:%M - %d/%m/%Y')
  for user in range(len(userList)):
    caixa = open(userList[user] + '.txt', 'a+')
    caixa.write(data + '\n\n')
    caixa.close()

# Checa se o comando digitado é um dos comandos aceitos no atual estado da aplicação
def verificar_comando(connectionSocket, sentence, comandos):
  if (':' in sentence):
    comando = sentence.split(':')[0]
  elif (' ' in sentence):
    comando = sentence.split()[0]
  else: comando = sentence


  for i in range(len(comandos)):
    if (comandos[i] == comando): 
      return COMANDOS_ENUM[comando]

  connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
  return False


def helo(connectionSocket, sentence):
  try: 
    message = "250 Hello " + sentence.split()[1] + ", pleased to meet you"
    connectionSocket.send(message.encode('UTF-8'))
    return True

  except Exception as e:
    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
    return False


def noop(connectionSocket):
  connectionSocket.send('250 OK'.encode('UTF-8'))


def vrfy(connectionSocket, sentence):
  try: 
    user = sentence.split()[1]
    if(os.path.isfile(user + '.txt')):
      message = '250 ' + user+ '@redes.uff'
      connectionSocket.send(message.encode('UTF-8'))
    else:
      connectionSocket.send("550 Address unknown".encode('UTF-8'))

  except Exception as e: 
    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))


def quit(connectionSocket):
  connectionSocket.send("221 redes.uff closing connection".encode('UTF-8'))
  connectionSocket.close()


def mail_from(connectionSocket, sentence):
  try: 
    sentence = sentence.replace(' ', '').split(':')[1]

    if ((not ('@' in sentence)) or (len(sentence) < 1) or (('<' != sentence[0]) or ('>' != sentence[-1]))): raise Exception()

    sentence = sentence.replace('<', '').replace('>', '')

    message = '250 ' + sentence + '... Sender ok'
    connectionSocket.send(message.encode('UTF-8'))
    return True

  except Exception as e:
    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
    return False

def rcpt_to(connectionSocket, sentence, rcpt):
  try:
    sentence = sentence.replace(' ', '').split(':')[1]

    if ((not ('@' in sentence)) or (len(sentence) < 1) or (('<' != sentence[0]) or ('>' != sentence[-1]))): raise Exception()

    sentence = sentence.replace('<', '').replace('>', '')
    email = sentence.split('@')
    # email[0] = nome / email[1] = dominio

    if (email[1] != 'redes.uff'): 
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

  except Exception as e:
    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
    return False

def data(connectionSocket, rcpt):
  if (len(rcpt) < 1):
    print('DATA recebido sem destinatários definidos.')
    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
    return False

  print('DATA recebido, aguardando texto da mensagem e o "." final')
  connectionSocket.send('354 Enter mail, end with ".". on a line by itself'.encode('UTF-8'))
  return True