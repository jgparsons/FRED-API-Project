# FRED-API-Project

## Website

Can be found online at: https://fred-api-project.onrender.com/

## Setup

### Virtual Environment

Create and activate a virtual environment:

```sh
conda create -n FRED-env python=3.11
conda activate FRED-env
```

### Packages

Install packages:

```sh
pip install -r requirements.txt
```

### Run Web App Locally

```sh
# Mac OS:
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```

## Tests

Run the tests:
```sh
pytest
```