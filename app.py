"""
Este é um módulo Flask simples para renderizar uma página inicial.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """
    Função para renderizar a página inicial.

    Retorna:
        str: Uma mensagem de boas-vindas.
    """
    title = "TimeSync"
    message = "Sejam bem vindos ao siterrrr"
    return render_template('TimeSync.html', title=title,
                           message=message)


if __name__ == '__main__':
    app.run(debug=True)
