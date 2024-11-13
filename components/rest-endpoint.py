# from langflow.field_typing import Data
from langflow.custom import Component
from langflow.io import MessageTextInput, Output, DropdownInput, MultilineInput, SecretStrInput
from langflow.schema import Data
import requests, json, re
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from loguru import logger

class CustomComponent(Component):
    display_name = "REST Endpoint"
    description = "Interact with a REST endpoint."
    documentation: str = "http://docs.langflow.org/components/custom"
    icon = "custom_components"
    name = "RESTEndpoint"

    inputs = [
        MessageTextInput(name="endpoint", display_name="Endpoint", required=True, placeholder="https://api.restful-api.dev/objects", info="The URL of the REST endpoint"),
        DropdownInput(name="authentication", display_name="Authentication type", required=True, options=['None / other', 'Basic', 'Digest'], placeholder='None / other', value='None/other', info="Authentication type, please also provide username and password"),
        MessageTextInput(name="username", display_name="Username", info="Username for Basic or Digest Authentication"),
        SecretStrInput(name="password", display_name="Password", info="Password for Basic or Digest Authentication"),
        DropdownInput(name="method", display_name="Method", required=True, options=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'], placeholder='GET', info="Method for calling the REST endpoint"),
        MessageTextInput(name="query", display_name="Query string", placeholder="id=4&id=6", info="Query string, if any"),
        MultilineInput(name="headers", display_name="Headers", placeholder='Content-Type: application/json', value='Content-Type: application/json', info="Type your headers as follows:\nContent-Type: application/json", is_list=True),
        MultilineInput(name="payload", display_name="Payload", placeholder='{}', value='{}', info="Payload in JSON format"),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def ensure_url(self, string: str) -> str:
        """
        Ensures the given string is a URL by adding 'http://' if it doesn't start with 'http://' or 'https://'.
        Raises an error if the string is not a valid URL.

        Parameters:
            string (str): The string to be checked and possibly modified.

        Returns:
            str: The modified string that is ensured to be a URL.

        Raises:
            ValueError: If the string is not a valid URL.
        """
        if not string.startswith(("http://", "https://")):
            string = "http://" + string

        # Basic URL validation regex
        url_regex = re.compile(
            r"^(https?:\/\/)?"  # optional protocol
            r"(www\.)?"  # optional www
            r"([a-zA-Z0-9.-]+)"  # domain
            r"(\.[a-zA-Z]{2,})?"  # top-level domain
            r"(:\d+)?"  # optional port
            r"(\/[^\s]*)?$",  # optional path
            re.IGNORECASE,
        )

        if not url_regex.match(string):
            msg = f"Invalid URL: {string}"
            raise ValueError(msg)

        return string
        
    def construct_headers(self, headers: list) -> dict:
        # Check no headers
        if len(headers) == 0 or all(header.strip() == "" for header in headers):
            return {}
        headers = [header.strip() for header in headers]
        # List should contain semicolons
        if len(headers) == 0 or all(":" not in header for header in headers):
            raise ValueError(f"Invalid header string(s), the should be of the form: 'Content-Type: application/json' for instance")
        # Construct a dict with headers to be used by requests
        headers = {header.split(":")[0].strip(): header.split(":")[1].strip() for header in headers}
        return headers
        
    def build_output(self) -> str:
        endpoint = self.ensure_url(self.endpoint.strip())
        method = self.method
        query = str(self.query.strip() if self.query else '')
        if query and query != '':
            endpoint += '?' + query
        logger.debug(f"{self.name}: Calling: {endpoint} with method {method}")
        
        authentication = self.authentication
        username = str(self.username.strip() if self.username else '')
        password = str(self.password.strip() if self.password else '')
        if (authentication in ["Basic", "Digest"] and not all([username, password])):
            raise ValueError("Authentication defined as Basic or Digest but no username and/or password supplied")
        logger.debug(f"{self.name}: Authentication: {authentication}, {username}/{password}")

        headers = self.construct_headers(self.headers)
        logger.debug(f"{self.name}: Headers: {headers}")
        
        try:
            payload = json.loads(self.payload) if self.payload else {}
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON payload: {self.payload}")
        logger.debug(f"{self.name}: Payload: {payload}")
            
        auth = None
        if (self.authentication == 'Basic' and username and password):
            auth = HTTPBasicAuth(username, password)
        if (self.authentication == 'Digest' and username and password):
            auth = HTTPDigestAuth(username, password)

        response = requests.request(self.method.lower(), endpoint, headers=headers, auth=auth, json=payload)
        return json.dumps(response.json())