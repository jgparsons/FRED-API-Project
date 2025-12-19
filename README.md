# FRED-API-Project

## Website

Can be found online at: https://fred-api-project.onrender.com/

## Setup

### Obtain Environment Variables

To run this program locally, users will need certain environment variables to put into their .env file:

a FRED API key, which users can obtain at https://fred.stlouisfed.org/docs/api/api_key.html

This key should be set as FRED_API_KEY in the .env file



a Mailgun domain, which can be created or selected from a current domain at https://app.mailgun.com/mg/sending/domains

a Mailgun API key, which can be create or found in the domain settings for any Mailgun domain you choose to create or use at https://app.mailgun.com/mg/sending/domains

a Mailgun sender address, which can be found in the SMTP credentials tab of the domain settings for a given domain at https://app.mailgun.com/mg/sending/domains

a Mailgun mailing list, which users can create or select from at https://app.mailgun.com/mg/sending/mailing-lists

These environment variables should be named MAILGUN_DOMAIN, MAILGUN_API_KEY, MAILGUN_SENDER_ADDRESS, and MAILING_LIST, respectively, in the .env file

Users must also add the line "FLASK_APP=web_app" to their .env file

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
