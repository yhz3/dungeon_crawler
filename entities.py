from __future__ import annotations
import random


class Entity:
    """A type of character the player can play as.

    hp: current hp of entity
    max_hp: maximum hp of entity
    mana: current mana of entity
    max_mana: maximum mana of entity
    ad: attack damage of entity
    mp: magic power of entity
    speed: speed at which entity casts abilities and evades attacks
        used to calculate whether abilities of entity land or not
    abilities: a list of abilities of the entity

    === Representation Invariants ===
    - 0 <= hp <= _max_hp
    - 0 <= mana <= _max_mana
    - there are no duplicate abilities in abilities
    """

    hp: int
    _max_hp: int
    mana: int
    _max_mana: int
    ad: int
    mp: int
    speed: int
    _abilities: list[Ability]

    def __init__(self, name: str, hp: int, mana: int, ad: int, mp: int,
                 speed: int, abilities: list[Ability]):
        """Initialize an instance of PlayerClass. Start off with hp = _max_hp
        and mana = _max_mana."""
        self.name = name
        self.hp, self._max_hp = hp, hp
        self.mana, self._max_mana = mana, mana
        self.ad = ad
        self.mp = mp
        self.speed = speed
        self._abilities = abilities

    def use_ability(self, ability: int, target: Entity):
        original_hp = target.hp
        success = self._abilities[ability].use(self, target)
        if success:
            damage = original_hp - target.hp
            print(self.name + ' damaged ' + target.name + ' for ' + str(damage)
                  + ' using ' + str(self._abilities[ability]))
        else:
            print(self.name + ' missed')


    def heal(self):
        """Changes the value of _hp to _max_hp."""
        self.hp = self._max_hp

    def mana_refill(self):
        self.mana = self._max_mana


class PlayerClass(Entity):
    """A type of character the player can play as.

    hp: current hp of player
    max_hp: maximum hp of player
    mana: current mana of player
    max_mana: maximum mana of player
    ad: attack damage of player
    mp: magic power of player
    speed: speed at which player casts abilities and evades attacks
        used to calculate whether abilities of player land or not
    abilities: a list of abilities of the player
    items: a list of items the player has

    === Representation Invariants ===
    - hp <= _max_hp
    - mana <= _max_mana
    - there are no duplicate abilities in abilities
    """

    def fight_menu(self) -> str:
        """Returns current hp, mana, and the list of abilities available to
        the player."""
        option_string = ''
        option_string += self.name + '\n'
        option_string += 'HP: ' + str(self.hp) + '/' + str(self._max_hp) + '\n'
        option_string += 'Mana: ' + str(self.mana) + '/' + str(self._max_mana) \
                         + '\n' + '\n'

        option_string += 'Abilities: \n'
        i = 1
        for ability in self._abilities:
            option_string += str(i) + '. ' + str(ability) + ': ' + ability.desc\
            + '\n'
            i += 1
        return option_string

    def get_ability_len(self):
        return len(self._abilities)


class Knight(PlayerClass):

    def __init__(self, name: str):
        self.name = name
        self.hp, self._max_hp = 150, 150
        self.mana, self._max_mana = 0, 0
        self.ad = 40
        self.mp = 0
        self.speed = 50
        self._abilities = [Slash(), HeavySwing()]


class Mage(PlayerClass):

    def __init__(self, name: str):
        self.name = name
        self.hp, self._max_hp = 90, 90
        self.mana, self._max_mana = 150, 150
        self.ad = 20
        self.mp = 50
        self.speed = 55
        self._abilities = [Slash(), ArcaneBlast(), ArcaneComet()]


class Mob(Entity):

    def use_ability(self, target: Entity):
        ability = self.choose_ability()
        while self._abilities[ability].cost > self.mana:
            ability = self.choose_ability()
        Entity.use_ability(self, ability, target)

    def choose_ability(self):
        return random.randint(0, len(self._abilities) - 1)

    def get_info(self):
        # Used to make the string displaying hp and mana for the player.
        info_str = ''
        info_str += str(self.name) + '\n'
        info_str += 'HP: ' + str(self.hp) + '/' + str(self._max_hp) + '\n'
        info_str += 'Mana: ' + str(self.mana) + '/' + str(self._max_mana) + '\n'
        info_str += 'Attack: ' + str(self.ad) + '\n'
        info_str += 'Magic: ' + str(self.mp)
        return info_str


class DarkKnight(Mob):

    def __init__(self):
        hp = random.randint(140, 170)
        mana = random.randint(50, 70)
        self.name = 'Dark Knight'
        self.hp, self._max_hp = hp, hp
        self.mana, self._max_mana = mana, mana
        self.ad = random.randint(40, 60)
        self.mp = random.randint(10, 20)
        self.speed = random.randint(30, 55)
        self._abilities = [Slash(), HeavySwing(), BloodSlash()]


