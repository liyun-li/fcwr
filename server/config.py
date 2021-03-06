from dotenv import load_dotenv
from pathlib import Path
from redis import Redis
from os import getenv

load_dotenv(verbose=True)


class Config:
    # database variables
    dbuser = getenv('DB_USER')
    dbpass = getenv('DB_PASS')
    dbhost = getenv('DB_HOST')
    dbname = getenv('DB_NAME')
    dbport = 3306

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://'

    if getenv('DB_PORT'):
        port = int(getenv('DB_PORT'))

    SQLALCHEMY_DATABASE_URI += '{u}:{p}@{h}:{pt}/{n}'.format(
        u=dbuser, p=dbpass, h=dbhost, pt=dbport, n=dbname
    )

    if getenv('DEVELOPMENT_MODE'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    elif not (dbuser and dbhost and dbname):
        print('.env configuration incomplete')
        exit(1)

    # session
    # https://pythonhosted.org/Flask-Session/
    # 'filesystem' is an alternative if you don't want to use Redis
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/'

    SECRET_KEY = '823rFF43j2f 0u4mc-r0329ASDcu'

    # track DB mod
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # template autoreload
    TEMPLATES_AUTO_RELOAD = True

    # Debug mode
    DEBUG = False

    WECHAT_TOKEN = getenv('TOKEN')
