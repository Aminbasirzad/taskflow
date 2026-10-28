# TaskFlow

A task management REST API built with Django and Django REST Framework.

## Overview

TaskFlow is a backend project designed to manage tasks and workspaces through a REST API.

## Tech Stack

* Python
* Django
* Django REST Framework
* Django Filter
* Simple JWT
* drf-spectacular
* PostgreSQL driver (psycopg)

## Getting Started

### 1. Clone the repository

bash
git clone https://github.com/Aminbasirzad/taskflow.git
cd taskflow


### 2. Create a virtual environment

bash
python -m venv venv


Activate it on Windows:

bash
venv\Scripts\activate


### 3. Install dependencies

bash
pip install -r requirements.txt


### 4. Apply database migrations

bash
python manage.py migrate


### 5. Run the development server

bash
python manage.py runserver


The development server will be available at:

http://127.0.0.1:8000/

## Running Tests

Run the automated tests with:

bash
python manage.py test


## Configuration

Review config/settings.py before running the project in another environment.

Do not commit secret keys, passwords, or other sensitive credentials to version control.

## Project Status

Under development.

## License

No license specified.
