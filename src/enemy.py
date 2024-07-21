import heapq
import math
import pygame
import entity
from global_vars import *
import map
import weapon

HALF_TSIZE = TILE_SIZE / 2

class Enemy(entity.Entity):
    """
    A class to represent a person.

    Zmienne statyczne
    """
    enemylist = []

    def __init__(self, x_pos, y_pos, h, w, texture_id, weapon_type = "random"):
        """
        Tworzy nowy obiekt klasy Enemy
        """
        super().__init__(x_pos, y_pos, h, w, texture_id)
        self.prev_dest = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
        self.path = {}
        self.active = True
        self.notified = False
        self.speed = ENEMY_SPEED
        Enemy.enemylist.append(self)
        self.weapon = weapon.Weapon(x_pos, y_pos, 4, 4, weapon_type)

    def kill(self):
        """
        
        """
        self.active = False
    
    def __heuristic(a, b):
        dif_x = abs(a[0] - b[0])
        dif_y = abs(a[1] - b[1])
        if dif_x > dif_y:
            return 14 * dif_y + 10 * (dif_x - dif_y)
        return 14 * dif_x + 10 * (dif_y - dif_x)

    def find_path(self, dest):

        if dest == self.prev_dest:
            return
        self.prev_dest = dest
 
        # swap src and dest
        src_tile = dest
        dst_tile = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)

        dist_dif = dst_tile[0] - src_tile[0], dst_tile[1] - src_tile[1]
        if not self.notified or math.sqrt(dist_dif[0] * dist_dif[0] + dist_dif[1] * dist_dif[1]) > 23:
            self.notified = True
            self.path = {}
            self.path[dst_tile] = dst_tile
            return

        # A* search 
        came_from = {}
        cost_so_far = {}
        came_from[src_tile] = None
        cost_so_far[src_tile] = 0
        # items on the heap queue: [[tile_f_cost, tile_h_cost, tile_g_cost], [tile_x_pos, tile_y_pos]]
        pqueue = [[[0, 0, 0], src_tile]]

        while pqueue:
            current = heapq.heappop(pqueue)

            if current[1] == dst_tile:
                break

            neighbors = []
            for x in range(current[1][0] - 1, current[1][0] + 2):
                neighbors.append([])
                for y in range(current[1][1] - 1, current[1][1] + 2):
                    neighbors[x - current[1][0] + 1].append([not map.Map.is_collidable(x, y), 10, (x, y)])

            neighbors[1][1][0] = False # current tile is not a neighbor
            # we don't want to allow corner cutting
            neighbors[0][0][0] = neighbors[0][0][0] and neighbors[1][0][0] and neighbors[0][1][0]
            neighbors[2][0][0] = neighbors[2][0][0] and neighbors[2][1][0] and neighbors[1][0][0]
            neighbors[0][2][0] = neighbors[0][2][0] and neighbors[1][2][0] and neighbors[0][1][0]
            neighbors[2][2][0] = neighbors[2][2][0] and neighbors[2][1][0] and neighbors[1][2][0]
            neighbors[0][0][1] = neighbors[2][0][1] = neighbors[0][2][1] = neighbors[2][2][1] = 14

            current_cost = cost_so_far[current[1]]
            for x in range(0, 3):
                for y in range (0, 3):
                    nei = neighbors[x][y]
                    # nei[0] - is neighbor? 
                    # nei[1] - distance from current (10 or 14)
                    # nei[2] - [tile_x_pos, tile_y_pos]
                    if nei[0]:
                        new_cost = current_cost + nei[1]
                        if nei[2] not in cost_so_far or new_cost < cost_so_far[nei[2]]:
                            cost_so_far[nei[2]] = new_cost
                            h_cost = Enemy.__heuristic(nei[2], dst_tile)
                            priority = [h_cost + new_cost, h_cost, new_cost]
                            heapq.heappush(pqueue, [priority, nei[2]])
                            came_from[nei[2]] = current[1] 
        self.path = came_from

    def update(self, player_rect):
        if (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE) not in self.path:
            print("!!!")
            return
        dest = self.path[(self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)]
        if dest == None:
            return
        real_dest = dest[0] * TILE_SIZE + HALF_TSIZE, dest[1] * TILE_SIZE + HALF_TSIZE
        
        a = real_dest[0] - self.rect.centerx
        b = real_dest[1] - self.rect.centery 
        move_angle = desired_angle = (math.degrees((math.atan2(a, b))) - 180) % 360
        self.angle %= 360
        
        #--------sees player?
        # calculate angle player-enemy
        a = player_rect.centerx - self.rect.centerx 
        b = player_rect.centery - self.rect.centery
        player_angle =  (math.degrees((math.atan2(a, b))) - 180) % 360
        #desired_angle = player_angle
        #self.weapon.shoot(False)
        if self.weapon.simulate(270 - player_angle, player_rect):
            desired_angle = player_angle
            if abs(self.angle - player_angle) < 0.5:
                self.weapon.shoot(False)
        
        rotation_speed = 6
        if abs(self.angle -  desired_angle) < rotation_speed:
            self.angle = desired_angle
        elif (self.angle - desired_angle) % 360 > 180:
            self.angle += rotation_speed
        else:
            self.angle -= rotation_speed

        cos_alpha = math.cos(math.radians(270 - move_angle))
        sin_alpha = math.sin(math.radians(270 - move_angle))
    
        super().update(self.speed * cos_alpha, self.speed * sin_alpha)
        self.weapon.update(self.rect.centerx, self.rect.centery, 270 - self.angle)

    def updateAll(player_rect):
        player_pos = (player_rect.centerx // TILE_SIZE, player_rect.centery // TILE_SIZE)
        for enemy in Enemy.enemylist:
            enemy.find_path(player_pos)

        for enemy in Enemy.enemylist:
            enemy.update(player_rect)

    def draw_paths(display):
        for enemy in Enemy.enemylist:
            enemy.draw_path(display)

    def draw_path(self, display):
        tmp_red = pygame.Surface((16, 16))
        tmp_red.set_alpha(50)
        tmp_red.fill((255,0,0))
        pos = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
        while pos != None:
            display.blit(tmp_red, (pos[0] * TILE_SIZE - camera[0],pos[1] * TILE_SIZE - camera[1]))
            if pos not in self.path:
                break
            pos = self.path[pos]

    def clear():
        Enemy.enemylist = []

    def empty():
        if Enemy.enemylist:
            return False
        return True

    def refresh():
        Enemy.enemylist = [x for x in Enemy.enemylist if x.active]

    def renderAll(display):
        for enemy in Enemy.enemylist:
            enemy.render(display)
