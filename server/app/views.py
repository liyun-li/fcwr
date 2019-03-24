from flask import request, json, make_response, redirect, url_for, session, \
    Blueprint, render_template

from app.models import db, User, UserStatus


views = Blueprint('views', __name__)


def safer_commit(session):
    try:
        session.commit()
        return True
    except:
        session.rollback()
        raise
    # finally:
    #     return False

def get_user(open_id):
    users = User.query.filter_by(open_id=open_id)
    if not users:
        return null
    else:
        return users.first()

def render_user_profile(open_id):
    user = get_user(open_id)
    if not user:
        return "user not find"

    if user.status == UserStatus.NonSex:
        return "please select sex and liked sex"
    elif user.status == UserStatus.Waiting:
        return "waiting in a queue"
    elif user.status == UserStatus.Assigned:
        return "you already assigned a number"
    else:
        return "invalid status"

@views.route('/', methods=['GET'])
def index():
    if 'open_id' in session:
        return render_user_profile(session['open_id'])

    open_id = request.args.get('open_id')

    if not open_id:
        error = 'You must view this page with WeChat.'
        return render_template('index.html', error=error)
    else:
        user = get_user(open_id)

        if not user:
            user = User(open_id=str(open_id), status=UserStatus.NonSex)
            print (user.open_id)
            print (user.gender)
            print (user.like_gender)
            print (user.status)

            db.session.add(user)

            if not safer_commit(db.session):
                error = 'Something went wong. Please contact staff.'
                return render_template('index.html', error=error)

        session['open_id'] = open_id
        return render_user_profile(open_id)

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