class DarkMage(Mob):

    def __init__(self):
        hp = random.randint(70, 100)
        mana = random.randint(50, 70)
        self.name = 'Dark Mage'
        self.hp, self._max_hp = hp, hp
        self.mana, self._max_mana = mana, mana
        self.ad = random.randint(10, 15)
        self.mp = random.randint(30, 50)
        self.speed = random.randint(45, 60)
        self._abilities = [Slash(), ArcaneBlast(), ArcaneComet(), Backstab()]


class God(Mob):

    def __init__(self):
        hp = 400
        mana = 400
        self.name = 'God'
        self.hp, self._max_hp = hp, hp
        self.mana, self._max_mana = mana, mana
        self.ad = 1000
        self.mp = 1000
        self.speed = 100
        self._abilities = [Smite()]


class Ability:
    """Abilities that can be used by an Entity. Usability depends on class of
    player, as well as their stats. Abilities can scale with stats."""
    desc: str
    cost: int

    def __init__(self):
        raise NotImplementedError

    def use(self, caster: Entity, target: Entity):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def check_below_zero(self, target: Entity):
        # If a target's health is below zero due to an ability, their health is
        # changed to zero.
        if target.hp < 0:
            target.hp = 0



def hit_success(greater_chance: int, equal_chance: int,
                less_chance: int, caster: Entity, target: Entity) -> bool:
    # Gives different chances for hitting depending on the speed of the caster
    # and target. Allows for the probabilities to be varied between abilities
    if caster.speed > target.speed:
        success_probability = greater_chance
    elif caster.speed == target.speed:
        success_probability = equal_chance
    else:
        success_probability = less_chance
    return success_probability >= random.randint(0, 100)


class Slash(Ability):

    def __init__(self):
        """Initializes an instance of Slash"""
        self.desc = 'Quick and fast attack. \nUses physical damage.'
        self.cost = 0

    def __str__(self):
        return "Slash"

    def use(self, caster: Entity, target: Entity):
        success = hit_success(80, 60, 40, caster, target)
        if success:
            target.hp -= caster.ad
        self.check_below_zero(target)
        return success


class ArcaneBlast(Ability):

    def __init__(self):
        """Initializes an instance of ArcaneBlast"""
        self.desc = 'Fires a blast of magic. \nUses magic. \nMana cost: 30'
        self.cost = 30

    def __str__(self):
        return "Arcane Blast"

    def use(self, caster: Entity, target: Entity):
        success = hit_success(90, 70, 55, caster, target)
        caster.mana -= self.cost
        if success:
            target.hp -= caster.mp
        self.check_below_zero(target)
        return success


class HeavySwing(Ability):

    def __init__(self):
        self.desc = 'Swings weapon at enemy. \nUses physical damage.'
        self.cost = 0

    def __str__(self):
        return 'Heavy Swing'

    def use(self, caster: Entity, target: Entity):
        success = hit_success(65, 50, 45, caster, target)
        if success:
            target.hp -= caster.ad * 2
        self.check_below_zero(target)
        return success


class ArcaneComet(Ability):

    def __init__(self):
        self.desc = 'Summon an arcane comet. \nUses magic. \nMana cost: 35'
        self.cost = 35

    def __str__(self):
        return 'Arcane Comet'

    def use(self, caster: Entity, target: Entity):
        caster.mana -= self.cost
        success = hit_success(65, 50, 45, caster,target)
        if success:
            target.hp -= caster.mp * 2.5
            self.check_below_zero(target)
        return success


class Backstab(Ability):

    def __init__(self):
        self.desc = 'Backstab enemy. Requires speed to be higher than that of '\
                    'the enemy. \nUses physical damage.'
        self.cost = 0

    def __str__(self):
        return 'Backstab'

    def use(self, caster: Entity, target: Entity):
        if caster.speed > target.speed:
            target.hp -= caster.ad // 2
            self.check_below_zero(target)
            return True
        else:
            return False


class BloodSlash(Ability):

    def __init__(self):
        self.desc = 'Infuse blade with own blood and slash enemy. \n' \
                    'Uses physical damage and magic. \n'\
                    'HP cost: 20'\
                    'Mana cost: 30'
        self.cost = 30

    def __str__(self):
        return "Blood Slash"

    def use(self, caster: Entity, target: Entity):
        success = hit_success(80, 70, 50, caster, target)
        caster.hp -= 20
        caster.mana -= 30
        if success:
            target.hp -= (caster.ad + caster.mp)
        self.check_below_zero(target)
        self.check_below_zero(caster)
        return success


class Smite(Ability):

    def __init__(self):
        self.desc = 'The weapon of God. \nDeals holy damage.'
        self.cost = 0

    def __str__(self):
        return 'Smite'

    def use(self, caster: Entity, target: Entity):
        success = hit_success(15, 15, 15, caster, target)
        if success:
            target.hp = 0
        return success
