from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Entity, PlayerClass, Mob


class Item:
    """Items that can be used by the player."""

    def interact(self, player):
        pass
