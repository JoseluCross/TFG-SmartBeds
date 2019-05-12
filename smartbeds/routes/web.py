import smartbeds.vars as v
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from smartbeds.routes import webapi as api


@v.app.route('/', methods=['GET'])
def home():
    context = {"page": {"page": 'login'}, "info": get_info(), "title": "Inicio"}
    if context['info']['login']:
        mod_request()
        response, code = api.beds()
        context['beds'] = response.get_json()["beds"]
    return render_template('home.html', **context)


@v.app.route('/auth', methods=['GET', 'POST'])
def login():
    context = {"page": {"page": 'login', "bad": False}, "info": get_info(), "title": "Iniciar Sesión"}
    if request.method == "POST":
        response, code = api.auth()
        if code == 200:
            response_json = response.get_json()
            session['token'] = response_json['token']
            session['role'] = response_json['role']
            session['username'] = response_json['username']
            return redirect(url_for("home"))
        context["page"]['nick'] = request.form['user']
        context["page"]['bad'] = True
        return render_template('auth/login.html', **context)
    else:
        return render_template('auth/login.html', **context)


@v.app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for("home"))


@v.app.route('/bed')
def cama_ejemplo():
    context = {'page': {'page': 'bed'}, 'info': get_info(), "title": "Cama"}
    return render_template('cama.html', **context)


@v.app.route('/bed/<bedname>', methods=['GET'])
def cama(bedname):
    pass


@v.app.route('/bed/mod/<bedname>', methods=['GET', 'POST'])
def modifica_cama(bedname):
    pass


@v.app.route('/bed/add', methods=['GET', 'POST'])
def nueva_cama():
    pass


@v.app.route('/bed/del/<bedname>', methods=['GET'])
def borrar_cama(bedname):
    pass


@v.app.route('/beds', methods=['GET'])
def camas():
    context = {"page": {"page": 'admin_beds'}, "info": get_info(), "title": "Administrar camas"}
    mod_request()
    response, code = api.beds()
    context['beds'] = response.get_json()["beds"]
    return render_template('camas.html', **context)


def get_info():
    if 'token' in session:
        try:
            return {"login": True, "role": session['role'], "user": session['username']}
        except KeyError:
            return {"login": False}
    else:
        return {"login": False}


def mod_request():
    data = dict(request.form)
    data['token'] = session['token']
    request.form = data  # Técnicamente esta operación no es legal, pero funciona
