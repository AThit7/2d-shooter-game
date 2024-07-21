import pygame
import map
from global_vars import *
import enemy

class Collision:
    def AABB(rectA, rectB):
        return (rectA.x < rectB.x + rectB.width and \
        rectA.x + rectA.width > rectB.x and \
        rectA.y < rectB.y + rectB.height and \
        rectA.y + rectA.height > rectB.y)
    
    def tile_hit(rect, inside = False):
        for y in range(rect.top // TILE_SIZE - 0, rect.bottom // TILE_SIZE + 1):
            for x in range(rect.left // TILE_SIZE - 0, rect.right // TILE_SIZE + 1):
                if map.Map.is_collidable(x, y):
                    if inside:
                        if pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE).contains(rect):
                            return True
                    elif (Collision.AABB(rect, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))):
                        return True

    def enemy_hit(rect, inside = False):
        for e in enemy.Enemy.enemylist:
            if (Collision.AABB(rect, e.rect)):
                e.kill()
                return True

    #def draw_tile_hitlist(rect, display):
    #    from game import Game
    #    tmp_red = pygame.Surface((16, 16))
    #    tmp_red.set_alpha(50)
    #    tmp_zxc = tmp_red.copy()
    #    tmp_red.fill((255,0,0))
    #    tmp_red.fill((0,255,0))
    #    for y in range(rect.top // TILE_SIZE - 0, rect.bottom // TILE_SIZE + 1):
    #        for x in range(rect.left // TILE_SIZE - 0, rect.right // TILE_SIZE + 1):
    #            if Map.is_collidable(x, y):
    #                display.blit(tmp_red, (x * TILE_SIZE - Game.camera[0],y * TILE_SIZE - Game.camera[1]))
    #            else:
    #                display.blit(tmp_zxc, (x * TILE_SIZE - Game.camera[0],y * TILE_SIZE - Game.camera[1]))