class Targetable:
    """
    An entity that is targetable by ElementalActions. For example, CombatTeam and CombatElemental.
    In the case of CombatTeam, many of these will remain stubs.
    """
    def on_receive_ability(self, ability, actor):
        raise NotImplementedError

    def receive_damage(self, amount, actor):
        raise NotImplementedError

    def heal(self, amount):
        raise NotImplementedError

    def add_status_effect(self, effect):
        raise NotImplementedError
