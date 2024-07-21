import asset_manager
import pygame
from global_vars import *

class Entity:
    def __init__(self, x_pos, y_pos, h, w, texture_id):
        self.rect = pygame.Rect(x_pos, y_pos, w, h)
        self.real_pos = [x_pos, y_pos]
        self.tex_id = texture_id
        self.x_movement = self.y_movement = False
        self.speed = 0
        self.angle = 0
    
    def update(self, x_up, y_up):
        self.real_pos[0] += x_up
        self.real_pos[1] += y_up
        self.rect.x = int(self.real_pos[0])
        self.rect.y = int(self.real_pos[1])
        
    def render(self, display):
        tex = asset_manager.AssetManager.get_texture(self.tex_id)
        if self.angle != 0:
            tex = pygame.transform.rotate(asset_manager.AssetManager.get_texture(self.tex_id), self.angle)

        display.blit(tex, (self.rect.x - camera[0],self.rect.y - camera[1]))