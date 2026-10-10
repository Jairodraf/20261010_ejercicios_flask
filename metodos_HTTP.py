from flask import request

@flask.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_post()
    else:
        return login_get()

# @flask.get('/login')
def login_get():
    return f'Estás logeado'

# @flask.post('/login')
def login_post():
    return f'Se han añadido los datos correctamente'