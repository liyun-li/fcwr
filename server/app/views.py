from flask import (
    request, json, make_response, redirect,
    url_for, session, Blueprint, render_template
)


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    open_id = request.args.get('open_id')
    return render_template('index.html')


@views.route('/tutorial', methods=['GET'])
def tutorial():
    return 'ok'


@views.route('/status', methods=['GET'])
def status():
    open_id = request.args.get('open_id')
    return 'ok'
