from flask import Flask, send_file, render_template, request, redirect, session, url_for, flash, get_flashed_messages

import os
from dotenv import load_dotenv
import psycopg2
import io

app = Flask(__name__)
app.secret_key = 'viajapass'

load_dotenv('C:/Users/dantf/Documents/projeto-viajapass/config.env')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = psycopg2.connect(
            host="localhost",
            database="viajapass",
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'))
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT password FROM usuarios WHERE username = %s", (username,))
                user = cursor.fetchone()
                if user and user[0] == password:
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    flash('O login falhou, tente novamente!', 'error') 
                    return redirect(url_for('login'))
        except Exception as e:
            print(f"Erro ao autenticar o usuário: {e}")
        finally:
            conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def get_pdf_from_db(telefone):
    conn = psycopg2.connect(
        host="localhost",
        database="viajapass",
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'))

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT content FROM pdfs WHERE telefone = %s", (telefone,))
            pdf_content = cursor.fetchone()
            if pdf_content is not None:
                return pdf_content[0]
            else:
                return None
    except Exception as e:
        print(f"Erro ao recuperar PDF do banco de dados: {e}")
    finally:
        conn.close()
        
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/download-pdf/')
@login_required
def download_pdf():
    telefone = request.args.get('telefone')
    pdf_content = get_pdf_from_db(telefone)
    if pdf_content:
        return send_file(
            io.BytesIO(pdf_content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{telefone}.pdf'
        )
    else:
        flash('Arquivo não encontrado!', 'error') 
        return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
