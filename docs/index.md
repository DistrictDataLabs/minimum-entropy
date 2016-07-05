# Welcome to Minimum Entropy

This describes the development environment for Minimum Entropy.

## How to Run

In order to run the server locally, follow these steps:

1. Clone the repository into a working directory of your choice

2. Install the dependencies using pip install -r requirements.txt

    Note, it may be helpful to use a virtualenv - and you really should.

3. Set the following environment vars (or use a .env file, see below):

        $ export DJANGO_SETTINGS_MODULE=minent.settings.development
        $ export SECRET_KEY="super secret key"
        $ export GOOGLE_OAUTH2_KEY="googlekey"
        $ export GOOGLE_OAUTH2_SECRET="googlesecret"

    Note that this app is enabled with Google OAuth login, you'll need to
    create your own Google credentials with the Google Developers console.

4. Create a database on postgres (on the localhost) called minent

    Note, you can set the envvars DB_NAME, DB_USER, DB_PASS etc.

5. Run the database migration:

        $ python manage.py migrate

6. Run the server:

        $ make runserver

7. You should now be able to open a browser at http://127.0.0.1:8000/

### Environment Variables

Although many settings for different deployment environments can be tracked with the codebase in the correct settings file, some variables like passwords and secret keys should be stored in operating system environment for security reasons. I've installed `django-dotenv` so to manage your development environment, place inside a `.env` file in the root of the repository with the following required keys:

    DJANGO_SETTINGS_MODULE=minent.settings.development
    SECRET_KEY=asupersecretpassword
    GOOGLE_OAUTH2_CLIENT_ID=ourgoogleclientid
    GOOGLE_OAUTH2_CLIENT_SECRET=ourgoogleclientsecret  

Optional environment variables that should be set in the environment in production are as follows (along with their current defaults):

    # Specify database information
    DB_NAME=minent
    DB_USER=django
    DB_PASS=
    DB_HOST=localhost
    DB_PORT=5432

    # Specify email logging information (gmail credentials)
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=
