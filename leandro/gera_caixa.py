arquivo = open('usuarios.txt', 'r+')

usuarios = arquivo.readlines()

for i in range(len(usuarios)):
  usuario = (usuarios[i][0:-1] + ".txt")
  caixa = open(usuario, 'w')