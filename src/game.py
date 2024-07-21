import sys
import pygame
from pygame.locals import QUIT
import player
import asset_manager
import map
import projectile
from global_vars import *
import enemy

class Game:

    def __init__(self):
        self.window_size = WINDOW_SIZE
        self.clock = pygame.time.Clock()
        self.current_level = 1
        pygame.init()
        pygame.font.init()
        self.display = pygame.Surface((SURFACE_SIZE))
        self.screen = pygame.display.set_mode(self.window_size,0,32)
        pygame.display.set_icon(self.screen)
        pygame.display.set_caption('game')
        asset_manager.AssetManager.init()
        self.load_level()

    def load_level(self):
        enemy.Enemy.clear()
        projectile.Projectile.clear()
        map.Map.clear()

        try:
            player_pos, enem_list = map.Map.load_map('assets/maps/map{}.map'.format(self.current_level))
        except FileNotFoundError:
            self.display
            while True:
                self.display.blit(pygame.image.load('assets/textures/end_game_screen.png'),(0,0))
                surf = pygame.transform.scale(self.display, self.window_size)
                self.screen.blit(surf, (0, 0))    
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

        asset_manager.AssetManager.add_sound('gun1', 'assets/sounds/gun_shot.wav')
        asset_manager.AssetManager.add_texture('enemy', 'assets/textures/enemy.png')
        asset_manager.AssetManager.add_texture('player', 'assets/textures/player.png')
        asset_manager.AssetManager.add_texture('projectile', 'assets/textures/projectile.png')
        self.player = player.Player(player_pos[0], player_pos[1], 16, 16, 'player')
        for pos in enem_list:
            enemy.Enemy(pos[0], pos[1], 16, 16,'enemy')
        self.true_scroll = [self.player.rect.centerx, self.player.rect.centery]

    def run(self):
        while True:
            self.update()
            self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == pygame.MOUSEBUTTONDOWN:
            #    pass
            else:
                self.player.handle_events(event)

        self.player.update()
        enemy.Enemy.updateAll(self.player.rect)
        tmp = projectile.Projectile.updateAll(self.player.rect)
        projectile.Projectile.refresh()
        if tmp or projectile.Projectile.updateAll(self.player.rect):
            self.load_level()

        enemy.Enemy.refresh()
        projectile.Projectile.refresh()

        if enemy.Enemy.empty():
            self.current_level += 1
            self.load_level()

        pr = self.player.rect
        px, py = pr.x, pr.y

        self.true_scroll[0] += (px - self.true_scroll[0] - (self.display.get_width() - 16) / 2) / 10
        self.true_scroll[1] += (py - self.true_scroll[1] - (self.display.get_height() - 16) / 2) / 10
        camera[0] = int(self.true_scroll[0])
        camera[1] = int(self.true_scroll[1])


    def render(self):
        self.display.fill((112, 112, 112))

        map.Map.render(self.display, 0)

        if SHOW_ENEMY_PATHS:
            enemy.Enemy.draw_paths(self.display)

        projectile.Projectile.renderAll(self.display)
        enemy.Enemy.renderAll(self.display)
        self.player.render(self.display)

        map.Map.render(self.display, 1)
        self.player.render_info(self.display)

        surf = pygame.transform.scale(self.display, self.window_size)
        self.screen.blit(surf, (0, 0))    
        pygame.display.update()
        self.clock.tick(60)
        pygame.display.set_caption('game \t FPS: ' + "{:.3f}".format(1000 / self.clock.get_time()))