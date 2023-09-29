import numpy as np
from random import randint
from entities import PlayerClass, Mob, Slash, ArcaneBlast, Backstab, \
    BloodSlash, HeavySwing, ArcaneComet, Knight, DarkKnight, Mage, DarkMage, Smite, God

LINE_BREAK = '--------------------------------------------------------------'


def battle(player: PlayerClass, enemy: Mob):
    print(LINE_BREAK)
    print(enemy.name + ' has challenged you to a battle')
    print(LINE_BREAK)
    input('Press Enter')
    print(LINE_BREAK)
    return battle_recursion(player, enemy)


def battle_recursion(player: PlayerClass, enemy: Mob) -> bool:
    print(enemy.get_info())
    print(LINE_BREAK)
    print(player.fight_menu())
    ability = ability_select(player)
    print(LINE_BREAK)
    player.use_ability(ability, enemy)
    if enemy.hp == 0:
        print(LINE_BREAK)
        return True
    enemy.use_ability(player)
    print(LINE_BREAK)
    if player.hp == 0:
        return False
    else:
        input('Press Enter to continue')
        print(LINE_BREAK)
        return battle_recursion(player, enemy)


def ability_select(player: PlayerClass):
    try:
        ability = int(input('Select an ability')) - 1
        if 0 <= ability <= player.get_ability_len() - 1:
            if player.mana < player._abilities[ability].cost:
                print('Insufficient mana, please select again\n')
                return ability_select(player)
            return ability
        else:
            print('Invalid input, please select again\n')
            return ability_select(player)
    except ValueError:
        print('Invalid input, please select again\n')
        return ability_select(player)


def dungeon(player: PlayerClass, wins: int):
    if randint(1, 5) == 5:
        enemy = God()
    elif randint(1, 2) == 1:
        enemy = DarkKnight()
    else:
        enemy = DarkMage()
    if not battle(player, enemy):
        print('Game over')
    else:
        wins += 1
        print(enemy.name + ' has been slain.\n \nTotal wins:' + str(wins))
        if randint(1, 2) == 1:
            print(LINE_BREAK)
            print('A health potion was found on the corpse.')
            player.heal()
        player.mana_refill()
        input('Press Enter to continue into dungeon')
        dungeon(player, wins)


def select_class():
    player = input('Select a class: ')
    if player == 'Knight':
        name = input('Enter a name: ')
        return Knight(name)
    elif player == 'Mage':
        name = input('Enter a name: ')
        return Mage(name)
    else:
        print('Invalid selection, please select again')
        return select_class()


if __name__ == '__main__':
    print(LINE_BREAK)
    print('Classes')
    print(LINE_BREAK)
    print(Knight('Knight').fight_menu())
    print('\n' + Mage('Mage').fight_menu())
    player = select_class()
    dungeon(player, 0)
