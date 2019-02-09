displacement_detector_api
=========================

Zeiss Hackathon Contestant

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

Setup
--------


1. Setup
    -> setup interpreter and virtualenv for the project

    Install the local dependencies + local dependencies in the venv
    -> pip install -e .[local]

    Migrate:
    -> manage.py migrate

2. Sync Silks Database tables:
    -> python manage.py syncdb

3. Execute the runserver_local run configuration
    -> You got your smooth server going.
    -> it includes travisCI, all tests included are called via manage.py test
    -> you got djangorestframework (endpoint users/ as a demo implemented with test)
    -> debug_toolbar available for local users
    -> postgres database connection included
    -> stub for generating yaml config files included


Next up:
    -> Defining editorconfig and gitconfig
    -> Introduction of MyPy
