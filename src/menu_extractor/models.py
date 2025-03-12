from typing import Literal

from pydantic import BaseModel, RootModel


class MenuItem(BaseModel):
    """
    Represents a menu item.

    Attributes:
        name (str): The name of the menu item.
        description (str): A brief description of the menu item.
        price (float): The price of the menu item.
        type (Literal["drink", "snack", ...]): The category of the menu item,
    """

    name: str
    description: str
    price: float
    type: Literal[
        "drink",
        "snack",
        "dessert",
        "sharer",
        "small plate",
        "main",
        "side",
        "other",
    ]


class MenuItemList(RootModel):  # type: ignore
    root: list[MenuItem]


class Menu(BaseModel):
    service_charge: float
    menu_description: str
    menu_items: MenuItemList
