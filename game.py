import random
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_s,
    K_a,
    K_1,
    K_2,
    K_3,
    K_ESCAPE,
    K_r,
    KEYDOWN,
    QUIT,
)

from objects.character import Character
from objects.weapon import Weapon
from helper.menu import Menu

from settings import (
    TILE_S,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    NUM_TILES,
    TILE_COLOR_ONE,
    TILE_COLOR_TWO,
    NPC_NUMS,
    WEAPONS
)

ACTION_KEYS = [
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_s,
    K_a,
]

SWITCH_KEYS = [
    K_1,
    K_2,
    K_3
]

KEY_MATCHING = {
    K_1: 0,
    K_2: 1,
    K_3: 2
}


class Game():
    # ----------------- init functions -------------------
    def init_weapons(self):
        """Returns an array of weapons.

        Creates a Weapon instance for each weapon in the settings.
        """
        return [
           Weapon(wpn[0], wpn[1], wpn[2]) for wpn in WEAPONS
        ]

    def init_chars(self):
        """Returns an array of Characters (npcs) and a Character instance (player).

        Creates a Character instance for each npc.
        Creates a Character instance for the player.
        Two characters cannot share the same position.
        Assigns a random weapon to each character except player.
        Assigns an index to each npc to healp display their health
        and position.
        """
        npcs = []
        positions = []
        for x in range(NPC_NUMS + 1):
            picked_position = False
            position = None
            # pick a unique position randomly on the board
            while not picked_position:
                position = (
                    random.randint(0, NUM_TILES - 1),
                    random.randint(0, NUM_TILES - 1)
                )
                if position not in positions:
                    picked_position = True
                    positions += [position]
            # instantiates Character with no weapons
            if x == NPC_NUMS:
                char = Character(position, None)
            # instantiates a Character with a random weapon for the npcs
            else:
                npcs += [Character(
                    position,
                    random.choice(self.weapons),
                    npc_index=x + 1
                )]
        return npcs, char

    def __init__(self):
        """Initializes the game class.

        The game is not runing by default.
        Initializes the display from the pygame lib.
        Instantiates the Menu.
        """
        pygame.init()
        self.running = False
        self.turn = 1
        self.weapons = self.init_weapons()
        self.npcs, self.character = self.init_chars()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tile = pygame.Surface((TILE_S, TILE_S))
        self.menu = Menu(self)

    # ----------------- player logic  -------------------
    def attack(self, by_npc=False):
        """Handles both player and npc attacks.

        Deals damage and backlash from weapon.
        Removes dead npc from npcs array.
        Ends game if player is dead.
        """
        # retrieve npc in the same tile as the player
        npc = self.npcs[self.fighting]
        # check who is attacking
        if not by_npc:
            attacker = self.character
            victim = npc
        else:
            attacker = npc
            victim = self.character
        # deal damage if weapon is held
        wpn = attacker.weapon
        if wpn:
            victim.get_hit(wpn.dmg)
            attacker.get_hit(wpn.backlash)
        # remove dead npc
        if not npc.alive:
            self.npcs.pop(self.fighting)
            if len(self.npcs) == 0:
                self.end_game(True)
        if not self.character.alive:
            self.end_game(False)

    def end_turn(self):
        """Runs at the end of a players' turn.

        Heals player and NPCs.
        Although not expressly defined in the assignment the player
        only heals at the end of his turn.
        Checks whether character and npc in same tile.
        """
        self.fighting = None
        self.character.heal()
        # check if character in same position as npc
        for count, npc in enumerate(self.npcs):
            npc.heal()
            if (
                self.character.pos_x,
                self.character.pos_y
            ) == (npc.pos_x, npc.pos_y):
                self.fighting = count
        # attack player if in same tile
        if type(self.fighting) == int:
            self.attack(by_npc=True)
        # we only count player's turns as it would otherwise be confusing
        self.turn += 1
        # update board and menu
        self.draw()

    def switch_weapon(self):
        """Waits for user to pick a weapon among choices.

        Triggers menu list of weapons.
        Action keys are ignored and players cannot move.
        """
        picked = False
        # show options in menu
        self.menu.draw_weapon_choices()
        pygame.display.flip()
        # wait for weapon choice
        while self.running and not picked:
            events = pygame.event.get()
            # allow players to quit
            self.listen_to_quit_or_reset(events)
            for event in events:
                if event.type == KEYDOWN and event.key in SWITCH_KEYS:
                    self.character.weapon = \
                        self.weapons[KEY_MATCHING[event.key]]
                    picked = True

    def player_play(self, events):
        """Handles inputs during player's turn.

        Only inputs from the ACTION_KEYS array are taken into account.
        """
        for event in events:
            if event.type == KEYDOWN and event.key in ACTION_KEYS:
                # move up
                if event.key == K_UP and self.character.pos_y > 0:
                    self.character.pos_y -= 1
                    self.end_turn()
                # move down
                elif event.key == K_DOWN and \
                        self.character.pos_y < NUM_TILES - 1:
                    self.character.pos_y += 1
                    self.end_turn()
                # move left
                elif event.key == K_RIGHT and \
                        self.character.pos_x < NUM_TILES - 1:
                    self.character.pos_x += 1
                    self.end_turn()
                # move right
                elif event.key == K_LEFT and self.character.pos_x > 0:
                    self.character.pos_x -= 1
                    self.end_turn()
                # switch weapon
                elif event.key == K_s:
                    self.switch_weapon()
                    self.end_turn()
                # attack if in same position as npc and weapon held
                elif event.key == K_a and self.character.weapon and \
                        type(self.fighting) == int:
                    self.attack()
                    self.end_turn()

    # ------------------ draw functions ------------------
    def draw_tiles(self):
        """Draw the board"""
        for x in range(NUM_TILES):
            for y in range(NUM_TILES):
                self.tile.fill(TILE_COLOR_ONE)
                if (x + y) % 2 == 0:
                    self.tile.fill(TILE_COLOR_TWO)
                self.screen.blit(self.tile, (x*TILE_S, y*TILE_S))

    def draw_chars(self):
        """Draw the characters."""
        for npc in self.npcs:
            npc.draw(self.screen)
        self.character.draw(self.screen)

    def draw(self):
        """Draw everything."""
        self.draw_tiles()
        self.draw_chars()
        self.menu.draw()
        pygame.display.flip()

    # ----------------- run and end game -------------------
    def run(self):
        """Start the game."""
        self.running = True
        self.draw()
        self.mainloop()

    def end_game(self, victory):
        """End the game."""
        if not victory:
            self.menu.draw_defeat()
        else:
            self.menu.draw_victory()
        pygame.display.flip()
        while True:
            events = pygame.event.get()
            self.listen_to_quit_or_reset(events)

    def reset_game(self):
        self.__init__()
        self.run()

    def listen_to_quit_or_reset(self, events):
        """Quit the game when escape pressed or x clicked."""
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_r:
                    self.reset_game()
            elif event.type == QUIT:
                self.running = False

    def mainloop(self):
        """Main game loop."""
        while self.running:
            events = pygame.event.get()
            self.listen_to_quit_or_reset(events)
            self.player_play(events)