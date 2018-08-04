from src.core.elements import Elements


class Targetable:
    """
    An entity that is targetable by ElementalActions. For example, CombatTeam and CombatElemental.
    """
    def on_receive_ability(self, ability, actor):
        raise NotImplementedError

    def receive_damage(self, amount: int, actor):
        raise NotImplementedError

    def heal(self, amount: int):
        raise NotImplementedError

    def add_status_effect(self, effect):
        raise NotImplementedError

    def update_mana(self, amount: int):
        raise NotImplementedError

    @property
    def element(self) -> Elements:
        raise NotImplementedError

    @property
    def damage_reduction(self) -> float:
        raise NotImplementedError

    @property
    def physical_def(self) -> int:
        raise NotImplementedError

    @property
    def magic_def(self) -> int:
        raise NotImplementedError

    @property
    def nickname(self) -> str:
        raise NotImplementedError

    @property
    def is_knocked_out(self) -> bool:
        raise NotImplementedError