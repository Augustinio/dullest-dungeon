import pygame

from settings import (
    NPC_COLOR,
    CHAR_COLOR,
    TILE_S,
    MAX_HEALTH
)


class Character:
    """Define Character class for npcs and player."""

    def __init__(self, position, weapon, npc_index=None):
        """Initialize a Character instance.

        Characters start with 100 health and are alive.
        Characters can have a weapon.
        Characters have an x and y position on the board.
        NPCs have an index.
        """
        self.health = MAX_HEALTH
        self.alive = True
        self.weapon = weapon
        self.pos_x, self.pos_y = position
        self.npc_index = npc_index

    def get_hit(self, dmg):
        """Handle damage brought to a character.

        If health reaches zero, kill the character.
        """
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def heal(self):
        """Heal character by 1HP if not at max health"""
        if self.health < MAX_HEALTH:
            self.health += 1

    def draw(self, screen):
        """Handle drawing of character.

        If character is a player draw circle.
        Else draw an X and the ennemy number.
        """
        if not self.npc_index:
            # draw a circle at player's position
            pygame.draw.circle(
                screen,
                CHAR_COLOR,
                ((self.pos_x + 1/2) * TILE_S, (self.pos_y + 1/2) * TILE_S),
                TILE_S/2,
                5
            )
        else:
            # draw an X at npc position
            pygame.draw.line(
                screen,
                NPC_COLOR,
                (self.pos_x * TILE_S, self.pos_y * TILE_S),
                ((self.pos_x + 1) * TILE_S, (self.pos_y + 1) * TILE_S),
                5
            )
            pygame.draw.line(
                screen,
                NPC_COLOR,
                ((self.pos_x + 1) * TILE_S, self.pos_y * TILE_S),
                (self.pos_x * TILE_S, (self.pos_y + 1) * TILE_S),
                5
            )
            # draw npc number
            font_npc = pygame.font.SysFont(None, 20)
            npc_index = font_npc.render(str(self.npc_index), True, 'red')
            screen.blit(
                npc_index,
                (self.pos_x * TILE_S, (self.pos_y + 1/3) * TILE_S)
            )
