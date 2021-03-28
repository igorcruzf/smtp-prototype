import os
import sys

COMANDOS_ENUM = {
  "HELO": 1,
  "MAIL FROM": 2,
  "RCPT TO": 3,
  "DATA": 4,
  "RSET": 5,
  "VRFY": 6,
  "NOOP": 7,
  "QUIT": 8
}

# Abre o arquivo inicial e cria as caixas de mensagem
def popula_caixa():
  try: 
    nomeCaixa = sys.argv[1]
  except Exception as e:
    print('Atenção: Você deve inserir o nome do arquivo como parâmetro na linha de comando')
    sys.exit()

  if os.path.isfile(nomeCaixa) == False:
    print('Atenção: Arquivo Inexistente, encerrando aplicação')
    sys.exit()

  arquivo = open(nomeCaixa, 'r+')

  usuarios = arquivo.readlines()

  for i in range(len(usuarios)):
      if usuarios[i][-1] != '\n':
          usuario = (usuarios[i] + ".txt")
      else:
          usuario = (usuarios[i][0:-1] + ".txt")
      caixa = open('caixas/'+ usuario, 'a+')
      caixa.close()


# Checa se o comando digitado é um dos comandos aceitos no atual estado da aplicação
def verificar_comando(connectionSocket, sentence, comandos):
  if (':' in sentence):
    comando = sentence.split(':')[0]
  elif (' ' in sentence):
    comando = sentence.split()[0]
  else: comando = sentence

  print(comando)

  for i in range(len(comandos)):
    if (comandos[i] == comando): 
      print('É o comando', comando)
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
    if(os.path.isfile('caixas/' + user + '.txt')):
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
    if (len(sentence) < 1): raise Exception()
    message = '250 ' + sentence + '... Sender ok'
    connectionSocket.send(message.encode('UTF-8'))
    return True

  except Exception as e:
    connectionSocket.send("500 Syntax error, command unrecognized".encode('UTF-8'))
    return False

# def rcpt_to(connectionSocket, sentence):
  