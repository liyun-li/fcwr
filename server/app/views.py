from flask import request, session, Blueprint, render_template
from sqlalchemy import or_
from app.models import db, User, Group, Matched, UserStatus
from app.utils import safer_commit, get_user, set_status, validate_user
from os import getenv
from json import dumps
import xmltodict
import hashlib


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    request_open_id = request.args.get('open_id')
    session_open_id = session.get('open_id')

    # print(session.items())
    if not request_open_id and not session_open_id:
        error = 'You must view this page with WeChat.'
        return render_template('index.html', error=error)

    open_id = request_open_id
    if not validate_user(open_id):
        error = 'You must view this page with WeChat.'
        return render_template('index.html', error=error)

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
    else:
        session['gender'] = user.gender
        session['preference'] = user.preference
        session['open_id'] = user.open_id
        session['status'] = str(user.status)\
            .replace('UserStatus.', '')

        if user.status == UserStatus.Assigned:
            return render_template(
                'index.html',
                gender=session['gender'],
                preference=session['preference'],
                status=session['status'],
                group_id=user.group_id
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


@views.route('/rematch', methods=['GET'])
def rematch():
    open_id = session.get('open_id')

    if not validate_user(open_id):
        return 'You must open this page with WeChat', 403

    user = get_user(open_id)

    if not user:
        return '', 404

    match = get_user(user.match)

    if not match:
        return '', 404

    # delete user from queue
    db.session.delete(user)
    if not safer_commit():
        return 'Something went wrong. Please talk to staff', 500

    matched = Matched(user_1=user.open_id, user_2=match.open_id)
    db.session.add(matched)
    # commit the matched pair
    if not safer_commit():
        return 'Something went wrong. Please talk to staff', 500

    # set status of the user matched with user
    set_status(match)
    if not safer_commit():
        return 'Something went wrong. Please talk to staff', 500

    # add user to the end of list (hopefully)
    new_user = User(
        open_id=user.open_id, gender=user.gender,
        preference=user.preference)

    db.session.add(new_user)
    if not safer_commit():
        return 'Something went wrong. Please talk to staff', 500

    # set match of new user's status
    set_status(new_user)
    if not safer_commit():
        return 'Something went wrong. Please talk to staff', 500

    # get group id
    group = Group.query.filter_by(group_id=user.group_id).first()
    if not group:
        return 'Something went wrong. Please talk to staff', 500

    # and remove it
    db.session.delete(group)
    if not safer_commit():
        return 'Something went wrong. Please talk to staff', 500

    return '', 200


@views.route('/set_preference', methods=['POST'])
def set_preference():
    genders = ['M', 'F']
    data = request.get_json()
    gender = data.get('gender')
    preference = data.get('preference')
    open_id = session.get('open_id') or request.args.get('open_id')

    if not validate_user(open_id):
        return 'You must view this page with WeChat', 403

    if open_id and gender and preference and \
            gender in genders and preference in genders:

        user = get_user(open_id)
        if user:
            return 'You have already picked your preference', 403

        user = User(open_id=open_id, gender=gender, preference=preference)

        set_status(user)

        # whichever case it is, add user
        db.session.add(user)

        if safer_commit():
            session['gender'] = gender
            session['preference'] = preference

            return '', 200

    return 'Something went wrong. Please contact staff.', 403


@view.route('/super_secret_api_for_doing_nothing', methods=['POST'])
def validation():
    timestamp = request.args.get('timestamp')
    signature = request.args.get('signature')
    nonce = request.args.get('nonce')
    token = getenv('token')

    # if not timestamp or not signature or not nonce or not token:
    # return '', 403

    print(timestamp)
    print(signature)
    print(nonce)

    tmp_arr = [str(timestamp), str(nonce)]
    tmp_arr.sort()
    tmp_str = ''.join(tmp_arr)

    m = hashlib.sha1()
    m.update(tmp_str.encode())
    print(m.digest(), signature)
    print(m.digest() == signature)

    xml = xmltodict.parse(request.data).get('xml')

    if not xml:
        return '', 403

    open_id = xml.get('FromUserName')
    if not open_id:
        return '', 403

    return '', 200
