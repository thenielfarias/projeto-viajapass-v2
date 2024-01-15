import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from ctypes import *
from dotenv import load_dotenv
import os
import psycopg2
import sys

load_dotenv('C:/Users/dantf/Documents/projeto-viajapass/config.env')

def generate():
    # Get inputs
    print('Digite os dados do titular para gerar a compra')
    nome = input("Nome e sobrenome: ")
    while True:
        inputNome = "".join(nome.split())
        if inputNome.isalpha() is True:
            break
        else:
            nome = input("Verifique o nome e digite novamente: ")

    email = input("E-mail: ")
    patternMail = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    while True:
        if re.match(patternMail, email):
            break
        else:
            email = input("Digite um endereço de e-mail válido: ")

    telefone = input("Telefone: ")
    patternTel = r"^[0-9]*$"
    while True:
        if re.match(patternTel, telefone):
            break
        else:
            telefone = input("Digite um número de telefone válido: ")

    checkin = input("Data inicial de utilização [DD/MM/AAAA]: ")
    patternDate = r"^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$"
    while True:
        if re.match(patternDate, checkin):
            break
        else:
            checkin = input("Digite uma data válida: ")
    
    pax = input("Nº de viajantes: ")
    while True:
        if pax >= '1' and pax <= '6':
            break
        else:
            pax = input("Digite um número de viajantes entre 1 e 6: ")

    destinoOpt = input("Destino:\n1 - Florianópolis\n2 - Balneário Camboriú\nDigite o destino: ")
    while True:
        if destinoOpt == '1':
            destino = 'Florianópolis'
            break
        elif destinoOpt == '2':
            destino = 'Balneário Camboriú'
            break
        else:
            destinoOpt = input("Verifique a opção escolhida:\n1 - Florianópolis\n2 - Balneário Camboriú\nDigite o destino: ")
    # Generate QRCode
    def generateQRCode():
        try:
            qr = qrcode.QRCode(version=1,box_size=15,border=2)
            uri = "http://www.viajapass.com.br/admin/{}.pdf".format(telefone)
            qr.add_data(uri)
            qr.make(fit=True)
            img=qr.make_image(fill="Black",back_color="White")
            img.save("{}.png".format(telefone))
            print('QR code gerado com sucesso!')
        except:
            print('Erro ao gerar o QR code!')

    generateQRCode()
    # Generate PDF
    def generatePDF(cliente):
        try:
            nome_pdf = telefone
            pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
            x = 806
            for item, detalhe in cliente.items():
                x -= 15
                pdf.setFillColor(HexColor('#777777'))
                pdf.drawString(175, x, '{}: {}'.format(item, detalhe))
            y = 700
            for item, detalhe in atividades.items():
                y -= 15
                pdf.setFillColor(HexColor('#777777'))
                pdf.setFont("Helvetica", 12)
                pdf.drawString(15, y, '{} - {}'.format(item, detalhe))
            pdf.setTitle(nome_pdf)
            pdf.drawImage('logo.png', 15, 740, 5.2*cm, 3*cm, mask='auto')
            pdf.drawString(15, 730, '_'*84)
            pdf.setFillColor(HexColor('#003C52'))
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(175, 808, 'Detalhes da compra')
            pdf.drawString(15, 702, 'Atrações inclusas:')
            pdf.setFillColor(HexColor('#FA4067'))
            pdf.drawString(15, 488, 'QR code para admissão nas atrações:')
            pdf.drawImage(f'{telefone}.png', 85, 55, 15*cm, 15*cm)
            pdf.setFillColor(HexColor('#777777'))
            pdf.setFont("Helvetica", 12)
            pdf.drawString(15, 20, 'Central de atendimento: +55 (48) 999999999 | contato@viajapass.com.br')
            pdf.save()
            print('PDF criado com sucesso!')
        #except:
            #print('Erro ao gerar PDF')
        except Exception as e:
            print(f'Erro ao gerar PDF: {e}')  

    cliente = {'Nome do titular':f'{nome}', 'Início da utilização':f'{checkin}', 'Nº de pessoas':f'{pax}', 'Destino':f'{destino}'}

    if destino == 'Florianópolis':
        atividades = {'· Atração 01':'saídas qui, sex, sab | (endereço) | reservas pelo telefone (48) 999999999',
                  '· Atração 02':'todos os dias das 9h às 18h | (endereço) | não necessita reserva',
                  '· Atração 03':'funcionamento',
                  '· Atração 04':'funcionamento',
                  '· Atração 05':'funcionamento',
                  '· Atração 06':'funcionamento',
                  '· Atração 07':'funcionamento',
                  '· Atração 08':'funcionamento',
                  '· Atração 09':'funcionamento',
                  '· Atração 10':'funcionamento',
                  '· Atração 11':'funcionamento',
                  '· Atração 12':'funcionamento'
                 }
    elif destino == 'Balneário Camboriú':
        atividades = {'· Atração 01':'funcionamento',
                  '· Atração 02':'funcionamento',
                  '· Atração 03':'funcionamento',
                  '· Atração 04':'funcionamento',
                  '· Atração 05':'funcionamento',
                  '· Atração 06':'funcionamento',
                  '· Atração 07':'funcionamento',
                  '· Atração 08':'funcionamento',
                  '· Atração 09':'funcionamento',
                  '· Atração 10':'funcionamento',
                  '· Atração 11':'funcionamento',
                  '· Atração 12':'funcionamento'
                 }

    generatePDF(cliente)
    # Save DB
    def save_db():
        # To bytes string
        def get_pdf_content(telefone):
            with open(telefone, 'rb') as file:
                return file.read()
        
        pdf_content = get_pdf_content('{}.pdf'.format(telefone))

        def connect_db():
            return psycopg2.connect(
                host = "localhost",
                database = "vjps",
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'))

        def save_pdf_to_db(pdf_content, telefone):
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO pdfs (telefone, content) VALUES (%s, %s)", (telefone, pdf_content))
                conn.commit()
                print('Armazenado no banco de dados com sucesso!')
            except Exception as e:
                print(f"Erro ao salvar PDF no banco de dados: {e}")
            finally:
                conn.close()          
        save_pdf_to_db(pdf_content, telefone)

    save_db()
    # Send mail
    def sendMail():
        try:
            anexo = telefone

            subject = "ViajaPASS - Confirmação de compra"
            body = "Olá {}! Sua compra do ViajaPASS {} está confirmada. Segue anexo voucher digital.\nObrigado e aproveite!\n\nAtenciosamente,\nEquipe ViajaPASS".format(nome, destino)
            sender_email = os.getenv('SENDER_EMAIL')
            password = os.getenv('EMAIL_PASSWORD')
            receiver_email = email

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            filename = '{}.pdf'.format(anexo)  # In same directory as script

            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename = {filename}",
            )

            message.attach(part)
            text = message.as_string()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)
            
            print('E-mail enviado com sucesso!')
        #except:
            #print('Erro ao enviar e-mail!')
        except Exception as e:
            print(f'Erro ao enviar e-mail: {e}') 
    sendMail()

generate()