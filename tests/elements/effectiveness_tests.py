from unittest import TestCase

from src.core.elements import Effectiveness, Elements
from tests.elemental.elemental_builder import ElementalBuilder


class ElementalEffectivenessTests(TestCase):

    def test_fire_vs_earth(self):
        error = "Fire is supposed to be effective against earth"
        fire_vs_earth = Effectiveness(Elements.FIRE, Elements.EARTH)
        multipler = fire_vs_earth.calculate_multiplier()
        self.assertGreater(multipler, 1, error)

    def test_earth_vs_fire(self):
        error = "Fire is supposed to resist earth"
        earth_vs_fire = Effectiveness(Elements.EARTH, Elements.FIRE)
        multiplier = earth_vs_fire.calculate_multiplier()
        self.assertLess(multiplier, 1, error)

    def test_lightning_vs_water(self):
        error = "Lightning is supposed to be effective against water"
        lightning_vs_water = Effectiveness(Elements.LIGHTNING, Elements.WATER)
        multiplier = lightning_vs_water.calculate_multiplier()
        self.assertGreater(multiplier, 1, error)

    def test_water_vs_lightning(self):
        error = "Lightning is supposed to resist water"
        water_vs_lightning = Effectiveness(Elements.WATER, Elements.LIGHTNING)
        multiplier = water_vs_lightning.calculate_multiplier()
        self.assertLess(multiplier, 1, error)

    def test_wind_vs_fire(self):
        error = "Wind is supposed to be effective against fire"
        wind_vs_fire = Effectiveness(Elements.WIND, Elements.FIRE)
        multiplier = wind_vs_fire.calculate_multiplier()
        self.assertGreater(multiplier, 1, error)

    def test_fire_vs_wind(self):
        error = "Wind is supposed to resist fire"
        fire_vs_wind = Effectiveness(Elements.FIRE, Elements.WIND)
        multiplier = fire_vs_wind.calculate_multiplier()
        self.assertLess(multiplier, 1, error)

    def test_light_vs_dark(self):
        error = "Light and dark are supposed to be effective against each other"
        light_vs_dark = Effectiveness(Elements.DARK, Elements.LIGHT)
        light_vs_dark_multiplier = light_vs_dark.calculate_multiplier()
        dark_vs_light = Effectiveness(Elements.LIGHT, Elements.DARK)
        dark_vs_light_multiplier = dark_vs_light.calculate_multiplier()
        self.assertGreater(light_vs_dark_multiplier, 1, error)
        self.assertGreater(dark_vs_light_multiplier, 1, error)

    def test_chaos_effective(self):
        error = "Chaos is supposed to be effective against other elements"
        expected = True
        for attr in vars(Elements):
            chaos_vs_other = Effectiveness(Elements.CHAOS, getattr(Elements, attr))
            multiplier = chaos_vs_other.calculate_multiplier()
            expected = multiplier > 1
            if not expected:
                break
        self.assertTrue(expected, error)

    def test_others_vs_chaos_effective(self):
        error = "Other elements are supposed to be effective against chaos"
        expected = True
        for attr in vars(Elements):
            other_vs_chaos = Effectiveness(getattr(Elements, attr), Elements.CHAOS)
            multiplier = other_vs_chaos.calculate_multiplier()
            expected = multiplier > 1
            if not expected:
                break
        self.assertTrue(expected, error)

    def test_find_effective(self):
        error = "Should have found an effective elemental given a list"
        elementals = [
            ElementalBuilder().with_element(Elements.WATER).build(),
            ElementalBuilder().with_element(Elements.EARTH).build(),
            ElementalBuilder().with_element(Elements.WATER).build()
        ]
        result = Effectiveness.find_effective(elementals, Elements.FIRE)
        self.assertEqual(len(result), 2, error)

    def test_find_neutral(self):
        error = "Should have found a neutral elemental given a list"
        elementals = [
            ElementalBuilder().with_element(Elements.LIGHT).build(),
            ElementalBuilder().with_element(Elements.EARTH).build(),
            ElementalBuilder().with_element(Elements.WIND).build()
        ]
        result = Effectiveness.find_effective(elementals, Elements.FIRE)
        self.assertEqual(len(result), 1, error)
