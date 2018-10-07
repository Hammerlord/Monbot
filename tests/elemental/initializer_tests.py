import unittest

from src.core.elements import Elements
from src.elemental.elemental_factory import ElementalInitializer
from src.elemental.species.mithus import Mithus
from src.elemental.species.nepharus import Nepharus


class ElementalInitializerTests(unittest.TestCase):

    def test_make_random_exclude(self):
        error = "ElementalInitializer didn't correctly exclude specified elementals"
        correctly_excluded = True
        exclusions = [ElementalInitializer.make(Mithus()),
                      ElementalInitializer.make(Nepharus())]
        names = [elemental.name for elemental in exclusions]
        for i in range(100):
            elemental = ElementalInitializer.make_random(excluding=exclusions)
            if elemental.name in names:
                correctly_excluded = False
                break
        self.assertTrue(correctly_excluded, error)

    def test_make_random_element(self):
        error = "ElementalInitializer didn't return an elemental of a specified element"
        correct_element = True
        chosen_element = Elements.WATER
        for i in range(100):
            elemental = ElementalInitializer.make_random(element=chosen_element)
            if elemental.element != chosen_element:
                correct_element = False
                break
        self.assertTrue(correct_element, error)