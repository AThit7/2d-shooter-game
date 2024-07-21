import entity
from global_vars import *
import projectile
import asset_manager
import random

class IllegalArgumentError(ValueError):
    pass

class Weapon(entity.Entity):
    """
    Weapon przechowuje informacje o broni używanej prze obiekty klas Enemy i Player
    """
    def __init__(self, x_pos, y_pos, w, h, texture_id):
        """
        Tworzy nowy obiekt Weapon
        """
        if texture_id == "random":
            texture_id = random.choice(("pistol", "rifle"))
        super().__init__(x_pos, y_pos, h, w, texture_id)
        self.sound_id = texture_id
        self.explosion_range = -1
        self.timer = 0
            
        if texture_id == "pistol":
            self.range = 360
            self.ammo = 20
            self.volume = 600
            self.bullet_speed = 4
            self.delay = 20
        elif texture_id == "flamethrower":
            raise NotImplementedError("TODO")
            self.range = 40
            self.ammo = 200
            self.volume = 200
            self.bullet_speed = 1
            self.delay = 1
        elif texture_id == "rifle":
            self.range = 360
            self.ammo = 30
            self.volume = 2000
            self.bullet_speed = 4
            self.delay = 10
        else:
            raise IllegalArgumentError("No such weapon")
        self.ammo = [self.ammo, self.ammo]
        self.tex_id = "none" #TODO; usunac

    def update(self, x_pos, y_pos, angle):
        """
        Aktualizuje stan broni
        """
        if self.timer > 0:
            self.timer -= 1
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.angle = angle

    def shoot(self, friendly = True):
        """
        Tworzy Projectile przemieszczający się w kierunku, w którym wskazuje broń
        """
        if (not self.timer) and self.ammo[0]:
            self.ammo[0] -= 1
            self.timer = self.delay
            projectile.Projectile(self.rect.centerx, self.rect.centery, self.angle, self.range, friendly, speed = self.bullet_speed)
            asset_manager.AssetManager.play_sound("gun1")

    def simulate(self, angle, target):
        """
        Symuluje drogę pocisku gdyby został teraz wystrzelony

        :param target: Prostokąt, w którego kierunku leci pocisk
        :return: True jeśli nastąþi kolizja z target, False w p.p.
        """
        return projectile.Projectile.simulate(target, self.rect.centerx, self.rect.centery, angle, self.range, self.bullet_speed)
