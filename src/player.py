from pygame.transform import scale
import asset_manager
import entity
import pygame
from pygame import *
import collision
import math
from global_vars import *
import weapon

class Player(entity.Entity):
    """
    Reprezentuje postać, którą steruje użytkownik.
    """
    def __init__(self, x_pos, y_pos, h, w, texture_id):
        """
        Tworzy nowy obiekt klasy Player.
        """
        super().__init__(x_pos, y_pos, h, w, texture_id)
        self.moving_left = self.moving_right = self.moving_down = self.moving_up = False
        self.shot_timer = 0
        self.shot_delay = 10
        self.speed = 2.5
        self.weapon = weapon.Weapon(x_pos, y_pos, 4, 4, "rifle")
        self.ammo_text = pygame.font.SysFont('Comic Sans MS', 15)
        
    def handle_events(self, event):
        """
        Określa w którym kierunku użytkownik chce poruszyć obiekt.
        """
        #-----------KEYBOARD-INPUT----------#
        if event.type == KEYDOWN:  
            if event.key == K_a:
                self.moving_left = True
            if event.key == K_d:
                self.moving_right = True
            if event.key == K_w:
                self.moving_up = True
            if event.key == K_s:
                self.moving_down = True
        if event.type == KEYUP:
            if event.key == K_a:
                self.moving_left = False
            if event.key == K_d:
                self.moving_right = False
            if event.key == K_w:
                self.moving_up = False
            if event.key == K_s:
                self.moving_down = False
        #-----------------------------------#

    def update(self):
        """
        Na podstawie inputu sprzętowego zmienia pozycję, kąt obrócenia obiektu.
        """

        if self.shot_timer > 0:
            self.shot_timer -= 1

        old_rect = self.rect.copy()
        old_real_pos = self.real_pos.copy()
        if (self.moving_down or self.moving_up) and (self.moving_left or self.moving_right):
            speed = self.speed / math.sqrt(2)
        else:
            speed = self.speed


        if self.moving_left == self.moving_right:
            x_movement = 0
        elif self.moving_left:
             x_movement = -speed
        elif self.moving_right:
             x_movement = speed

        super().update(x_movement, 0.0)

        col_rect = self.rect.copy()
        col_rect.x += 1
        col_rect.y += 1
        col_rect.width -= 1
        col_rect.height -= 1
        if collision.Collision.tile_hit(col_rect):
            self.rect.x = old_rect.x
            self.real_pos[0] = old_real_pos[0]

        if self.moving_up == self.moving_down:
            y_movement = 0
        elif self.moving_up:
             y_movement = -speed
        elif self.moving_down:
             y_movement = speed

        super().update(0.0, y_movement)

        col_rect = self.rect.copy()
        col_rect.x += 1
        col_rect.y += 1
        col_rect.width -= 1
        col_rect.height -= 1
        if collision.Collision.tile_hit(col_rect):
            self.rect.y = old_rect.y
            self.real_pos[1] = old_real_pos[1]

        mouse_pos = pygame.mouse.get_pos()
        a = mouse_pos[0] * SCALE[0] - self.rect.centerx + camera[0]
        b = mouse_pos[1] * SCALE[1] - self.rect.centery + camera[1]

        self.angle = math.degrees((math.atan2(a, b))) - 180

        self.weapon.update(self.rect.centerx, self.rect.centery, 270 - self.angle)

        if pygame.mouse.get_pressed()[0]:
            self.weapon.shoot()
    
    def render_info(self, display):
        """
        Wyświetla informacje o stanie amunicji w broni gracza.
        """
        surf = self.ammo_text.render('AMMO: {}/{}'.format(self.weapon.ammo[0], self.weapon.ammo[1]), False, (0, 0, 0))
        display.blit(surf, (0, 0))