import unittest

from src.elemental.ability.ability import Ability
from src.elemental.ability.defend import Defend
from src.elemental.attribute.attribute_factory import AttributeFactory
from src.elemental.attribute.attribute_manager import AttributeManager
from tests.character.character_builder import PlayerBuilder
from tests.elemental.elemental_builder import ElementalBuilder, SpeciesBuilder
from tests.elemental.species_builder import StatsBuilder


class ElementalTests(unittest.TestCase):
    def setUp(self):
        self.elemental = ElementalBuilder().with_level(1).build()

    def tearDown(self):
        self.elemental = None

    def get_growth_rate(self) -> 'GrowthRate':
        return StatsBuilder() \
            .with_physical_att(1) \
            .with_magic_att(1) \
            .with_physical_def(1) \
            .with_magic_def(1) \
            .with_speed(2) \
            .with_max_hp(3) \
            .build()

    def get_species(self) -> 'Species':
        return SpeciesBuilder() \
            .with_physical_att(15) \
            .with_magic_att(15) \
            .with_physical_def(15) \
            .with_magic_def(10) \
            .with_speed(5) \
            .with_max_hp(50) \
            .with_growth_rate(self.get_growth_rate()) \
            .build()

    def get_preset_manager(self) -> AttributeManager:
        manager = AttributeFactory.create_empty_manager()
        AttributeFactory.add_ferocity(manager)
        AttributeFactory.add_attunement(manager)
        AttributeFactory.add_resolve(manager)
        return manager

    def test_gain_exp(self):
        error = "Elemental couldn't acquire experience"
        self.elemental.add_exp(10)
        exp_gained = self.elemental.current_exp
        self.assertEqual(exp_gained, 10, error)

    def test_level_up(self):
        error = "Elemental couldn't level"
        before_level = self.elemental.level
        self.elemental.add_exp(self.elemental.exp_to_level)
        after_level = self.elemental.level
        self.assertGreater(after_level, before_level, error)

    def test_level_exp_cap(self):
        error = "Leveling up didn't increase the Elemental's required exp"
        lower_requirement = self.elemental.exp_to_level
        higher_level_elemental = ElementalBuilder().with_level(2).build()
        higher_requirement = higher_level_elemental.exp_to_level
        self.assertGreater(higher_requirement, lower_requirement, error)

    def test_multi_level_up(self):
        error = "Elemental failed to level up multiple times with multiple levels' worth of experience"
        exp_gained = self.elemental.exp_to_level * 5  # Arbitrary large amount of exp
        before_level = self.elemental.level
        self.elemental.add_exp(exp_gained)
        after_level = self.elemental.level
        self.assertGreater(after_level, before_level + 1, error)

    def test_default_nickname(self):
        error = "Nickname must be the Species name by default"
        species = SpeciesBuilder().with_name("Richard").build()
        elemental = ElementalBuilder().with_species(species).build()
        self.assertEqual(elemental.nickname, "Richard", error)

    def test_set_nickname(self):
        error = "Elemental nickname couldn't be set"
        name = "Monze"
        self.elemental.nickname = name
        self.assertEqual(self.elemental.nickname, name, error)

    def test_nickname_max_length(self):
        error = "Elemental nickname can incorrectly be set to more than 15 characters"
        self.elemental.nickname = "dsadadaifjasifjasfdsd"
        name_length = len(self.elemental.nickname)
        self.assertLessEqual(name_length, 15, error)

    def test_reset_nickname(self):
        error = "Elemental nickname couldn't be reset"
        species = SpeciesBuilder().with_name("Richard").build()
        elemental = ElementalBuilder().with_species(species).build()
        elemental.nickname = "Logi"
        elemental.reset_nickname()
        self.assertEqual(elemental.nickname, "Richard", error)

    def test_set_note(self):
        error = "Elemental note couldn't be set"
        note = "+PDEF +PATT +SPEED bruiser"
        self.elemental.note = note
        self.assertEqual(self.elemental.note, note, error)

    def test_note_max_length(self):
        error = "Elemental note can incorrectly be set to more than 75 characters"
        self.elemental.note = error
        name_length = len(self.elemental.note)
        self.assertLessEqual(name_length, 75, error)

    def test_gain_stats(self):
        error = "Elemental stat increase level doesn't match its Species' growth rate"
        elemental = ElementalBuilder().with_level(2).with_species(self.get_species()).build()
        self.assertEqual(elemental.physical_att, 16, error)  # See get_species()
        self.assertEqual(elemental.magic_att, 16, error)
        self.assertEqual(elemental.physical_def, 16, error)
        self.assertEqual(elemental.magic_def, 11, error)
        self.assertEqual(elemental.speed, 7, error)
        self.assertEqual(elemental.max_hp, 53, error)

    def test_species_static(self):
        error = "Species' stats should not change when Elemental levels!"
        species = self.get_species()
        elemental = ElementalBuilder().with_level(1).with_species(species).build()
        exp = elemental.exp_to_level
        self.elemental.add_exp(exp)
        self.assertEqual(species._physical_att, 15, error)
        self.assertEqual(species._magic_att, 15, error)
        self.assertEqual(species._physical_def, 15, error)
        self.assertEqual(species._magic_def, 10, error)
        self.assertEqual(species._speed, 5, error)
        self.assertEqual(species._max_hp, 50, error)

    def test_has_ability(self):
        error = "Elemental didn't get Abilities on instantiation"
        self.assertIsInstance(self.elemental.active_abilities[0], Ability, error)

    def test_owner_restricts_level(self):
        error = "Elemental shouldn't be able to level past its owner"
        player = PlayerBuilder().with_level(15).build()
        elemental = ElementalBuilder().with_level(14).with_owner(player).build()
        exp = elemental.exp_to_level * 15  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        self.assertEqual(player.level, elemental.level, error)

    def test_rank_restricts_level(self):
        error = "Elemental must have be rank 2 to grow past level 10"
        elemental = ElementalBuilder().with_level(10).build()
        exp = elemental.exp_to_level * 5  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        self.assertEqual(elemental.level, 10, error)

    def test_exp_gain_rank_restriction(self):
        error = "Elemental should be allowed to overflow experience even when it is under-ranked"
        elemental = ElementalBuilder().with_level(10).with_rank(1).build()
        exp = elemental.exp_to_level * 5  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        self.assertEqual(elemental.current_exp, exp, error)

    def test_exp_overflow_level(self):
        error = "Elemental failed to resolve overflow exp after it ranked up"
        elemental = ElementalBuilder().with_level(10).with_rank(1).build()
        exp = elemental.exp_to_level * 5  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        self.assertGreater(elemental.level, 10, error)

    def test_num_attributes(self):
        error = "Elemental must have three attributes"
        elemental = ElementalBuilder().build()
        num_attributes = len(elemental.attributes)
        self.assertEqual(num_attributes, 3, error)

    def test_create_unique_attributes(self):
        error = "Elemental can incorrectly have a duplicate attribute"
        for i in range(100):
            elemental = ElementalBuilder().build()
            attributes = elemental.attributes
            no_duplicates = len(attributes) == len(set(attributes))
            self.assertIs(no_duplicates, True, error)

    def test_raise_attribute(self):
        error = "Elemental who met requirements couldn't raise an attribute"
        elemental = ElementalBuilder().with_level(10).build()
        elemental.raise_attribute(0)
        attributes = elemental.attributes
        attribute_level = attributes[0].level
        self.assertEqual(attribute_level, 1, error)

    def test_attribute_gives_stats(self):
        error = "No stats gained from raising an attribute"
        manager = self.get_preset_manager()  # Physical attack Attribute is guaranteed in the first slot
        elemental = ElementalBuilder().with_attribute_manager(manager).with_level(10).build()
        p_att_before = elemental.physical_att
        elemental.raise_attribute(0)
        p_att_after = elemental.physical_att
        self.assertGreater(p_att_after, p_att_before, error)

    def test_initial_abilities(self):
        error = "Elemental didn't learn abilities on creation"
        num_abilities = len(self.elemental.active_abilities)
        self.assertGreater(num_abilities, 0, error)

    def test_learn_abilities_by_level(self):
        error = "Elemental couldn't learn an ability by leveling"
        initial_num_abilities = len(self.elemental.active_abilities)
        exp = self.elemental.exp_to_level * 500  # Arbitrary large amount of exp to reach level 10
        self.elemental.add_exp(exp)
        leveled_num_abilities = len(self.elemental.active_abilities)
        self.assertGreater(leveled_num_abilities, initial_num_abilities, error)

    def test_learn_defend(self):
        error = "Elemental must learn Defend as a basic ability"
        has_defend = False
        for ability in self.elemental.active_abilities:
            if ability.id == Defend().id:
                has_defend = True
        self.assertIs(has_defend, True, error)

    def test_num_active_abilities(self):
        error = "Elemental can incorrectly have more than 5 abilities active"
        # TODO

    def test_swap_defend(self):
        error = "Elemental can incorrectly swap out Defend for another ability"
        # TODO

