from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Entity


class Ability:
    """Abilities that can be used by the player. Usability depends on class of
    player, as well as their stats. Abilities can scale with stats."""

    def use(self, caster: Entity, target: Entity):
        raise NotImplementedError


class Slash(Ability):

    def __init__(self):
        """Initializes an instance of Slash"""

    def use(self, caster: Entity, target: Entity):
        target.hp -= caster.ad
        if target.hp < 0:
            target.hp = 0
