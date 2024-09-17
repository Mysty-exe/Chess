import pygame
import Project.constants as constants
import Project.instance as instance
import sys

class GameController:

    def __init__(self):
        pygame.init()

        self.title = constants.TITLE
        self.icon = pygame.image.load(constants.ICON)
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)

        self.game_state = "Menu"
        self.game = instance.GameInstance()

        self.fps = constants.FPS
        self.dt = self.fps
        self.clock = pygame.time.Clock()

        self.copyOfDisplay = None

    def run(self):
        while self.game_state != 'Quit':
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.game_state = 'Quit'

            if self.game_state == 'Menu':
                self.game_state = self.game.main_menu(self.dt, self.game_state, events)

            if self.game_state == 'Lobby':
                self.game_state = self.game.lobby(self.dt, self.game_state, events)
            
            if self.game_state == 'Server Fail':
                self.game_state = self.game.serverFailed(self.dt, self.game_state, events)

            if self.game_state == 'Game':
                self.game_state, self.copyOfDisplay = self.game.run(self.dt, self.game_state, events)

            if self.game_state == 'Forfeit':
                self.game_state = self.game.forfeitedEnd(self.dt, self.game_state, events, self.copyOfDisplay)

            if self.game_state == 'Forfeited':
                self.game_state = self.game.forfeitEnd(self.dt, self.game_state, events, self.copyOfDisplay)
            
            if self.game_state == 'Checkmate':
                self.game_state = self.game.checkmateEnd(self.dt, self.game_state, events, self.copyOfDisplay)

            if self.game_state == 'Checkmated':
                self.game_state = self.game.checkmatedEnd(self.dt, self.game_state, events, self.copyOfDisplay)

            pygame.display.update()
            self.dt = (self.clock.tick(self.fps) / 1000) * 60

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()
