# Langflow playground
This playground is used for sharing and testing components. Additionally, it is used to provide a local environment for the Langflow application.

## Running locally with Python
Python 3.10 or newer is required.
- Download and install Astral uv, instructions [here](https://docs.astral.sh/uv/getting-started/installation/)
- Create a virtual environment and install the dependencies
```bash
uv sync
```
- Create a `.env` file and add the environment variables, see `.env.example` for reference
- Run the Langflow application
```bash
uv run langflow run --env-file .env
```

## Running locally with Docker
The docker compose file will start a Langflow instance and a Postgres database for storing the data.
```bash
docker compose up
```

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