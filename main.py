import unittest
from flask import make_response, request, redirect, render_template, session
from flask_login import login_required, current_user

from app import create_app
from app.firestore_service import get_users, get_todos
app = create_app()

todos = ['Enviar café', 'Solicitar respuesta', 'Confirmar con el comprador']

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    context ={
        'user_ip':user_ip,
        'todos':get_todos(user_id=username),
        'username':username
    }
    return render_template('hello.html', **context)

