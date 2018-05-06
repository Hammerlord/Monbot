from unittest import TestCase

from src.core.elements import Effectiveness, Elements


class ElementalEffectivenessTests(TestCase):

    def test_fire_vs_earth(self):
        error = "Fire is supposed to be effective against earth"
        fire_vs_earth = Effectiveness(Elements.FIRE, Elements.EARTH)
        fire_vs_earth.calculate()
        self.assertGreater(fire_vs_earth.effectiveness_multiplier, 1, error)

    def test_earth_vs_fire(self):
        error = "Fire is supposed to resist earth"
        earth_vs_fire = Effectiveness(Elements.EARTH, Elements.FIRE)
        earth_vs_fire.calculate()
        self.assertLess(earth_vs_fire.effectiveness_multiplier, 1, error)

    def test_lightning_vs_water(self):
        error = "Lightning is supposed to be effective against water"
        lightning_vs_water = Effectiveness(Elements.LIGHTNING, Elements.WATER)
        lightning_vs_water.calculate()
        self.assertGreater(lightning_vs_water.effectiveness_multiplier, 1, error)

    def test_water_vs_lightning(self):
        error = "Lightning is supposed to resist water"
        water_vs_lightning = Effectiveness(Elements.WATER, Elements.LIGHTNING)
        water_vs_lightning.calculate()
        self.assertLess(water_vs_lightning.effectiveness_multiplier, 1, error)

    def test_wind_vs_fire(self):
        error = "Wind is supposed to be effective against fire"
        wind_vs_fire = Effectiveness(Elements.WIND, Elements.FIRE)
        wind_vs_fire.calculate()
        self.assertGreater(wind_vs_fire.effectiveness_multiplier, 1, error)

    def test_fire_vs_wind(self):
        error = "Wind is supposed to resist fire"
        fire_vs_wind = Effectiveness(Elements.FIRE, Elements.WIND)
        fire_vs_wind.calculate()
        self.assertLess(fire_vs_wind.effectiveness_multiplier, 1, error)

    def test_light_vs_dark(self):
        error = "Light and dark are supposed to be effective against each other"
        light_vs_dark = Effectiveness(Elements.DARK, Elements.LIGHT)
        light_vs_dark.calculate()
        dark_vs_light = Effectiveness(Elements.LIGHT, Elements.DARK)
        dark_vs_light.calculate()
        self.assertGreater(light_vs_dark.effectiveness_multiplier, 1, error)
        self.assertGreater(dark_vs_light.effectiveness_multiplier, 1, error)

    def test_chaos(self):
        error = "Chaos is supposed to be effective against other elements and vice versa"
        for attr in vars(Elements):
            chaos_vs_other = Effectiveness(Elements.CHAOS, getattr(Elements, attr))
            chaos_vs_other.calculate()
            other_vs_chaos = Effectiveness(getattr(Elements, attr), Elements.CHAOS)
            other_vs_chaos.calculate()
            self.assertGreater(chaos_vs_other.effectiveness_multiplier, 1, error)
            self.assertGreater(other_vs_chaos.effectiveness_multiplier, 1, error)
