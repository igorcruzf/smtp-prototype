import os
def checa_destinatario(destinatario):
    if os.path.isfile(destinatario +'.txt') == False:
        print("550 Address unknown")