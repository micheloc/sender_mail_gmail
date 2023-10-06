import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import parse_qs
from flask import Flask, request, send_file, render_template, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Função para configurar manualmente o CORS
def configure_cors(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    return response

def sender_email(objeto): 
    try:
        jsObj = json.loads(objeto)
        sender_mail = jsObj["sender_mail"][0]
        mail_key = jsObj["mail_key"][0]
        destine_mail = jsObj["destine_mail"][0]
        Titulo = jsObj["title"][0] 
        Message = jsObj["msg"][0] 

        email_destino = destine_mail

        mensagem = MIMEMultipart()
        mensagem["From"] = sender_mail
        mensagem["To"] = email_destino
        mensagem["Subject"] = Titulo
        mensagem.attach(MIMEText(Message, "html"))

        mensagem["Importance"] = "High"

        # Conexão com o servidor SMTP
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()

        # Autenticação no servidor SMTP
        smtp_server.login(sender_mail, mail_key)

        # Envio da mensagem
        smtp_server.sendmail(sender_mail, email_destino, mensagem.as_string())

        # Encerramento da conexão SMTP
        smtp_server.quit()
        return "E-mail enviado"
    except Exception as e:
        return str(e)

@app.route("/send_email", methods=['POST', 'OPTIONS'])
def send_mail():
    objeto = request.get_data().decode('utf-8')
    objeto = parse_qs(objeto)
    objeto = json.dumps(objeto)
    try:
        result = sender_email(objeto)
        if result == "E-mail enviado":
            return configure_cors(jsonify({"success": True, "message": "E-mail enviado com sucesso", "resultado": result}))
        else:
            return configure_cors(jsonify({"success": False, "message": result, "resultado": result}))
    except Exception as e:
        return configure_cors(jsonify({"success": False, "message": f"Erro ao converter os dados: {str(e)}"}))

    return "Ok "

@app.route("/")
@cross_origin()
def index():
    return "Olá"


    # 52.316.802.0001-09 