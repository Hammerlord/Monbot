import unittest

from src.elemental.ability.abilities.claw import Claw
from src.elemental.ability.abilities.defend import Defend
from src.elemental.ability.abilities.fireball import Fireball
from src.elemental.ability.abilities.rend import Rend
from src.elemental.ability.abilities.rolling_thunder import RollingThunder
from src.elemental.ability.abilities.slam import Slam
from src.elemental.ability.ability import Ability, LearnableAbility
from src.elemental.attribute.attribute_factory import AttributeFactory
from src.elemental.attribute.attribute_manager import AttributeManager
from tests.character.character_builder import PlayerBuilder
from tests.elemental.elemental_builder import ElementalBuilder
from tests.elemental.species_builder import StatsBuilder, SpeciesBuilder


class ElementalTests(unittest.TestCase):
    def get_growth_rate(self) -> 'GrowthRate':
        return StatsBuilder() \
            .with_physical_att(1) \
            .with_magic_att(1) \
            .with_physical_def(1) \
            .with_magic_def(1) \
            .with_speed(2) \
            .with_max_hp(3) \
            .build()

    def get_learnable_ability(self, level: int) -> LearnableAbility:
        """
        Returns a test LearnableAbility for checking requirements.
        """
        learnable = LearnableAbility(Claw())
        learnable.level_required = level
        return learnable

    def get_species(self) -> 'Species':
        return SpeciesBuilder() \
            .with_physical_att(15) \
            .with_magic_att(15) \
            .with_physical_def(15) \
            .with_magic_def(10) \
            .with_speed(5) \
            .with_max_hp(50) \
            .with_growth_rate(self.get_growth_rate()) \
            .with_abilities([self.get_learnable_ability(level=1),
                             self.get_learnable_ability(level=2),
                             self.get_learnable_ability(level=3),
                             self.get_learnable_ability(level=4),
                             self.get_learnable_ability(level=5)
                             ]) \
            .build()

    def get_preset_manager(self) -> AttributeManager:
        manager = AttributeFactory.create_empty_manager()
        AttributeFactory.add_ferocity(manager)
        AttributeFactory.add_attunement(manager)
        AttributeFactory.add_resolve(manager)
        return manager

    def level_up(self, elemental) -> None:
        """
        Levels up an Elemental by granting it an amount of exp = exp_to_level
        :param elemental: Elemental
        """
        elemental.add_exp(elemental.exp_to_level)

    def test_gain_exp(self):
        error = "Elemental couldn't acquire experience"
        elemental = ElementalBuilder().with_level(1).build()
        elemental.add_exp(10)
        exp_gained = elemental.current_exp
        self.assertEqual(exp_gained, 10, error)

    def test_level_up(self):
        error = "Elemental couldn't level"
        elemental = ElementalBuilder().with_level(1).build()
        before_level = elemental.level
        self.level_up(elemental)
        after_level = elemental.level
        self.assertGreater(after_level, before_level, error)

    def test_level_exp_cap(self):
        error = "Leveling up didn't increase the Elemental's required exp"
        elemental = ElementalBuilder().with_level(1).build()
        lower_requirement = elemental.exp_to_level
        self.level_up(elemental)
        higher_requirement = elemental.exp_to_level
        self.assertGreater(higher_requirement, lower_requirement, error)

    def test_multi_level_up(self):
        error = "Elemental failed to level up multiple times with multiple levels' worth of experience"
        elemental = ElementalBuilder().with_level(1).build()
        before_level = elemental.level
        exp_gained = elemental.exp_to_level * 5  # Arbitrary large amount of exp
        elemental.add_exp(exp_gained)
        after_level = elemental.level
        self.assertGreater(after_level, before_level + 1, error)

    def test_default_nickname(self):
        error = "Nickname must be the Species name by default"
        species = SpeciesBuilder().with_name("Richard").build()
        elemental = ElementalBuilder().with_species(species).build()
        self.assertEqual(elemental.nickname, "Richard", error)

    def test_set_nickname(self):
        error = "Elemental nickname couldn't be set"
        name = "Monze"
        elemental = ElementalBuilder().build()
        elemental.nickname = name
        self.assertEqual(elemental.nickname, name, error)

    def test_nickname_max_length(self):
        error = "Elemental nickname can incorrectly be set to more than 15 characters"
        elemental = ElementalBuilder().build()
        elemental.nickname = "dsadadaifjasifjasfdsd"
        name_length = len(elemental.nickname)
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
        elemental = ElementalBuilder().build()
        elemental.note = note
        self.assertEqual(elemental.note, note, error)

    def test_note_max_length(self):
        error = "Elemental note can incorrectly be set to more than 75 characters"
        elemental = ElementalBuilder().build()
        elemental.note = error
        name_length = len(elemental.note)
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
        self.level_up(elemental)
        self.assertEqual(species._physical_att, 15, error)
        self.assertEqual(species._magic_att, 15, error)
        self.assertEqual(species._physical_def, 15, error)
        self.assertEqual(species._magic_def, 10, error)
        self.assertEqual(species._speed, 5, error)
        self.assertEqual(species._max_hp, 50, error)

    def test_has_ability(self):
        error = "Elemental didn't get Abilities on instantiation"
        elemental = ElementalBuilder().build()
        self.assertIsInstance(elemental.active_abilities[0], Ability, error)

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
        elemental = ElementalBuilder() \
            .with_attribute_manager(manager) \
            .with_level(10) \
            .build()
        p_att_before = elemental.physical_att
        elemental.raise_attribute(0)
        p_att_after = elemental.physical_att
        self.assertGreater(p_att_after, p_att_before, error)

    def test_initial_abilities(self):
        error = "Elemental didn't learn abilities on creation"
        elemental = ElementalBuilder().build()
        num_abilities = len(elemental.active_abilities)
        self.assertGreater(num_abilities, 0, error)

    def test_learn_abilities_by_level(self):
        error = "Elemental couldn't learn an ability by leveling"
        elemental = ElementalBuilder() \
            .with_level(1) \
            .with_species(self.get_species()) \
            .build()
        initial_num_abilities = len(elemental.active_abilities)
        exp = elemental.exp_to_level * 500  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        leveled_num_abilities = len(elemental.active_abilities)
        self.assertGreater(leveled_num_abilities, initial_num_abilities, error)

    def test_learn_defend(self):
        error = "Elemental must learn Defend as a basic ability"
        elemental = ElementalBuilder().build()
        has_defend = False
        for ability in elemental.active_abilities:
            if ability.name == 'Defend':
                has_defend = True
        self.assertIs(has_defend, True, error)

    def test_duplicate_abilities(self):
        error = "Elemental can incorrectly learn the same ability"
        species = SpeciesBuilder().with_abilities([self.get_learnable_ability(level=1)]).build()
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        num_abilities = len(elemental.active_abilities)  # Should be 2 because of the default ability Defend
        self.assertEqual(num_abilities, 2, error)

    def test_num_active_abilities(self):
        error = "Elemental can incorrectly have more than 5 abilities active"
        species = self.get_species()
        # Level until we learn all abilities, 6 in total including Defend
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        num_abilities = len(elemental.active_abilities)
        self.assertEqual(num_abilities, 5, error)

    def test_available_abilities(self):
        error = "Abilities weren't listed as available when learned"
        species = self.get_species()
        # Level until we learn all abilities, 6 in total including Defend
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        num_abilities = len(elemental.available_abilities)
        self.assertEqual(num_abilities, 6, error)

    def test_eligible_abilities(self):
        error = "Eligible abilities didn't separate active from available abilities correctly"
        species = self.get_species()
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        num_active = len(elemental.active_abilities)
        num_available = len(elemental.available_abilities)
        num_eligible = len(elemental.eligible_abilities)
        self.assertEqual(num_eligible, num_available - num_active, error)

    def test_swap_ability(self):
        error = "Elemental couldn't swap an ability"
        species = self.get_species()
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        active_ability = elemental.active_abilities[0]
        eligible_ability = elemental.eligible_abilities[0]
        elemental.swap_ability(active_ability, eligible_ability)
        self.assertIn(eligible_ability, elemental.active_abilities, error)

    def test_swap_defend(self):
        error = "Elemental can incorrectly swap out Defend for another ability"
        species = self.get_species()
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        defend = next(ability for ability in elemental.active_abilities if ability.name == 'Defend')
        other_ability = elemental.eligible_abilities[0]
        elemental.swap_ability(defend, other_ability)
        self.assertIn(defend, elemental.active_abilities, error)

    def test_set_abilities(self):
        error = "Elemental abilities couldn't be replaced"
        species = self.get_species()
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        abilities = [Slam(), RollingThunder(), Rend(), Fireball()]
        elemental.set_abilities(abilities)
        correctly_added = 0
        ability_names = [ability.name for ability in elemental.active_abilities]
        for ability in abilities:
            if ability.name in ability_names:
                correctly_added += 1
        self.assertEqual(correctly_added, len(abilities), error)

    def test_set_excessive_abilities(self):
        error = "Replacing an elemental's abilities with an excessive set wasn't handled correctly"
        species = self.get_species()
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        abilities = [Slam(), RollingThunder(), Rend(), Fireball(), Claw()]
        elemental.set_abilities(abilities)
        ability_names = [ability.name for ability in elemental.active_abilities]
        self.assertNotIn(Claw().name, ability_names, error)
        self.assertEqual(5, len(elemental.active_abilities))

    def test_set_abilities_readd_defend(self):
        error = "Defend wasn't re-added when replacing an elemental's abilities"
        species = self.get_species()
        elemental = ElementalBuilder().with_level(5).with_species(species).build()
        abilities = [Slam(), RollingThunder(), Rend(), Fireball()]
        elemental.set_abilities(abilities)
        ability_names = [ability.name for ability in elemental.active_abilities]
        self.assertIn(Defend().name, ability_names, error)