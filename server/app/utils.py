from app.models import User, UserStatus


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
    if users:
        return users.first()
    return None


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
