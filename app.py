from flask import request, session, flash, Flask, render_template, redirect, url_for
import calendar 
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from hashlib import sha256



app = Flask(__name__)
app.secret_key = os.urandom(12) 

# Se o site nn pegar e pq eu esqueci de mudar essa prr pro teu login
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' # muda pra user
app.config['MYSQL_PASSWORD'] = 'abc12345' # muda pra password
app.config['MYSQL_DB'] = 'mydb'

app.jinja_env.globals.update(
    foda=lambda a: str(a).zfill(2), 
    foda2=lambda a: str(a)[:-3], 
    foda3=lambda a: {"baixa": "Baixa", "media": "Média", "alta": "Alta"}[a]
)

mysql = MySQL(app)


"""
mydb = mysql.connector.connect(host="localhost", user="user", password="password")
cursor = mydb.cursor()
cursor.execute("use mydb")
"""


@app.route('/Logout', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = sha256(request.form['password'].encode("utf-8")).hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM TB_usuario WHERE nome_usuario = % s and senha = 0x{password}', (username, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['nome_usuario']
            msg = 'Logado com sucesso'
            return redirect("/Home", code=302)
        else:
            msg = 'E-mail ou senha incorretos. Tente novamente.'
            return render_template('Logout.HTML')
        """
        if email == 'email@admin.com' and password == '123':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha incorretos. Tente novamente.')
            return redirect(url_for('login'))
        """
    else:
        return render_template('Logout.HTML')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/Cadastrar', methods =['GET', 'POST'])
def Cadastrar():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        apelido = request.form['apelido']
        password = sha256(request.form['password'].encode("utf-8")).hexdigest()
        email = request.form['email']
        data = request.form['data']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM TB_usuario WHERE nome_usuario = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Essa conta ja existe'
            flash(msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Email invalido'
            flash(msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Nome de usuario deve conter apenas letras e numeros'
            flash(msg)
        elif not re.match(r'[A-Za-z0-9]+', apelido):
            msg = 'Nome de usuario deve conter apenas letras e numeros'
            flash(msg)
        elif not username or not password or not email or not data:
            msg = 'Preencha todos os campos'
            flash(msg)
        else:
            cursor.execute(f'INSERT INTO TB_Usuario VALUES (% s, % s, % s, % s, % s, 0x{password})', (username, apelido, email, data, None ))
            mysql.connection.commit()
            msg = 'Registrado com sucesso'
            flash(msg)
    elif request.method == 'POST':
        msg = 'Por favor preencha os campos.'
        flash(msg)
    return render_template('Cadastrar.html', msg = msg)

@app.route('/Equipe')
def equipe():
    if not session.get('loggedin'):
        return render_template('Logout.html')
    

    return render_template('Equipe.html')

@app.route('/Sobre')
def sobre():
    if not session.get('loggedin'):
        return render_template('Logout.html')
    return render_template('Sobre.html')    

def list_fetch(fetch):
    return list(map(lambda a: list(a.values())[0], fetch))

def date_to_string(date):
    return f"{str(date.day).zfill(2)}/{str(date.month).zfill(2)}/{date.year}"

def contagem_foda(cursor):
    cursor.execute("SELECT COUNT(*) FROM tb_eventos")
    print("Eventos totais:", list(cursor.fetchone().values())[0])

    cursor.execute("SELECT dia FROM tb_eventos GROUP BY dia")
    dias = list(map(date_to_string, list_fetch(cursor.fetchall())))
    cursor.execute("SELECT COUNT(dia) FROM tb_eventos GROUP BY dia")
    print("Quantidade de eventos em cada dia:", dict(zip(dias, list_fetch(cursor.fetchall()))))
    
    cursor.execute("SELECT COUNT(dia) FROM tb_eventos  WHERE importancia = \"baixa\"")
    print("Eventos com importância baixa:", list(cursor.fetchone().values())[0])

    cursor.execute("SELECT COUNT(dia) FROM tb_eventos  WHERE importancia = \"media\"")
    print("Eventos com importância média:", list(cursor.fetchone().values())[0])

    cursor.execute("SELECT COUNT(dia) FROM tb_eventos  WHERE importancia = \"alta\"")
    print("Eventos com importância alta:", list(cursor.fetchone().values())[0])

    cursor.execute("SELECT distinct dia FROM tb_eventos")
    dias = list(map(date_to_string, list_fetch(cursor.fetchall())))
    print(f"Dias com eventos ({len(dias)})", dias)

@app.route('/')
@app.route('/Home', methods=["GET", "POST"]) 
def index():
    """
    Função para renderizar a página inicial.
    """
    if not session.get('loggedin'):
        return render_template('Logout.html')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.form:
        cursor.execute(f'INSERT INTO tb_eventos VALUES (str_to_date("{request.form["dia"]}", "%Y-%m-%d"), "{request.form["horario_comeco"]}", "{request.form["horario_fim"]}", "{request.form["modalidade"]}", "{request.form["importancia"]}", "{request.form["local"]}", "{session.get("username")}")')
        mysql.connection.commit()
    
    # Mapeamento de nomes de meses em português para números
    meses = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12
    }

    # Obter o mês e o ano da solicitação, ou definir o padrão
    mes = request.args.get('mes', default='Janeiro')
    ano = int(request.args.get('ano', default='2024'))
    mes_num = meses.get(mes, 1)  # Padrão para Janeiro se não encontrado
    title = mes

    # Navegar entre os meses
    direcao = request.args.get('direcao')
    if direcao == 'next':
        mes_num += 1
        if mes_num > 12:
            mes_num = 1
            ano += 1
    elif direcao == 'prev':
        mes_num -= 1
        if mes_num < 1:
            mes_num = 12
            ano -= 1

    # Obter o primeiro dia da semana (0 = Segunda-feira, 6 = Domingo) e o número de dias no mês
    primeiro_dia_semana, num_dias = calendar.monthrange(ano, mes_num)

    # Ajustar para que a semana comece no domingo (0 = Domingo)
    primeiro_dia_semana = (primeiro_dia_semana + 1) % 7

    dias = []

    # Obter o número de dias do mês anterior
    if mes_num == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes_num - 1
        ano_anterior = ano

    num_dias_mes_anterior = calendar.monthrange(ano_anterior, mes_anterior)[1]
    true_mes = mes_num - 1
    true_ano = ano
    if true_mes <= 0:
        true_mes = 12
        true_ano = ano - 1
    # Preencher os dias do mês anterior
    for i in range(primeiro_dia_semana):
        dia_anterior = num_dias_mes_anterior - (primeiro_dia_semana - i - 1)
        dia_semana = (calendar.weekday(ano_anterior, mes_anterior, dia_anterior) + 1) % 7

        # Verificar se é sábado (6) ou domingo (0) e marcar como feriado
        classe = 'fds' if dia_semana == 6 or dia_semana == 0 else 'prev-month'
        feriado = 'Feriado' if classe == 'fds' else ''

        dias.append({'id': '', 'dia': dia_anterior, 'class': classe, 'feriado': feriado, 'mes': true_mes, 'ano': true_ano})
    true_mes = mes_num
    true_ano = ano
    # Preencher os dias do mês atual
    for i in range(1, num_dias + 1):
        dia = {'id': i, 'dia': i, 'class': '', 'feriado': '', 'mes': true_mes, 'ano': true_ano}
        dia_semana = (primeiro_dia_semana + i - 1) % 7

        # Verificar se é sábado (6) ou domingo (0) e marcar como feriado
        if dia_semana == 6 or dia_semana == 0:
            dia['class'] = 'fds'
            dia['feriado'] = 'Feriado'
        else:
            dia['class'] = 'dias'
        dias.append(dia)

    true_mes = mes_num + 1
    if true_mes > 12:
        true_mes = 1
        true_ano = ano + 1
    # Preencher os dias do próximo mês para completar 42 células
    proximo_dia = 1
    if mes_num == 12:
        proximo_mes = 1
        ano_proximo = ano + 1
    else:
        proximo_mes = mes_num + 1
        ano_proximo = ano

    num_dias_proximo_mes = calendar.monthrange(ano_proximo, proximo_mes)[1]

    while len(dias) < 42:
        dia_semana = len(dias) % 7
        classe = 'fds' if dia_semana == 6 or dia_semana == 0 else 'dias'
        if proximo_dia > num_dias_proximo_mes:
            proximo_dia = 1
        dias.append({'ano': true_ano, 'mes': true_mes, 'id': '', 'dia': proximo_dia, 'class': classe, 'feriado': 'Feriado' if classe == 'fds' else ''})
        proximo_dia += 1

    # Debugging: print variables to check values
    print(f"Month: {mes_num}, Year: {ano}")
    cursor.execute(f"SELECT * from tb_eventos WHERE nome_usuario_fk = \"{session.get("username")}\"")
    eventos = cursor.fetchall()
    for evento in eventos:
        for dia in dias:
            if dia["dia"] != evento["dia"].day or dia["mes"] != evento["dia"].month or dia["ano"] != evento["dia"].year:
                continue
            dia["class"] += " evento"
            if "eventos" not in dia:
                dia["eventos"] = []
            dia["eventos"].append(evento)
    contagem_foda(cursor)
    return render_template('TimeSync.html', title=title, dias=dias, ano=ano)

if __name__ == '__main__':
    app.run(debug=True)


