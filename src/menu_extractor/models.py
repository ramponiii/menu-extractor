import json

from pydantic import BaseModel


class JsonSchemaBaseModel(BaseModel):
    """
    Custom BaseModel that adds a method to get the schema as a formatted JSON string.
    """

    @classmethod
    def formatted_schema(cls) -> str:
        return json.dumps(cls.model_json_schema(), indent=4)


class MenuItem(JsonSchemaBaseModel):
    """
    Represents a menu item.

    Attributes:
        name (str): The name of the menu item.
        description (str | None): A brief description of the menu item.
        price (float | None): The price of the menu item.
        tags (list[str] | None): List of special tags such as "Vegan", "Vegeterian", etc.
        calories (int | None): The calorie count of the menu item.
        extras (list[MenuItem] | None): A list of extras for the menu item
    """

    name: str
    description: str | None = None
    price: float | None = None
    tags: list[str] | None = None
    calories: int | None = None
    extras: list["MenuItem"] | None = None


class Menu(JsonSchemaBaseModel):
    """
    Represents a menu with a service charge and a description.

    Attributes:
        service_charge (float): The service charge applied to the menu.
        menu_description (str): A description of the menu.
        menu_items (list[MenuItem]): A list of menu items included in the menu.
    """

    service_charge: float
    menu_description: str
    menu_items: list[MenuItem]
