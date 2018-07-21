

class Targetable:
    """
    An entity that is targetable by ElementalActions. For example, CombatTeam and CombatElemental.
    """
    def on_receive_ability(self, ability, actor):
        raise NotImplementedError

    def receive_damage(self, amount, actor):
        raise NotImplementedError

    def heal(self, amount):
        raise NotImplementedError

    def add_status_effect(self, effect):
        raise NotImplementedError

    def snapshot(self):
        """
        :return CombatElementalLog: A log showing the current health and visible stats of the Elemental at the time
        this snapshot was taken. This is for rendering purposes.
        """
        raise NotImplementedError
