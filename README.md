# 非诚勿扰

Offline Matchmaker

## Dependencies

* Python 3
* PIP
* (Optional) Docker and Docker Compose
* (Optional) Python Virtual Environment

## Usage

To deploy in debug mode:

```
pip install -r requirements.txt
cd server
echo DEVELOPMENT_MODE=yes > .env
FLASK_MODE=1 python serve.py
```

Or use Docker Compose:

```
echo DEVELOPMENT_MODE=yes > server/.env
docker-compose up
```

We are using Jinja 2 as the rendering engine. The template files are in `server/app/templates`. CSS, JS and images are in `server/app/static`.
