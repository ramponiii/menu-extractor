from typing import Literal

from pydantic import BaseModel, RootModel


class MenuItem(BaseModel):
    name: str
    description: str
    price: float
    type: Literal["drink", "food", "missing"]


class MenuItemList(RootModel):  # type: ignore
    root: list[MenuItem]


class Menu(BaseModel):
    service_charge: int
    menu_description: str
    menu_items: MenuItemList
