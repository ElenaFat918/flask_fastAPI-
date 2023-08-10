"""
Генерация пути к статике
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/about/')
def about():
    context = {'title': 'Обомне', 'name': 'Харитон', }
    return render_template('about.html', **context)


if __name__ == "__main__":
    app.run(debug=True)