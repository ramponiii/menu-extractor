import pytest

from menu_extractor.exceptions import (
    InvalidGPTMenuItemResponseError,
)
from menu_extractor.models import MenuItem, MenuItemList
from menu_extractor.parsing import (
    parse_dict_str_from_llm_response,
)

burger = MenuItemList(
    [
        MenuItem(
            name="Burger", description="Beef Quarter Pounder", price=10.50, type="food"
        )
    ]
)
burger_json_str = burger.model_dump_json(indent=4)


class TestResponseParsing:
    def test_llm_response_is_empty_list(self):
        output = parse_dict_str_from_llm_response("```json[]```")
        assert output == MenuItemList([])

    def test_llm_response_simple_case(self):
        output = parse_dict_str_from_llm_response(burger_json_str)
        assert output == burger

    def test_llm_response_no_json_marker_is_empty_list(self):
        output = parse_dict_str_from_llm_response("```[]```")
        assert output == MenuItemList([])

    def test_llm_response_no_backticks_is_empty_list(self):
        output = parse_dict_str_from_llm_response("[]")
        assert output == MenuItemList([])

    def test_no_json_in_llm_response_raises_invalid_menu_item_response_error(self):
        with pytest.raises(InvalidGPTMenuItemResponseError):
            parse_dict_str_from_llm_response("I couldn't find any menu items")

    # test if one item in list is invalid
    # test list has item with missing property
    # test list has item with extra property
    # test list has item as expected
    # test case json is cutoff
