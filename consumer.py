import sys
import os
import json
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
import psycopg2
from confluent_kafka import Consumer, KafkaException, KafkaError

load_dotenv('C:/Users/dantf/Documents/projeto-viajapass/config.env')

def generate(nome, email, telefone, checkin, pax, destino):
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
            pdf.drawImage('img/logo.png', 15, 740, 5.2*cm, 3*cm, mask='auto')
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


def createConsumer():

    topics = ['ezvjbeie-default']

    conf = {
        'bootstrap.servers': 'glider.srvs.cloudkafka.com:9094',
        'group.id': "%s-consumer" % 'ezvjbeie',
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-512',
        'sasl.username': 'ezvjbeie', #os.getenv('KAFKA_USER'),
        'sasl.password': 'JA3HCWSxJk2WDHEKidFlEyZ_yt5grzIs' #os.getenv('KAFKA_PASSWORD')
    }

    c = Consumer(conf)
    c.subscribe(topics)
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                
            print(msg.value())
            orders = msg.key()
            params = json.loads(orders.decode('utf-8'))
            nome = params["nome"]
            email = params["email"]
            telefone = params["telefone"]
            checkin = params["checkin"]
            pax = params["pax"]
            destino = "Florianópolis"
            destinoOpt = params["destino"]
            if destinoOpt == 'FLN':
                destino = 'Florianópolis'
            elif destinoOpt == 'BBCAM':
                destino = 'Balneário Camboriú'      

            generate(nome, email, telefone, checkin, pax, destino)

    except KeyboardInterrupt:
        sys.stderr.write('Aborted by user')

    c.close()

createConsumer()