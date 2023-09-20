# Grantha LMS

![Logo](static/custom/images/grantha.png)

Library Management System built with [Django](https://www.djangoproject.com/ 'Django Website'). Uses
[Bootstrap](https://getbootstrap.com/ 'Bootstrap Website') and
[Font Awesome Icons](https://fontawesome.com/icons 'Font Awesome Website').

## Requirements

-   [Python](https://python.org/downloads/ 'Download Python') (with pip)

## Setup

First clone the repository. Then, to install dependencies, navigate to project root in the terminal and run:

```
pip install -r requirements.txt
```

Although not mandatory, a `.env` file can be created at project root to set various credentials.
An example is given below.

```.env
# Specify whether to use hosts that can serve the application
# besides localhost
ADDED_HOSTS=True

# HOSTS is necessary and used only when ADDED_HOSTS is set to True
# HOSTS=first.com, (format for single host)
HOSTS=first.com,second.com # (format for multiple hosts)

# Uses PostgreSQL if True, otherwise uses SQLite
USE_POSTGRES=False

# Database credentials are necessary and used only when
# USE_POSTGRES is set to True
DB_NAME=dbname
DB_USERNAME=admin
DB_PASSWORD=super_secure_password
DB_HOST=db_host
DB_PORT=5432
```

Create database migrations and perform migration:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

# Running the development server

After successful completion of setup steps above, the development server can be run with:

```
python manage.py runserver 0:8000
```

If above command does not produce errors,
[localhost:8000](http://localhost:8000/ 'localhost port 8000') can be visited to view the running application.
