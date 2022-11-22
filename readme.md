## HealthBuddy Backend

## Development Setup

### Local Setup

- `git clone https://github.com/abhijeet-dhumal/healthybuddy-pro.git`

- `cd duonut-back`

- Create Virtual Environment `virtualenv venv`

- Activate Virtual Environment 
    - Windows - `venv/Scripts/activate.ps1`
    - Linux - `source venv/bin/activate`

- Install Dependencies `pip install -r requirements.txt`

- Add `.env` file

- Run Migratations `python manage.py migrate`

- Create Super User `python manage.py createsuperuser`
    - Enter Username and Password and Create Super User

- Start Server `python manage.py runserver`


## Env file
```
SECRET_KEY="django-insecure-s8zejlj)(4kzb(&izzgd#@02qltd=h29bxu#pdlo^$n(7^g2+0"
DEBUG=True
ALLOWED_HOSTS="*"


EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER="youremail@gmail.com"
EMAIL_HOST_PASSWORD="yourgmailpass"
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=""
DEFAULT_EMAIL_TO=""


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=""
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=""
```

## API Documentation
- `http://localhost:8000/docs`
