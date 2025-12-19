# FRED-API-Project

## Website

Can be found online at: https://fred-api-project.onrender.com/

## Setup

### Obtain Environment Variables

To run this program locally, users will need certain environment variables to put into their .env file:

a FRED API key, which users can obtain at https://fred.stlouisfed.org/docs/api/api_key.html

This key should be set as FRED_API_KEY in the .env file

a Mailgun API key, Mailgun domain, Mailgun sender address, and Mailgun mailing list, which users can set up at https://app.mailgun.com/

These environment variables should be named MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_SENDER_ADDRESS, and MAILING_LIST, respectively, in the .env file

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
