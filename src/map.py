import asset_manager
from global_vars import *

class Map:
    tilemap = []
    render_layers = [[], []]
    tile_types = {}
    collidable_tiles = {'wall'}
    def load_map(path):
        f = open(path).readlines()
        for idx, line in enumerate(f):
            if line == '\n':
                f = f[idx + 1:]
                break
            line = line.split('=')
            Map.tile_types[idx] = line[0]
            asset_manager.AssetManager.add_texture(line[0], line[1][:-1])

        enemies = []
        start = (-TILE_SIZE, -TILE_SIZE)
        for y, line in enumerate(f):
            if line == '\n':
                f =f[y + 1:]
                break
            line = line[:-1].split(',')
            Map.tilemap.append([])
            for x, num in enumerate(line):
                Map.tilemap[y].append(Map.tile_types[int(num)])
                if Map.tile_types[int(num)] == 'start':
                    start = (x * TILE_SIZE, y * TILE_SIZE)
                elif Map.tile_types[int(num)] == 'enemy_spawn':
                    enemies.append((x * TILE_SIZE, y * TILE_SIZE))

        return start, enemies 
        #for line in Map.tilemap:
         #   print(line)
        #broprint("\nCollidable tiles: ",  Map.collidable_tiles, "\n")

    def clear():
        Map.tilemap = []
        Map.render_layers = [[], []]
        Map.tile_types = {}

    def is_collidable(x, y):
        try:
            return x >= 0 and  y>= 0 and Map.tilemap[y][x] in Map.collidable_tiles
        except IndexError:
            return False

    def render(display, layer):
        for y in range(camera[1] // TILE_SIZE, (camera[1] + SURFACE_SIZE[1]) // TILE_SIZE + 1):
            for x in range(camera[0] // TILE_SIZE, (camera[0] + SURFACE_SIZE[0]) // TILE_SIZE + 1):
                if x >= 0 and y >= 0:
                    try:
                        tile_id = Map.tilemap[y][x]
                        if tile_id in Map.collidable_tiles and layer == 0:
                            tile_id = False
                        elif not (tile_id in Map.collidable_tiles) and layer == 1:
                            tile_id = False
                    except IndexError:
                        tile_id = False
                    if tile_id:
                        display.blit(asset_manager.AssetManager.get_texture(tile_id), (x * TILE_SIZE - camera[0],y * TILE_SIZE - camera[1]))