from flask import request, json, make_response, redirect, url_for, session, \
    Blueprint, render_template

from app.models import db, User, UserStatus
from app.utils import safer_commit, get_user, render_user_profile

from random import randint


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

            db.session.add(user)

            if not safer_commit(db.session):
                error = 'Something went wong. Please contact staff.'
                return render_template('index.html', error=error)

        session['open_id'] = open_id
        session['gender'] = user.gender
        session['preference'] = user.preference
        session['status'] = user.status

        status = render_user_profile(open_id)
        return render_template('index.html', gender, status=UserStatus)


@views.route('/tutorial', methods=['GET'])
def tutorial():
    return 'ok'


@views.route('/set_preference', methods=['POST'])
def interest():
    genders = ['M', 'F']
    gender = reuqest.args.get('gender')
    preference = request.args.get('preference')
    open_id = session['open_id'] or request.args.get('open_id')

    if open_id and gender and preference and gender in genders and preference in genders:
        user = User(open_id=open_id, gender=gender, preference=preference)
        if safer_commit(db.session):
            user_waiting = User.query.filter_by(
                preference=gender, gender=preference,
                status=UserStatus.Waiting)

            if user_waiting:
                user_waiting.status = UserStatus.Assigned
                user.status = UserStatus.Assigned
                matches = Matches(
                    group_id=randint(1000, 9999),
                    user_1=user_waiting.open_id, user_2=user.open_id)
            else:

        db.session.add(user)

    return ''
