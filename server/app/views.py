from flask import request, json, make_response, redirect, url_for, session, \
    Blueprint, render_template

from app.models import db, User, UserStatus
from app.utils import safer_commit, get_user, render_user_profile


views = Blueprint('views', __name__)


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
            user = User(open_id=open_id, status=UserStatus.NonSex)
            print(user.open_id)
            print(user.gender)
            print(user.like_gender)
            print(user.status)

            db.session.add(user)

            if not safer_commit(db.session):
                error = 'Something went wong. Please contact staff.'
                return render_template('index.html', error=error)

        session['open_id'] = open_id
        session['gender'] = user.gender
        session['interest'] = user.like_gender
        session['status'] = user.status

        status = render_user_profile(open_id)
        return render_template('index.html', gender, status=UserStatus)


@views.route('/tutorial', methods=['GET'])
def tutorial():
    return 'ok'


@views.route('/set_preference', methods=['POST'])
def interest():
    gender = reuqest.args.get('gender')
    preference = reuqest.args.get('preference')

    return ''
