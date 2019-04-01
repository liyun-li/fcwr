from flask import request, json, make_response, redirect, url_for, session, \
    Blueprint, render_template
from app.models import db, User

views = Blueprint('views', __name__)

def safer_commit(session):
    try:
        session.commit()
        return True
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        session.rollback()
        return False
      
@views.route('/tutorial', methods=['GET'])
def tutorial():
    return 'ok'

@views.route('/', methods=['GET'])
def index_2():
    open_id = request.args.get('open_id')
    if open_id:
        session['open_id'] = open_id
        user = User.query.filter_by(open_id=open_id).first()
        # New User
        if not user:
            user = User(open_id=open_id)
            db.session.add(user)
            if not safer_commit(db.session):
                return 'Something went wong. Please contact staff.'
        # User already matched
        if user.number != None:
            return str(user.number);
        # User is matching
        if user.gender != None and user.like_gender != None:
            return 'matching';
        # Setting the user sex
        return render_template('index.html')

    error = 'You must view this page with WeChat.'
    return render_template('index.html', error=error)

@views.route('/setSexAndInterest', methods=['POST'])
def selfsex():
    open_id = session['open_id']
    user = User.query.filter_by(open_id=open_id).first()
    user.gender = request.form['gender']
    user.like_gender = request.form['like_gender']
    db.session.add(user)
    if not safer_commit(db.session):
        return 'Something went wong. Please contact staff.'
    return "success"

@views.route("/matching", methods=['GET'])
def matching():
    return render_template('matching.html')

# ---------------------------- For Test
@views.route('/testSession', methods=['GET'])
def hello():
    if 'open_id' in session:
        print(session['open_id'])
        open_id = session['open_id']
        user = User.query.filter_by(open_id=open_id).first()
        print(user.number)
        return 'you have logged in'
    return 'you have NOT logged in'

@views.route('/testWebsockt', methods=['GET'])
def test():
    return render_template('matching.html')
