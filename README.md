## Song Vault Backend Api

⭐ Star us on GitHub — it motivates us a lot!

- Music streaming backend api build with Django Rest Framework.

Live Project Link: coming soon

### Functionality

Authentication:

    ✅ SignUp
    ✅ Login
    ✅ Logout
    ❌ Reset Password
    ❌ Email Confirmation

Api endpoints:

    ✅ /api/accounts - authentication api routes
    ✅ /api/albums - albums api routes
    ✅ /api/artists - artists api routes
    ✅ /api/playlists - playlists api endpoints
    ✅ /api/songs - Songs api endpoints

User Actions:
:

Backend and Deployment:

- Python3
- Django
- Django Rest Framework
- Postgres database
- nginx - reverse proxy - when hosted
- gunicorn - uwsgi server - when hosted

### setup project locally

###### Create a virtual environment:

    >  python3 -m venv <environment name>

###### Install dependencies

    > pip install -r requirements.txt

###### Setup environment variables:

    - The environment are needed to setup the database and add the secret key
    ```
        DB_USER="" DB_PWD="" DB_HOST="" DB_NAME="" DB_PORT="" SECRET_KEY="" DEBUG=""
    ```

##### run migrations and update db:

    - python3 manage.py makemigrations

    - python3 manage.py migrate

###### Run application:

    On linux and windows:

    - python3 manage.py runserver

##### Run tests:

    - python3 manage.py test
