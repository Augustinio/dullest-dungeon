import pygame

from settings import (
    MENU_WIDTH,
    PLAY_DIM,
    MAX_DISPLAYED_NPCS
)


class Menu():
    """Define Menu class for displaying game info."""

    def __init__(self, game):
        """Initialize Menu instance."""
        self.game = game
        self.width = MENU_WIDTH
        self.zero = PLAY_DIM + 20  # add a margin
        self.font_title = pygame.font.SysFont(None, 50)
        self.font_hints = pygame.font.SysFont(None, 30)
        self.font_turns = pygame.font.SysFont(None, 15)

    def reset(self):
        """Reset menu area to a black rectangle,"""
        pygame.draw.rect(self.game.screen, 'black', pygame.Rect(
            self.zero, 0, MENU_WIDTH, PLAY_DIM
        ))

    def draw_title(self):
        """Draw title of the game."""
        title = self.font_title.render('Dullest Dungeon', True, 'brown')
        self.game.screen.blit(title, (self.zero, 20))

    def draw_turn(self):
        """Draw current turn."""
        turn = self.font_turns.render(f'turn: {self.game.turn}', True, 'brown')
        self.game.screen.blit(turn, (self.zero + self.width - 80, 10))

    def draw_hints(self):
        """Draw game explanations."""
        hint_one = self.font_hints.render(
            'use the arrows to move', True, 'brown'
        )
        hint_two = self.font_hints.render(
            'a: attack, s: switch weapon', True, 'brown'
        )
        hint_three = self.font_hints.render(
            'esc: quit, r: reset', True, 'white'
        )
        self.game.screen.blit(hint_one, (self.zero, 75))
        self.game.screen.blit(hint_two, (self.zero, 95))
        self.game.screen.blit(hint_three, (self.zero, PLAY_DIM - 30))

    def draw_player_health(self):
        """Draw player healthbar and number."""
        pygame.draw.rect(self.game.screen, 'white', pygame.Rect(
            self.zero, 130, self.width/2, 20
        ), 1)
        pygame.draw.rect(self.game.screen, 'green', pygame.Rect(
            self.zero, 130, self.width/2 * self.game.character.health / 100, 20
        ))
        health_num = self.font_hints.render(
            str(self.game.character.health), True, 'white'
        )
        self.game.screen.blit(health_num, (self.zero + self.width/2 + 20, 130))

    def draw_player_weapon(self):
        """Draw current player weapon."""
        wpn = self.game.character.weapon
        # draw weapon name
        wpn_name = self.font_hints.render(
            wpn.name if wpn else "No Weapon", True, 'white'
        )
        self.game.screen.blit(wpn_name, (self.zero, 160))
        # draw weapon stats
        if wpn:
            wpn_stat_a = self.font_hints.render(str(wpn.dmg), True, 'white')
            wpn_stat_b = self.font_hints.render(str(wpn.backlash), True, 'red')
            self.game.screen.blit(wpn_stat_a, (self.zero, 180))
            self.game.screen.blit(wpn_stat_b, (self.zero + 20, 180))

    def draw_always(self):
        """Draw the top part of the menu"""
        self.reset()
        self.draw_turn()
        self.draw_title()
        self.draw_hints()
        self.draw_player_health()
        self.draw_player_weapon()

    def draw_weapon_choices(self):
        """Draw the weapon choices, including name, dmg and backlash.

        Is displayed when player hits s.
        """
        self.draw_always()
        # draw choose your weapon
        choose = self.font_hints.render("Choose your weapon", True, 'white')
        self.game.screen.blit(choose, (self.zero, 220))
        # draw weapon name and stats for each weapon
        for count, wpn in enumerate(self.game.weapons):
            wpn_name = self.font_hints.render(
                f'[{count + 1}] - {wpn.name}', True, 'white'
            )
            wpn_stat_a = self.font_hints.render(str(wpn.dmg), True, 'white')
            wpn_stat_b = self.font_hints.render(str(wpn.backlash), True, 'red')
            self.game.screen.blit(wpn_name, (self.zero, 260 + 80 * count))
            self.game.screen.blit(wpn_stat_a, (self.zero, 280 + 80 * count))
            self.game.screen.blit(
                wpn_stat_b, (self.zero + 20, 280 + 80 * count)
            )

    def draw_ennemies(self):
        """Draw a list of ennemies and their corresponding stats.

        In order, on each line:
        - npc indec
        - npc health bar
        - npc health number
        - npc weapon dmg and backlash
        """
        remaining = self.font_hints.render(
            f'{len(self.game.npcs)} ennemies remaining', True, 'white'
        )
        self.game.screen.blit(remaining, (self.zero, 220))
        for count, npc in enumerate(self.game.npcs):
            # cap max displayed ennemies to not overflow
            if count > MAX_DISPLAYED_NPCS - 1:
                break
            y = 260 + 40 * count
            # draw npc index
            index = self.font_hints.render(str(npc.npc_index), True, 'red')
            self.game.screen.blit(index, (self.zero, y))
            # draw empty rect
            pygame.draw.rect(self.game.screen, 'red', pygame.Rect(
                self.zero + 30, y, self.width/2, 20
            ), 1)
            # fill rect with health bar
            pygame.draw.rect(self.game.screen, 'red', pygame.Rect(
                self.zero + 30, y, self.width/2 * npc.health / 100, 20
            ))
            # show health number
            health_num = self.font_hints.render(str(npc.health), True, 'red')
            self.game.screen.blit(
                health_num, (self.zero + self.width/2 + 40, y)
            )
            # show npc weapon stats
            wpn_stat_a = self.font_hints.render(
                str(npc.weapon.dmg), True, 'red'
            )
            wpn_stat_b = self.font_hints.render(
                str(npc.weapon.backlash), True, 'white'
            )
            self.game.screen.blit(
                wpn_stat_a, (self.zero + self.width/2 + 100, y)
            )
            self.game.screen.blit(
                wpn_stat_b, (self.zero + self.width/2 + 120, y)
            )

    def draw_defeat(self):
        """Draw defeat screem."""
        self.draw_always()
        game_over = self.font_title.render('GAME OVER', True, 'red')
        self.game.screen.blit(game_over, (self.zero, PLAY_DIM/2))

    def draw_victory(self):
        """Draw victory screem."""
        self.draw_always()
        victory = self.font_title.render('VICTORY', True, 'green')
        self.game.screen.blit(victory, (self.zero, PLAY_DIM/2))

    def draw(self):
        """Draw the top menu part and enemu health.

        Is displayed when player is playing.
        """
        self.draw_always()
        self.draw_ennemies()
