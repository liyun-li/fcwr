# 非诚勿扰

Offline Matchmaker

## Usage

To deploy:

```
pip install -r requirements.txt
cd server
echo DEVELOPMENT_MODE=yes > .env
python serve.py
```

Or use Docker Compose

```
docker-compose up
```

We are using Jinja 2 for our front end template. HTML documents are in `server/app/templates`. CSS and JS are in `server/app/static`.
