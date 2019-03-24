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

@views.route('/', methods=['GET'])
def index():
    open_id = request.args.get('open_id')
    if open_id:
        session['open_id'] = open_id
        user = User.query.filter_by(open_id=open_id).first()
        # New User
        if not user:
            user = User(open_id=open_id)
            db.session.add(user)

            if not safer_commit(db.session):
                error = 'Something went wong. Please contact staff.'
                return render_template('index.html', error=error)
        # User already matched
        if user.number != null:
            return render_template('index.html', number=user.number)

    error = 'You must view this page with WeChat.'
    return render_template('index.html', error=error)


@views.route('/tutorial', methods=['GET'])
def tutorial():
    return 'ok'

@views.route('/selfsex', methods=['POST'])
def selfsex():
    user = User.query.filter_by(open_id=open_id).first()
    gender = reuqest.args.get('selfsex')
    return ''

@views.route('/interest', methods=['POST'])
def interest():
    gender = reuqest.args.get('interest')
    return ''


# For Test
@views.route('/hello', methods=['GET'])
def hello():
    if 'open_id' in session:
        print session['open_id']
        return 'you have logged in'
    return 'you have NOT logged in'
