"""
Este é um módulo Flask simples para renderizar uma página inicial.
"""

from flask import Flask, render_template, request
import calendar 

app = Flask(__name__)


@app.route('/Logout')
def logout():
    """
    Pagina de logout e login tambem porra
    """
    return render_template('Logout.html')

@app.route('/')
@app.route('/Home') 
def index():
    """
    Função para renderizar a página inicial.
    """
    
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

    # Preencher os dias do mês anterior
    for i in range(primeiro_dia_semana):
        dia_anterior = num_dias_mes_anterior - (primeiro_dia_semana - i - 1)
        dia_semana = (calendar.weekday(ano_anterior, mes_anterior, dia_anterior) + 1) % 7

        # Verificar se é sábado (6) ou domingo (0) e marcar como feriado
        classe = 'fds' if dia_semana == 6 or dia_semana == 0 else 'prev-month'
        feriado = 'Feriado' if classe == 'fds' else ''

        dias.append({'id': '', 'dia': dia_anterior, 'class': classe, 'feriado': feriado})

    # Preencher os dias do mês atual
    for i in range(1, num_dias + 1):
        dia = {'id': i, 'dia': i, 'class': '', 'feriado': ''}
        dia_semana = (primeiro_dia_semana + i - 1) % 7

        # Verificar se é sábado (6) ou domingo (0) e marcar como feriado
        if dia_semana == 6 or dia_semana == 0:
            dia['class'] = 'fds'
            dia['feriado'] = 'Feriado'
        else:
            dia['class'] = 'dias'

        dias.append(dia)

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
        dias.append({'id': '', 'dia': proximo_dia, 'class': classe, 'feriado': 'Feriado' if classe == 'fds' else ''})
        proximo_dia += 1

    # Debugging: print variables to check values
    print(f"Month: {mes_num}, Year: {ano}")
    
    return render_template('TimeSync.html', title=title, dias=dias, ano=ano)

if __name__ == '__main__':
    app.run(debug=True)


