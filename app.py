"""
Este é um módulo Flask simples para renderizar uma página inicial.
"""

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    """
    Função para renderizar a página inicial.

    Retorna:
        str: Uma mensagem de boas-vindas.
    """

    mes = request.args.get('mes', default='Janeiro')  # Obtém o mês, padrão é Janeiro
    title = mes

    feriados = {
        7: "Feriado",
        1: "Feriado",
        14: "Feriado",
        8: "Feriado",
        15: "Feriado",
        21: "Feriado",
        22: "Feriado",
        28: "Feriado",
        29: "Feriado"
    }

    dias = []
    # Lógica para determinar o número de dias no mês atual
    if mes in ["Janeiro", "Março", "Maio", "Julho", "Agosto", "Outubro", "Dezembro"]:
        num_dias = 31
    elif mes == "Fevereiro":
        num_dias = 28  # Considerando um ano não bissexto para simplificar
    else:
        num_dias = 30

    for i in range(1, num_dias + 1):
        dia = {'id': i, 'dia': i, 'class': '', 'feriado': ''}
        if i in feriados:
            dia['class'] = 'fds'
            dia['feriado'] = feriados[i]
        else:
            dia['class'] = 'dias'
        dias.append(dia)

    return render_template('TimeSync.html', title=title, dias=dias)


if __name__ == '__main__':
    app.run(debug=True)
