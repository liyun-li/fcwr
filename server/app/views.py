from flask import request, json, make_response, redirect, url_for, session, \
    Blueprint, render_template

from sqlalchemy import or_

from app.models import db, User, Matches, UserStatus
from app.utils import safer_commit, get_user, render_user_profile

from random import randint
from json import dumps

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    request_open_id = request.args.get('open_id')
    session_open_id = session.get('open_id')

    print(session.items())

    if not request_open_id and not session_open_id:
        error = 'You must view this page with WeChat.'
        return render_template('index.html', error=error)

    open_id = request_open_id
    if not request_open_id:
        open_id = session_open_id
    elif request_open_id != session_open_id:
        session.clear()

    user = get_user(open_id)

    if not user:
        session['gender'] = None
        session['preference'] = None
        session['open_id'] = open_id
        session['status'] = str(UserStatus.Selecting)\
            .replace('UserStatus.', '')
    elif user:
        session['gender'] = user.gender
        session['preference'] = user.preference
        session['open_id'] = user.open_id
        session['status'] = str(user.status)\
            .replace('UserStatus.', '')

        if user.status == UserStatus.Assigned:
            group = Matches.query.filter(
                or_(Matches.user_1 == open_id, Matches.user_2 == open_id)
            ).first()
            return render_template(
                'index.html',
                gender=session['gender'],
                preference=session['preference'],
                status=session['status'],
                group_id=group.group_id
            )

    return render_template(
        'index.html',
        gender=session['gender'],
        preference=session['preference'],
        status=session['status']
    )


@views.route('/tutorial', methods=['GET'])
def tutorial():
    return ''


@views.route('/set_preference', methods=['POST'])
def interest():
    genders = ['M', 'F']
    data = request.get_json()
    gender = data.get('gender')
    preference = data.get('preference')
    open_id = session['open_id'] or request.args.get('open_id')

    if open_id and gender and preference and \
            gender in genders and preference in genders:

        user = get_user(open_id)
        if user:
            return 'You have already picked your preference', 403

        user = User(open_id=open_id, gender=gender, preference=preference)

        user_waiting = User.query.filter_by(
            preference=gender, gender=preference,
            status=UserStatus.Waiting).order_by(User.id).first()

        if user_waiting:
            user_waiting.status = UserStatus.Assigned
            user.status = UserStatus.Assigned
            matches = Matches(
                group_id=randint(1000, 9999),
                user_1=user_waiting.open_id, user_2=user.open_id)
            db.session.add(matches)
        else:
            user.status = UserStatus.Waiting

        db.session.add(user)
        if safer_commit(db.session):
            session['gender'] = gender
            session['preference'] = preference

        return '', 200

    return 'Something went wrong. Please contact staff.', 403
