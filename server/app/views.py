from flask import request, json, make_response, redirect, url_for, session, \
    Blueprint, render_template

from app.models import db, User


views = Blueprint('views', __name__)


def safer_commit(session):
    try:
        session.commit()
        return True
    except:
        session.rollback()
        raise
    finally:
        return False

def render_user_profile(open_id):
    user = User.query.filter_by(open_id=open_id).first()
    # if user.status == UserStatus.NonSex:
    return "test"

@views.route('/', methods=['GET'])
def index():
    if 'open_id' in session:
        return render_user_profile(session['open_id'])

    open_id = request.args.get('open_id')
    if open_id:
        user = User.query.filter_by(open_id=open_id).first()
        gender = 'M'
        if not user:
            user = User(open_id=open_id, gender=gender)
            db.session.add(user)

            if not safer_commit(db.session):
                error = 'Something went wong. Please contact staff.'
                return render_template('index.html', error=error)

        return render_template('index.html', gender=gender)

    error = 'You must view this page with WeChat.'
    return render_template('index.html', error=error)


@views.route('/tutorial', methods=['GET'])
def tutorial():
    print(2)
    return 'ok'


@views.route('/status', methods=['GET'])
def status():
    open_id = request.args.get('open_id')
    return 'ok'


@views.route('/interest', methods=['POST'])
def interest():
    gender = reuqest.args.get('interest')
    return ''
