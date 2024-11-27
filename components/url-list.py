# from langflow.field_typing import Data
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message


class CustomComponent(Component):
    display_name = "URL list"
    description = "Provide a list of URL to be processed."
    icon = "code"
    name = "CustomComponent"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="URLs",
            info="URL list (newline separated)",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> list[Message]:
        urls = self.input_value.split("\n")
        data = []
        for url in urls:
            data.append(Message(text=url))
        self.status = data
        return data