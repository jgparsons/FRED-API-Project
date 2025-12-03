# FRED-API-Project

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
# pip install pytest
pip install -r requirements.txt
```

## Usage

```sh
python -m app.collect_FRED_data
```

### Web App

Run the web app (then view in the browser at http://localhost:5000/):

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
# find all the tests and run them:
pytest
```