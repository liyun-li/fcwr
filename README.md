# 非诚勿扰

Offline Matchmaker

## Usage

To deploy:

```
cd server
echo DEVELOPMENT_MODE=yes > .env
pip install -r requirements.txt
python serve.py
```

Or use Docker Compose

```
docker-compose up
```

We are using Jinja 2 for our front end template. HTML documents are in `server/app/templates`. CSS and JS are in `server/app/static`.
