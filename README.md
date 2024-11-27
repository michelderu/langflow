# Langflow playground
This playground is used for sharing and testing components. Additionally, it is used to provide a local environment for the Langflow application.

## Custom components
The `components` folder contains custom components that can be used in the Langflow application.

Currently the following components are available:

### URL List
Provide a list of URLs to be processed by the URL component. Just provide a newline separated list of URLs.

### Rest Endpoint
Interact with a REST endpoint with support for:
- `GET`, `POST`, `PUT` and `DELETE`
- Basic and digest authentication
- Headers
- Payload (form, json)

## Running locally with Python
Python 3.10 or newer is required.

```bash
source .venv/bin/activate
python -m pip install langflow -U
python -m langflow run
```

## Running locally with Docker
The docker compose file will start a Langflow instance and a Postgres database for storing the data.
```bash
docker compose up
```