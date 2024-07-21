import math
import entity
import collision
from global_vars import *

class Projectile(entity.Entity):
    friendly_projectiles = []
    enemy_projectiles = []

    def __init__(self, x_src, y_src, angle, range, friendly, texture_id = 'projectile', speed = 4, add_to_list = True):
        super().__init__(x_src, y_src, PROJ_WIDTH, PROJ_HEIGH, texture_id)
        self.active = True
        self.float_x, self.float_y = x_src, y_src #TODO;
        angle = math.radians(angle)
        cos_alpha = math.cos(angle)
        sin_alpha = math.sin(angle)
        self.velocity = [speed * cos_alpha, speed * sin_alpha]
        self.velocity_norm = math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])
        self.range = range
        if add_to_list:
            if friendly:
                Projectile.friendly_projectiles.append(self)
            else:
                Projectile.enemy_projectiles.append(self)

    def updateAll(player_rect):
        res = False
        for x in Projectile.friendly_projectiles:
            x.update()
        for x in Projectile.enemy_projectiles:
            if x.update(player_rect):
                return True
        return False

    def update(self, player_rect = None):
        self.float_x += self.velocity[0]
        self.float_y += self.velocity[1]
        self.rect.x = self.float_x
        self.rect.y = self.float_y
        self.range -= self.velocity_norm

        if self.range < 0:
            self.active = False
        elif collision.Collision.tile_hit(self.rect):
            self.active = False
        elif not player_rect and collision.Collision.enemy_hit(self.rect):
            self.active = False
        elif player_rect and collision.Collision.AABB(self.rect, player_rect):
            self.active = False
            return True
        return False

    def simulate(target, x_src, y_src, angle, range, spd):
        #Projectile(x_src, y_src, angle, range, False, texture_id = 'projectile', speed = spd)
        proj = Projectile(x_src, y_src, angle, range, False, texture_id = 'none', speed = spd, add_to_list = False)
        while proj.isActive():
            proj.update(target)
            if collision.Collision.AABB(proj.rect, target):
                return True
        return False

    def destroy(self):
        self.active = False

    def isActive(self):
        return self.active

    def clear():
        Projectile.friendly_projectiles = []
        Projectile.enemy_projectiles = []

    def refresh():
        Projectile.friendly_projectiles = [x for x in Projectile.friendly_projectiles if x.isActive()]
        Projectile.enemy_projectiles = [x for x in Projectile.enemy_projectiles if x.isActive()]

    def renderAll(display):
        for x in Projectile.friendly_projectiles:
            x.render(display)
        for x in Projectile.enemy_projectiles:
            x.render(display)
