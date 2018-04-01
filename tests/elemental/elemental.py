import unittest


class ElementalTests(unittest.TestCase):
    def setUp(self):
        self.elemental = ElementalBuilder().with_level(1).build()

    def tearDown(self):
        self.elemental.dispose()
        self.elemental = None

    def get_species(self) -> 'Species':
        return SpeciesBuilder() \
            .with_physical_att(15) \
            .with_magic_att(15) \
            .with_physical_def(15) \
            .with_magic_def(10) \
            .with_speed(5) \
            .with_hp(50) \
            .with_growth_rate({
                'physical_att': 1,
                'magic_att': 1,
                'physical_def': 1,
                'magic_def': 1,
                'speed': 2,
                'hp': 3
            }).build()

    def get_predetermined_attributes(self):
        return [AttributeFactory.physical_att_attribute(),
                AttributeFactory.magic_att_attribute(),
                AttributeFactory.hp_attribute()]

    def test_gain_exp(self):
        error = "Elemental couldn't acquire experience"
        self.elemental.add_exp(10)
        exp_gained = self.elemental.current_exp
        self.assertEqual(exp_gained, 10, error)

    def test_level_up(self):
        error = "Elemental couldn't level"
        exp_to_level = self.elemental.exp_to_level
        before_level = self.elemental.level
        self.elemental.add_exp(exp_to_level)
        after_level = self.elemental.level
        self.assertGreater(after_level, before_level, error)

    def test_level_exp_cap(self):
        error = "Leveling up didn't increase the Elemental's required exp"
        lower_requirement = self.elemental.current_exp
        higher_level_elemental = ElementalBuilder().with_level(2).build()
        higher_requirement = higher_level_elemental.current_exp
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
        self.elemental.set_nickname(name)
        self.assertEqual(self.elemental.nickname, name, error)

    def test_nickname_max_length(self):
        error = "Elemental nickname can incorrectly be set to more than 15 characters"
        self.elemental.set_nickname("dsadadaifjasifjasfdsd")
        name_length = len(self.elemental.nickname)
        self.assertLessEqual(name_length, 15, error)

    def test_reset_nickname(self):
        error = "Elemental nickname couldn't be reset"
        species = SpeciesBuilder().with_name("Richard").build()
        elemental = ElementalBuilder().with_species(species).build()
        name = "Logi"
        elemental.set_nickname(name)
        elemental.reset_nickname()
        self.assertEqual(elemental.nickname, "Richard", error)

    def test_set_note(self):
        error = "Elemental note couldn't be set"
        note = "+PDEF +PATT +SPEED bruiser"
        self.elemental.set_note(note)
        self.assertEqual(self.elemental.note, note, error)

    def test_note_max_length(self):
        error = "Elemental note can incorrectly be set to more than 50 characters"
        self.elemental.set_note(error)
        name_length = len(self.elemental.note)
        self.assertLessEqual(name_length, 50, error)

    def test_gain_stats(self):
        error = "Elemental stat increase level doesn't match its Species' growth rate"
        elemental = ElementalBuilder().with_level(1).with_species(self.get_species()).build()
        exp = self.elemental.exp_to_level
        self.elemental.add_exp(exp)
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
        exp = self.elemental.exp_to_level
        self.elemental.add_exp(exp)
        self.assertEqual(species.base_physical_att, 15, error)
        self.assertEqual(species.base_magic_att, 15, error)
        self.assertEqual(species.base_physical_def, 15, error)
        self.assertEqual(species.base_magic_def, 10, error)
        self.assertEqual(species.base_speed, 5, error)
        self.assertEqual(species.base_max_hp, 50, error)

    def test_has_attribute_manager(self):
        error = "Elemental didn't get an AttributeManager on instantiation"
        self.assertIsInstance(self.elemental.attributes, AttributeManager, error)

    def test_has_ability_manager(self):
        error = "Elemental didn't get an AbilityManager on instantiation"
        self.assertIsInstance(self.elemental.abilities, AbilityManager, error)

    def test_owner_restricts_level(self):
        error = "Elemental shouldn't be able to level past its owner"
        player = PlayerBuilder().with_level(15).build()
        elemental = ElementalBuilder().with_level(14).with_rank(2).with_owner(player).build()
        exp = self.elemental.exp_to_level * 5  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        self.assertEqual(player.level, elemental.level, error)

    def test_rank_restricts_level(self):
        error = "Elemental must have be rank 2 to grow past level 10"
        elemental = ElementalBuilder().with_level(10).with_rank(1).build()
        exp = self.elemental.exp_to_level * 5  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        self.assertEqual(elemental.level, 10, error)

    def test_exp_gain_rank_restriction(self):
        error = "Elemental should be allowed to overflow experience even when it is under-ranked"
        elemental = ElementalBuilder().with_level(10).with_rank(1).build()
        exp = self.elemental.exp_to_level * 5  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        self.assertEqual(elemental.current_exp, exp, error)

    def test_exp_overflow_level(self):
        error = "Elemental failed to resolve overflow exp after it ranked up"
        elemental = ElementalBuilder().with_level(10).with_rank(1).build()
        exp = self.elemental.exp_to_level * 5  # Arbitrary large amount of exp
        elemental.add_exp(exp)
        # elemental.on_rank_up()
        self.assertGreater(elemental.level, 10, error)

    def test_num_attributes(self):
        error = "Elemental must have three attributes"
        elemental = ElementalBuilder().build()
        num_attributes = len(elemental.get_attributes())
        self.assertEqual(num_attributes, 3, error)

    def test_create_unique_attributes(self):
        error = "Elemental can incorrectly have a duplicate attribute"
        for i in range(100):
            elemental = ElementalBuilder().build()
            attributes = elemental.get_attributes()
            no_duplicates = len(attributes) == len(set(attributes))
            self.assertIs(no_duplicates, True, error)

    def test_raise_attribute(self):
        error = "Elemental who met requirements couldn't raise an attribute"
        elemental = ElementalBuilder().with_level(10).with_rank(2).build()
        elemental.raise_attribute(0)
        attributes = elemental.get_attributes()
        attribute_level = attributes[0].get_level()
        self.assertEqual(attribute_level, 1, error)

    def test_attribute_gives_stats(self):
        error = "No stats gained from raising an attribute"
        from_attributes = self.get_predetermined_attributes()  # Physical attack Attribute is guaranteed
        manager = AttributeFactory().create_manager(from_attributes)
        elemental = ElementalBuilder().with_attribute_manager(manager).with_level(10).with_rank(2).build()
        p_att_before = elemental.get_physical_att()
        elemental.raise_attribute(0)
        p_att_after = elemental.get_physical_att()
        self.assertGreater(p_att_after, p_att_before, error)

    def test_initial_abilities(self):
        error = "Elemental didn't learn abilities on creation"
        num_abilities = len(self.elemental.get_abilities())
        self.assertGreater(num_abilities, 1, error)

    def test_learn_abilities_by_level(self):
        error = "Elemental couldn't learn an ability by leveling"
        initial_num_abilities = len(self.elemental.get_abilities())
        exp = self.elemental.exp_to_level * 500  # Arbitrary large amount of exp to reach level 10
        self.elemental.add_exp(exp)
        leveled_num_abilities = len(self.elemental.get_abilities())
        self.assertGreater(leveled_num_abilities, initial_num_abilities, error)

    def test_learn_defend(self):
        error = "Elemental must learn Defend as a basic ability"
        has_defend = False
        for ability in self.elemental.get_abilities():
            if ability.id == Defend.id:
                has_defend = True
        self.assertIs(has_defend, True, error)

    def test_num_active_abilities(self):
        error = "Elemental can incorrectly have more than 5 abilities active"
        # TODO


