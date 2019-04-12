from flask import session, request
from sqlalchemy import and_
from sqlalchemy.sql import exists
from app.models import db, User, Group, Matched, WeChatId, UserStatus
from random import randint


def validate_user(open_id):
    return WeChatId.query.filter_by(open_id=open_id).first()


def safer_commit():
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        raise
        return False


def get_user(open_id):
    return User.query.filter_by(open_id=open_id).first()


def get_group(group_id):
    return Group.query.filter_by(group_id=group_id).first()


def set_status(user):
    '''Set appropriate status for user based on several criterias'''

    open_id = user.open_id
    gender = user.gender
    preference = user.preference

    # get prefered match, see if there's any
    # first get users of interest
    # then filter out the ones already matched before
    waiting = User.query.filter_by(
        preference=gender, gender=preference,
        status=UserStatus.Waiting
    ).order_by(User.queue).all()

    # get the ones that are already matched once before
    # and don't match them again
    matched = {}
    for match in Matched.query.filter_by(user_1=open_id).all():
        matched[match.user_2] = 1
    for match in Matched.query.filter_by(user_2=open_id).all():
        matched[match.user_1] = 1

    match_waiting = None
    for i in range(len(waiting)):
        if waiting[i].open_id not in matched:
            match_waiting = waiting[i]
            break

    if match_waiting:  # if there's someone waiting for you
        # generate
        group_id = randint(1000, 9999)
        while Group.query.filter_by(group_id=group_id).first():
            group_id = randint(1000, 9999)

        group = Group(group_id=group_id)

        db.session.add(group)

        # adjust waitlist queue number
        # TODO: rewrite
        waitlist_1 = User.query.filter_by(
            gender=gender, preference=preference,
            status=UserStatus.Waiting
        ).all()

        waitlist_2 = User.query.filter_by(
            gender=match_waiting.gender,
            preference=match_waiting.preference,
            status=UserStatus.Waiting
        ).all()

        for waiting_user in waitlist_1:
            if waiting_user.queue > (user.queue or 1000000):
                waiting_user.queue -= 1

        for waiting_user in waitlist_2:
            if waiting_user.queue > match_waiting.queue:
                waiting_user.queue -= 1

        # set status to assigned
        match_waiting.status = UserStatus.Assigned
        # set match to match's open_id
        match_waiting.match = open_id
        # remove from queue
        match_waiting.queue = None
        # assign a group ID
        match_waiting.group_id = group_id

        # set status to assigned
        user.status = UserStatus.Assigned
        # set match to match's open_id
        user.match = match_waiting.open_id
        # remove from queue
        user.queue = None
        # assigned a group id
        user.group_id = group_id

    else:  # your prefered gender is on high demand!
        # count how many are waiting in front of you
        queue_count = User.query.filter_by(
            preference=preference, gender=gender,
            status=UserStatus.Waiting).order_by(User.id).count()

        # set status to waiting
        user.status = UserStatus.Waiting
        # set the number of people in front of user
        user.queue = queue_count + 1
        # set match to null
        user.match = None
        # set group_id to null
        user.group_id = None
