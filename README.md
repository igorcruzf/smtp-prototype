<h1> Como rodar o programa </h1> 

  O programa utiliza linguagem python3.
  É necessário rodar de forma simultânea o servidor e o cliente, sendo que o servidor precisa ser levantado primeiro. Utilize os comandos:
  
    Para rodar o servidor:
      python server.py usuarios.txt
    
    Para rodar o cliente:
      python client.py

<h3> Comandos disponíveis: </h3>

- HELO _nome_do_dominio_
- MAIL FROM: _\<email@dominio\>_
- RCPT TO: _\<email@redes.uff\>_
- DATA
- QUIT


O fluxo de execução é dividido em estados, primeiro o cliente deve mandar uma requisição de **HELO**, com o nome do domínio, após a resposta do servidor de ok, o cliente deve mandar uma requisição de **MAIL FROM**, com um email válido, identificando o remetente. Após isso, pode reiniciar com um novo **MAIL FROM** ou começar uma lista de destinatários através do comando **RCPT TO**. Após definir pelo menos 1 destinário válido, pode ser utilizado também o comando **DATA** para iniciar a transmissão da mensagem. Todas requisições após o **DATA** serão considerados parte da mensagem até ser enviado uma requisição com apenas um "." como mensagem. Durante todos os estados, excluindo apenas o de **DATA**, será possível terminar a conexão através do comando **QUIT**.

<h3> Exemplo: </h3>

    S: 220 redes.uff
    C: HELO uff.br
    S: 250 Hello uff.br, pleased to meet you
    C: MAIL FROM: <h.i.l.t@uff.br>
    S: 250 h.i.l.t@uff.br... Sender ok
    C: RCPT TO: <thiago@redes.uff>
    S: 250 thiago@redes.uff... Recipient ok
    C: RCPT TO: <igor@redes.uff>
    S: 250 igor@redes.uff... Recipient ok
    C: DATA
    S: 354 Enter mail, end with "." on a line by itself
    C: Essa mensagem
    C: e um teste
    C: !!
    C: .
    S: 250 Message accepted for delivery
    C: QUIT
    S: 221 redes.uff closing connection

<h3> Códigos de status e seus significados: </h3>

    221 - encerrando conexão
    250 - ok
    354 - aguardando envio de dados
    500 - erro de sintaxe no comando
    501 - erro de sintaxe no parâmetro
    503 - comando válido usado fora de ordem
    550 - endereço não encontrado

<h3> Fontes: </h3>

   - https://www.serversmtp.com/smtp-error/
   - https://www.samlogic.net/articles/smtp-commands-reference.htm
   - Material assíncrono da aula.

<h3> Membros do grupo: </h3>
   
   - Higor Luiz
   - Igor Figueiredo
   - Leandro Josino
   - Thiago Laet
