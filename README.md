# Minimum Entropy
**A question/answer web application to create a data science knowledge base.**

[![Build Status][travis_img]][travis_href]
[![Coverage Status][coveralls_img]][coveralls_href]
[![Stories in Ready][waffle_img]][waffle_href]

[![Answers 1km](docs/images/answers.jpg)][answers.jpg]

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

## About

Minimum Entropy is a fork of [Kyudo](https://github.com/mclumd/kyudo), a knowledge goal casebase management and annotation tool. Kyudo was designed to create a corpus with which to explore case-based reasoning and automatic knowledge goal solutions in an artificial intelligence setting and was set up similarly to a Q&A application like [StackExchange](http://stackexchange.com/) or [Quora](https://www.quora.com/).

### Contributing

Minimum Entropy is open source, and we would love your help to develop the site, particularly if you are a Django or Front-End developer! You can contribute in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/DistrictDataLabs/minimum-entropy/issues](https://github.com/DistrictDataLabs/minimum-entropy/issues)
2. Work on a card on the dev board: [https://waffle.io/DistrictDataLabs/minimum-entropy](https://waffle.io/DistrictDataLabs/minimum-entropy)
3. Create a pull request in Github: [https://github.com/DistrictDataLabs/minimum-entropy/pulls](https://github.com/DistrictDataLabs/minimum-entropy/pulls)

The repository is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. Please make sure that all pull requests go into the _develop_ branch; pulls to master will not be considered. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/DistrictDataLabs/minimum-entropy) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

### Name Origin

[Maximum Entropy](https://en.wikipedia.org/wiki/Multinomial_logistic_regression) is a classification method that is used to predict the probabilities of different possible outcomes of a categorically distributed dependent variable. It uses a principle such that the probability which best represents the current state of knowledge is the one with the largest [entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)). Entropy refers to uncertainty, and in a question and answer site, uncertainty is bad. Therefore we've named the site minimum entropy to reflect the fact that we are trying to minimize uncertainty in order to best represent the current state of knowledge.

### Attribution

The image used in this README, [Answers][answers.jpg] by [Francisco Martins](https://www.flickr.com/photos/betta_design/) is licensed under [CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/)


## Changelog

The release versions that are sent to the Python package index (PyPI) are also tagged in Github. You can see the tags through the Github web application and download the tarball of the version you'd like. Additionally PyPI will host the various releases of Minimum Entropy (eventually).

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bug fixes or other micro changes that developers should feel free to immediately update to.


### Version 1.0 Beta 1

* **tag**: [v1.0b1](https://github.com/DistrictDataLabs/minimum-entropy/releases/tag/v1.0b1)
* **deployment**: Tuesday, July 5, 2016
* **commit**: [see tag](#)

This beta release for Version 1.0 simply moves the code over from Kyudo and modifies it to remove the research components and only present a question and answer system. Things are not perfect since the app was designed for a different research project. However, the core functionality - asking questions and answering them with Markdown, as well as up and down voting exists. This is a good start to beta to our faculty to see what they think!

<!-- References -->
[travis_img]: https://travis-ci.org/DistrictDataLabs/minimum-entropy.svg
[travis_href]: https://travis-ci.org/DistrictDataLabs/minimum-entropy
[waffle_img]: https://badge.waffle.io/DistrictDataLabs/minimum-entropy.png?label=ready&title=Ready
[waffle_href]: https://waffle.io/DistrictDataLabs/minimum-entropy
[coveralls_img]: https://coveralls.io/repos/github/DistrictDataLabs/minimum-entropy/badge.svg?branch=master
[coveralls_href]:https://coveralls.io/github/DistrictDataLabs/minimum-entropy?branch=master
[answers.jpg]: https://flic.kr/p/82Ub7z
