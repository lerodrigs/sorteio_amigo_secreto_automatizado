import smtplib
import uuid
import time
from twilio.rest import Client
from random import randint
from email.message import EmailMessage
    
def main():
    print("[Automatizador de sorteio para amigo secreto]\n\n")

    email_disparador  = str(input("Insira o email disparador: "))

    password = str(input("Insira a senha: "))
    
    amigos = buscar_amigos() 

    sorteados = sortear(amigos= amigos)

    server_email = conectar_email(email = email_disparador, password = password)

    client_twilio = conectar_twilio(sid = "<sid>", token = "<token>")

    print("Iniciando disparos do resultado do sorteio.")

    for amigo in sorteados:

        mensagem = "Oi {0}, seu amigo secreto é: <strong>{1}</strong>.</br></br>É <strong>SECRETO</strong> e não pode fofocar.".format(amigo["sorteante"].nome, str(amigo["sorteado"].nome).upper())

        enviar_email(amigo= amigo, mensagem= mensagem, server = server_email)

        enviar_sms(amigo= amigo, mensagem= mensagem, client = client_twilio)

        enviar_whatsapp(sorteados= sorteados, mensagem= mensagem, client = client_twilio)

        time.sleep(3)

    server_email.quit()

    print("Sorteio realizado.")
   
def sortear(amigos: []):
    sorteados = []

    qtd_amigos = len(amigos)

    contador=0

    while contador < qtd_amigos:        
        sorteante = amigos[randint(0, qtd_amigos-1)]

        sorteado = amigos[randint(0, qtd_amigos-1)]

        mesma_pessoa = sorteado.id == sorteante.id            

        foi_sorteado = (len(([x for x in sorteados if x["sorteado"].id == sorteado.id])) > 0)

        foi_sorteante = (len(([x for x in sorteados if x["sorteante"].id == sorteante.id])) > 0)

        if mesma_pessoa == False and foi_sorteado == False and foi_sorteante == False: 
            sorteados.append(dict(sorteante = sorteante, sorteado = sorteado))
            contador = contador + 1 

    print("Lista de sorteados criada!")

    return sorteados

def enviar_email(amigo, mensagem: str, server: smtplib.SMTP, email_disparador: str):    
    emailBody = EmailMessage()

    emailBody["From"] = email_disparador

    emailBody["Subject"] = "Sorteio - Amigo Secreto"

    emailBody["To"] = amigo["sorteante"].email
   
    emailBody.set_content(mensagem, subtype="html")

    server.sendmail(email_disparador, amigo["sorteante"].email, msg= emailBody.as_string())                

    print("Email para {0} enviado!".format(str(amigo["sorteante"].nome).upper()))   

def enviar_whatsapp(amigo, mensagem: str, client: Client):
    whatsapp = client.messages.create(body=mensagem, from_= "<twilio_whatsapp>", to= "whatsapp:" + amigo["sorteante"].celular)

    print("Whatsapp para {0} enviado! ".format(str(amigo["sorteante"].nome).upper()))

    print(whatsapp.sid)

def enviar_sms(amigo, mensagem: str, client: Client):
    sms = client.messages.create(body=mensagem, from_= "<twilio_celular>", to= amigo["sorteante"].celular)

    print("SMS para {0} enviado! ".format(str(amigo["sorteante"].nome).upper()))

    print(sms.sid)

def conectar_email(email: str, password: str):
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)

    server.starttls()

    server.login(email, password)

    print("Email disparador conectado.")

    return server

def conectar_twilio(sid: str, token: str): 
    return Client(sid, token)

class amigo: 
    def __init__(self, id, nome, email, celular):
        self.id = id
        self.nome = nome
        self.email = email
        self.celular = celular
    
def buscar_amigos():    
    amigos = []
    amigos.append(amigo(uuid.uuid4(), "fulano", "mowad35586@ikanid.com", "+5596981757173"))
    amigos.append(amigo(uuid.uuid4(), "ciclano", "mowad35586@ikanid.com", "+5596981757173"))
    amigos.append(amigo(uuid.uuid4(), "beltrano", "mowad35586@ikanid.com", "+5596981757173"))
    return amigos

if __name__ == "__main__":
    main()