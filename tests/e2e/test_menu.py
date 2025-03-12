import asyncio
import unittest
from pathlib import Path

from rapidfuzz import fuzz

from menu_extractor.main import main
from menu_extractor.models import Menu, MenuItem
from tests.data import GARDEN_GATE_EXPECTATION, GARDEN_GATE_PDF

DESCRIPTION_SIMILARTIY_THRESHOLD = 85


class MenuTestFramework:
    """
    Reusable test framework for validating menu extraction with structured test cases.
    """

    def __init__(self, pdf_path: Path, expected_menu: Menu):
        self.menu: Menu = asyncio.run(main(pdf_path=pdf_path))
        self.expected_menu = expected_menu

    def test_structure(self, test_case: unittest.TestCase):
        """Ensure the extracted menu contains expected top-level attributes."""
        test_case.assertIsInstance(
            self.menu.service_charge, float, "service_charge should be a float"
        )
        test_case.assertIsInstance(
            self.menu.menu_description, str, "menu_description should be a string"
        )
        test_case.assertIsInstance(
            self.menu.menu_items.root, list, "menu_items should be a list"
        )

    def test_menu_item(
        self, test_case: unittest.TestCase, name: str, expected_item: MenuItem
    ):
        """Test an individual menu item."""
        extracted_items = {item.name: item for item in self.menu.menu_items.root}
        test_case.assertIn(name, extracted_items, f"Expected item '{name}' not found")

        extracted_item = extracted_items[name]
        test_case.assertIsInstance(
            extracted_item, MenuItem, "Each menu item should be an instance of MenuItem"
        )
        test_case.assertGreaterEqual(
            fuzz.ratio(extracted_item.description, expected_item.description),
            DESCRIPTION_SIMILARTIY_THRESHOLD,
            f"Mismatch in description for {name} (similarity too low). Got description '{extracted_item.description}' but expected '{expected_item.description}'",
        )
        test_case.assertEqual(
            extracted_item.price, expected_item.price, f"Mismatch in price for {name}"
        )
        test_case.assertEqual(
            extracted_item.type, expected_item.type, f"Mismatch in category for {name}"
        )


class TestGardenGateMenu(unittest.TestCase):
    """Test case for the Garden Gate menu extraction."""

    @classmethod
    def setUpClass(cls):
        cls.tester = MenuTestFramework(
            pdf_path=GARDEN_GATE_PDF, expected_menu=GARDEN_GATE_EXPECTATION
        )

    def test_structure(self):
        self.tester.test_structure(self)

    def test_menu_items(self):
        for menu_item in GARDEN_GATE_EXPECTATION.menu_items.root:
            with self.subTest(name=menu_item.name):
                self.tester.test_menu_item(self, menu_item.name, menu_item)


if __name__ == "__main__":
    unittest.main()
